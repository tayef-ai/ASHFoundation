from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .models import *
from django.core.exceptions import ValidationError

class CustomerRegistrationForm(UserCreationForm):
    # Adding the role field from the Customer model
    role = forms.ChoiceField(
        choices=[('Patient', 'রোগী'), ('Doctor', 'ডাক্তার')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Role"
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender')] + [('Male', 'Male'), ('Female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Gender"
    )
    name = forms.CharField(label='Enter Your Name', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    dob = forms.DateField(
        label='Enter Your Date of Birth', 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = get_user_model()
        fields = ['name', 'dob', 'gender', 'email', 'role', 'password1', 'password2']  # Role added after email
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get('password1')
    #     password2 = cleaned_data.get('password2')
        
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("The two password fields didn’t match.")
        
    #     return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Customer.objects.create(user=user, role=self.cleaned_data['role'], name=self.cleaned_data['name'], dob=self.cleaned_data['dob'])
        return user


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}))
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus':True, "autocomplete": "email", 'class': 'form-control'}),
    )

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autofocus':True, "autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )

class CustomerProfileForm(UserChangeForm):
    role = forms.ChoiceField(
        choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')],
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        required=False,
        label="Role"
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        required=False,
        label="Gender"
    )
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    phone = forms.CharField(label='Mobile', widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = get_user_model()
        fields = ['name', 'dob', 'gender', 'role', 'email', 'address', 'phone']  # Role added after email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Update or create Customer data
            Customer.objects.filter(user=user).update(
                name=self.cleaned_data.get('name'),
                dob=self.cleaned_data.get('dob'),
                address=self.cleaned_data.get('address'),
                phone=self.cleaned_data.get('phone'),
            )
        return user

