from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import StudentProfile


class StudentProfileTests(TestCase):
    def setUp(self):
        self.media = TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.settings_override = override_settings(MEDIA_ROOT=self.media.name)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

    def profile_data(self, **overrides):
        data = {
            "full_name": "Ahmed Wael Younis",
            "university_id": "00120230395",
            "age": 22,
            "date_of_birth": date(2004, 6, 12),
            "address": "Gaza",
            "salary": Decimal("1500.25"),
            "photo": "profiles/avatar.png",
        }
        data.update(overrides)
        return data

    def test_home_has_empty_state(self):
        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add a student profile")

    def test_saved_profile_appears_on_all_home_routes(self):
        profile = StudentProfile.objects.create(**self.profile_data())
        profile.refresh_from_db()
        self.assertEqual(profile.university_id, "00120230395")
        self.assertEqual(profile.salary, Decimal("1500.25"))
        for route in ("pages:home", "pages:home_page", "pages:index"):
            response = self.client.get(reverse(route))
            self.assertTemplateUsed(response, "pages/home.html")
            for value in ("Ahmed Wael Younis", "00120230395", "22", "12 June 2004", "Gaza", "1,500.25", "/media/profiles/avatar.png"):
                self.assertContains(response, value)

    def test_invalid_values_are_rejected(self):
        invalid = (
            {"age": 0}, {"age": 121}, {"salary": Decimal("-0.01")},
            {"university_id": "ABC"},
            {"date_of_birth": timezone.localdate() + timedelta(days=1)},
        )
        for values in invalid:
            with self.subTest(values=values), self.assertRaises(ValidationError):
                StudentProfile(**self.profile_data(**values)).full_clean()

    def test_university_id_is_unique(self):
        StudentProfile.objects.create(**self.profile_data())
        with self.assertRaises(ValidationError):
            StudentProfile(**self.profile_data()).full_clean()

    def test_admin_can_save_profile_and_upload_image(self):
        admin = get_user_model().objects.create_superuser("testadmin", password="local-test-password")
        self.client.force_login(admin)
        image = BytesIO()
        Image.new("RGB", (50, 50), "green").save(image, format="PNG")
        data = self.profile_data(photo=SimpleUploadedFile("avatar.png", image.getvalue(), content_type="image/png"))
        response = self.client.post(reverse("admin:pages_studentprofile_add"), data)
        self.assertEqual(response.status_code, 302)
        profile = StudentProfile.objects.get()
        self.assertTrue(profile.photo.storage.exists(profile.photo.name))
        self.assertContains(self.client.get(reverse("pages:home")), profile.photo.url)

    def test_admin_rejects_non_image_upload(self):
        admin = get_user_model().objects.create_superuser("testadmin", password="local-test-password")
        self.client.force_login(admin)
        data = self.profile_data(photo=SimpleUploadedFile("invalid.png", b"not an image", content_type="image/png"))
        response = self.client.post(reverse("admin:pages_studentprofile_add"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("photo", response.context["adminform"].form.errors)
        self.assertEqual(StudentProfile.objects.count(), 0)
