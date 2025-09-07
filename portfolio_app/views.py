
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
import os
from django.http import FileResponse
from django.http import FileResponse, Http404
from django.contrib.staticfiles import finders

def index(request):
    return render(request, 'portfolio_app/index.html')

def index(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                subject=f"Portfolio Contact Form - {name}",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['akila271819@gmail.com'],  # change to your email
                fail_silently=False,
            )
            success = True
    else:
        form = ContactForm()

    return render(request, 'portfolio_app/index.html', {'form': form, 'success': success})




# ✅ CV Download View
# def download_cv(request):
#     filepath = os.path.join(settings.BASE_DIR, "static/portfolio_app/files/Muppudathi_CV.pdf")
#     return FileResponse(open(filepath, "rb"), as_attachment=True, filename="Muppudathi_CV.pdf")
def download_cv(request):
    filepath = finders.find("portfolio_app/files/Akila_Resume.pdf")
    if not filepath:
        raise Http404("CV not found.")
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename="Akila_Resume.pdf")


def success_page(request):
    name = request.GET.get('name', 'User')
    return render(request, "portfolio_app/success.html", {"name": name})