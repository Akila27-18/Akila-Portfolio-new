import os
import logging
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib import messages
from .forms import ContactForm

# Logger for debugging
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
        return render(request, 'portfolio_app/index.html', {'form': form})

    name = form.cleaned_data['name'].strip()
    email = form.cleaned_data['email'].strip()
    message = form.cleaned_data['message'].strip()

    # Determine if email backend is SMTP (local dev) or something else (Render)
    is_smtp = settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend'

    # --- Email to site owner ---
    try:
        send_mail(
            subject=f"Portfolio Contact Form - {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=not is_smtp,  # only raise errors locally
        )
    except Exception as e:
        logger.warning("Email sending failed: %s", e)
        if is_smtp:
            messages.error(request, "Failed to send your message. Please try again later.")
            return render(request, 'portfolio_app/index.html', {'form': form})
        else:
            # On Render, just log it and continue
            messages.info(request, "Message received. Email sending is disabled on this host.")

    # --- Thank-you email to sender (optional) ---
    if email:
        try:
            send_mail(
                subject="Thanks for reaching out!",
                message=(
                    f"Hi {name},\n\n"
                    "Thanks for contacting me. I’ve received your message:\n\n"
                    f"{message}\n\n"
                    "I will review and reply promptly.\n\n"
                    "- Akila C"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,  # never fail hard for thank-you email
            )
        except Exception as e:
            logger.warning("Thank-you email failed: %s", e)

    # --- Redirect to success page ---
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

    if not os.path.exists(file_path):
        logger.warning("CV file not found: %s", file_path)
        raise Http404("CV not found")

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Akila_Resume.pdf"'
            return response
    except Exception as e:
        logger.exception("Failed to serve CV file: %s", e)
        raise Http404("CV cannot be downloaded at this time.")
