import os
import logging
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import FileResponse, Http404
from django.urls import reverse
from django.contrib import messages
from .forms import ContactForm

# Set up logger
logger = logging.getLogger(__name__)

# -----------------------------
# Home / Index Page
# -----------------------------
def index(request):
    form = ContactForm()
    education_list = [
        {'degree': 'B.Sc Computer Science', 'institution': 'University Name', 'year': '2019-2023'},
        {'degree': 'High School Diploma', 'institution': 'School Name', 'year': '2017-2019'}
    ]
    return render(request, 'portfolio_app/index.html', {
        'form': form,
        'education_list': education_list
    })


# -----------------------------
# Contact Form Submission
# -----------------------------
def contact_submit(request):
    if request.method != "POST":
        return redirect('index')

    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, 'portfolio_app/index.html', {'form': form})

    name = form.cleaned_data['name'].strip()
    email = form.cleaned_data['email'].strip()
    message = form.cleaned_data['message'].strip()

    # --- Email to site owner ---
    try:
        send_mail(
            subject=f"Portfolio Contact Form - {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except BadHeaderError:
        logger.error("Invalid header found while sending email to site owner.")
    except Exception as e:
        logger.exception("Failed to send email to site owner: %s", e)

    # --- Thank-you email to sender (optional) ---
    try:
        send_mail(
            subject="Thanks for reaching out!",
            message=(
                f"Hi {name},\n\n"
                "Thanks for contacting me. I’ve received your message:\n\n"
                f"{message}\n\n"
                "I’ll reply as soon as possible.\n\n"
                "- Akila"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,  # Never crash if user email fails
        )
    except Exception as e:
        logger.exception("Failed to send thank-you email to sender: %s", e)

    # Always redirect to success page, even if emails fail
    messages.success(request, "Thank you for your message! I will get back to you soon.")
    return redirect(f"{reverse('portfolio_app:success_page')}?name={name}")


# -----------------------------
# Success Page
# -----------------------------
def success_page(request):
    name = request.GET.get('name', 'User')
    return render(request, "portfolio_app/success.html", {"name": name})


# -----------------------------
# CV Download
# -----------------------------
def download_cv(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        'portfolio_app',
        'static',
        'portfolio_app',
        'files',
        'Akila_Resume.pdf'
    )

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Akila_Resume.pdf')
    else:
        raise Http404("CV not found")
