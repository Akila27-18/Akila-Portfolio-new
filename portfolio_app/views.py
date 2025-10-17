from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse, Http404
import os
from .forms import ContactForm
from django.contrib import messages

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
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            try:
                # Email to site owner
                send_mail(
                    subject=f"Portfolio Contact Form - {name}",
                    message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['akila271819@gmail.com'],
                    fail_silently=False,
                )

                # Thank-you email to sender
                send_mail(
                    subject="Thank you for contacting Akila",
                    message=(
                        f"Dear {name},\n\n"
                        "Thank you for reaching out. I have received your message and will review it promptly. "
                        "You can expect a reply shortly.\n\n"
                        "Yours sincerely,\n"
                        "Akila"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )

            except Exception as e:
                import traceback
                print("Email error:", e)
                print(traceback.format_exc())
                messages.error(request, "Email failed. Check logs.")
                return render(request, 'portfolio_app/index.html', {'form': form})


            # Redirect to success page
            return redirect(f'/success/?name={name}')
        else:
            # Form invalid, redisplay with errors
            return render(request, 'portfolio_app/index.html', {'form': form})

    # If not POST, redirect to index
    return redirect('index')


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
    

