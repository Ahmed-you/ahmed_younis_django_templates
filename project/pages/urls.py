from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home_page'),
    path('index/', views.home, name='index'),
]
