from django.shortcuts import render

from .models import StudentProfile


def home(request):
    return render(request, "pages/home.html", {"profiles": StudentProfile.objects.all()})
