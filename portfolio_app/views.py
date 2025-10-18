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

    # Optional: Get success message from query parameters
    success = request.GET.get('success')
    name = request.GET.get('name', '')

    return render(request, 'portfolio_app/index.html', {
        'form': form,
        'education_list': education_list,
        'success': success,
        'name': name,
    })


# -----------------------------
# Contact Form Submission
# -----------------------------
def contact_submit(request):
    if request.method != "POST":
        return redirect(reverse('portfolio_app:index'))

    form = ContactForm(request.POST)
    if not form.is_valid():
        # Stay on the form page and display validation errors
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
        messages.error(request, "There was an error sending your message. Please try again.")
        return render(request, 'portfolio_app/index.html', {'form': form})
    except Exception as e:
        logger.exception("Failed to send email to site owner: %s", e)
        messages.error(request, "Failed to send your message. Please try again later.")
        return render(request, 'portfolio_app/index.html', {'form': form})

    # --- Optional: Thank-you email to sender ---
    try:
        send_mail(
            subject="Thanks for reaching out!",
            message=(
                f"Hi {name},\n\n"
                "Thanks for contacting me. I’ve received your message:\n\n"
                f"{message}\n\n"
                "I will review and reply to this mail promptly.\n\n"
                "- Akila C"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,  # Don't crash if user email fails
        )
    except Exception as e:
        logger.exception("Failed to send thank-you email to %s <%s>: %s", name, email, e)

    # Success: redirect back to the form page with success message
   # After successful email sending
    return redirect(f"{reverse('portfolio_app:success_page')}?name={name}")



# -----------------------------
# Success Page (optional)
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
        # Open without 'with' so FileResponse can stream the file
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Akila_Resume.pdf')
    else:
        raise Http404("CV not found")
