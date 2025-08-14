from django import forms
from django.contrib.auth.models import User
from .models import Profile, Settings, Report
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        # Set the label to an empty string to prevent it from rendering in the template
        label='',
        help_text='', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')



class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Override the 'bio' field to use a Textarea widget with custom styling
        self.fields['bio'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,  # Adjust rows for better user experience
            'placeholder': 'Tell us a little about yourself...'
        })
        
        # Add a custom label and styling for the 'avatar' field
        self.fields['avatar'].label = 'Profile Picture'
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control' # Use 'form-control' for a modern file input style
        })
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Style the 'allow_notifications' checkbox
        self.fields['allow_notifications'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['allow_notifications'].label = 'Allow Notifications'
        
        # Style the 'profile_visibility' as a standard text input
        self.fields['profile_visibility'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g., Public, Private'
        })
        self.fields['profile_visibility'].label = 'Profile Visibility'
    
    class Meta:
        model = Settings
        fields = ['allow_notifications', 'profile_visibility']


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Override the 'reason' field to use a Textarea widget with custom styling
        self.fields['reason'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,  # Adjust rows for better user experience
            'placeholder': 'Please provide details for your report...'
        })
        
        # Set a clear label for the field
        self.fields['reason'].label = 'Reason for Report'

    class Meta:
        model = Report
        fields = ['reason']
