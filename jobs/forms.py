from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'required_skills',
            'education_required',
            'experience_required',
            'location',
            'job_type',
            'salary_min',
            'salary_max',
            'is_active',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Machine Learning Engineer',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe the role, responsibilities, and requirements...',
            }),

            'required_skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Python, Machine Learning, SQL, Django',
            }),

            'education_required': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'B.Tech / B.E. / M.Tech in Computer Science',
            }),

            'experience_required': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hyderabad, India',
            }),

            'job_type': forms.Select(attrs={
                'class': 'form-control',
            }),

            'salary_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Minimum salary',
            }),

            'salary_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Maximum salary',
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }