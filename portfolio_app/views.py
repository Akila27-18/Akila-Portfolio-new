import os
import threading
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .forms import ContactForm

logger = logging.getLogger(__name__)

# -----------------------------
# Asynchronous Email Sender
# -----------------------------
def send_email_async(subject, message, from_email, recipient_list):
    """Send email in a background thread to avoid blocking the response."""
    def _send():
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info("Email sent successfully to %s", recipient_list)
        except BadHeaderError:
            logger.error("Invalid email header detected for email to %s", recipient_list)
        except Exception as e:
            logger.exception("Failed to send email to %s. Error: %s", recipient_list, e)

    threading.Thread(target=_send, daemon=True).start()

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
        'education_list': education_list,
    })

# -----------------------------
# Contact Submit
# -----------------------------
# def contact_submit(request):
#     if request.method != "POST":
#         return redirect(reverse('portfolio_app:index'))

#     form = ContactForm(request.POST)
#     if not form.is_valid():
#         return render(request, 'portfolio_app/index.html', {'form': form})

#     name = form.cleaned_data['name'].strip()
#     email = form.cleaned_data['email'].strip()
#     message = form.cleaned_data['message'].strip()

#     subject = f"Portfolio Contact Form - {name}"
#     body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
#     from_email = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [settings.EMAIL_HOST_USER]

#     try:
#         send_email_async(subject, body, from_email, recipient_list)
#         messages.success(request, "Your message has been submitted successfully!")
#     except Exception as e:
#         logger.exception("Error sending email: %s", e)
#         messages.error(request, f"Something went wrong while sending the email: {e}")

#     return redirect(f"{reverse('portfolio_app:success_page')}?name={name}")

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        try:
            send_mail(
                subject=f"New message from {name}",
                message=f"From: {email}\n\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["akila271819@gmail.com"],  # change this to your inbox
                fail_silently=False,
            )
            return redirect(f"/success/?name={name}")

        except Exception as e:
            print("Email error:", e)  # will also print in terminal
            return HttpResponse(f"Email error: {e}")  # 👈 shows actual error in browser

    return render(request, "contact.html")

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
        settings.BASE_DIR, 'portfolio_app', 'static', 'portfolio_app', 'files', 'Akila_Resume.pdf'
    )

    if not os.path.exists(file_path):
        logger.warning("CV file not found: %s", file_path)
        raise Http404("CV not found")

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=\"Akila_Resume.pdf\"'
            return response
    except Exception as e:
        logger.exception("Failed to serve CV file: %s", e)
        raise Http404("CV cannot be downloaded at this time.")

