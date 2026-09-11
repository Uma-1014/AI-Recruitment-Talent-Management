from django import forms
from .models import Candidate


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'full_name',
            'email',
            'phone',
            'resume',
            'skills',
            'education',
            'experience_years',
            'location',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Python, Django, Machine Learning, SQL',
            }),
            'education': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'B.Tech in Computer Science...',
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hyderabad, India',
            }),
        }