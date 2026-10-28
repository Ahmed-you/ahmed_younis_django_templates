from django.contrib import admin

from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "university_id", "age", "address", "salary")
    search_fields = ("full_name", "university_id", "address")
    fields = ("full_name", "university_id", "age", "date_of_birth", "address", "salary", "photo")
