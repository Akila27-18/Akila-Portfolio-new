from django.urls import path
from . import views

app_name = 'portfolio_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('success/', views.success_page, name='success_page'),
    path('download-cv/', views.download_cv, name='download_cv'),
]
