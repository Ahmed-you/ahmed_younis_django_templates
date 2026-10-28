from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


class StudentProfile(models.Model):
    full_name = models.CharField(max_length=150)
    university_id = models.CharField(
        "University ID number",
        max_length=20,
        unique=True,
        validators=[RegexValidator(r"^[0-9]+$", "Enter digits only.")],
    )
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    date_of_birth = models.DateField()
    address = models.TextField()
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Monthly salary in USD.",
    )
    photo = models.ImageField(upload_to="profiles/")

    class Meta:
        ordering = ["full_name", "pk"]

    def __str__(self):
        return self.full_name

    def clean(self):
        super().clean()
        if self.date_of_birth and self.date_of_birth > timezone.localdate():
            raise ValidationError({"date_of_birth": "Date of birth cannot be in the future."})
