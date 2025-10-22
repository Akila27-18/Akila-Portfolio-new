from django.urls import path
from . import views

app_name = 'portfolio_app'

urlpatterns = [
    path('', views.index, name='index'),                       # Home page with contact form
    path('contact-submit/', views.contact_submit, name='contact_submit'),  # Form submission
    path('success/', views.success_page, name='success_page'), # Success page
    path('download-cv/', views.download_cv, name='download_cv'),  # CV download
]
