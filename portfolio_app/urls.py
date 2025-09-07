
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path("download-cv/", views.download_cv, name="download_cv"),
    path("success/", views.success_page, name="success_page"),
]