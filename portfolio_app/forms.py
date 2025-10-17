from django import forms
from django.core.validators import RegexValidator

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z ]+$',
                message='Name can only contain letters and spaces.',
                code='invalid_name'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
        error_messages={'required': 'Please enter your name.'}
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}),
        error_messages={'required': 'Please enter a valid email address.'}
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control', 'rows': 4}),
        error_messages={'required': 'Please enter your message.'}
    )
