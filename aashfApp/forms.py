from django import forms
from .models import myVol_Registration, Contact
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from ahospital.models import NikahRegistration


class EventRegistrationForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = myVol_Registration
        fields = ['Full_Name', 'email', 'mobile', 'nid', 'Present_Address', 'Permanent_Address', 'image', 'facebook', 'captcha']
        widgets = {
            'Full_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Enter Address'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'nid': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'Present_Address': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
            'Permanent_Address': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Facebook profile link'
            }),
        }

class NikahRegistrationForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = NikahRegistration
        fields = ['email', 'groom_name', 'groom_present_address', 'groom_permanent_address', 'groom_occupation', 'groom_education', 'groom_nid', 'groom_mobile', 'groom_alternate_mobile', 'groom_father', 'groom_father_mobile', 'bride_name', 'bride_present_address', 'bride_permanent_address', 'bride_occupation', 'bride_education', 'bride_nid', 'bride_mobile', 'bride_alternate_mobile', 'bride_father', 'bride_father_mobile', 'applicant_name', 'applicant_mobile', 'applicant_groom', 'applicant_bride', 'groom_image', 'bride_image', 'captcha']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'groom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_permanent_address': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
            'groom_present_address': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
            'groom_occupation': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
            'groom_education': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_alternate_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_father': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_father_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_permanent_address': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
            'bride_present_address': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
            'bride_occupation': forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
            'bride_education': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_alternate_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_father': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_father_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'applicant_name': forms.TextInput(attrs={'class': 'form-control'}), 'applicant_mobile': forms.TextInput(attrs={'class': 'form-control'}), 'applicant_groom': forms.Select(attrs={'class': 'form-control'}),
            'applicant_bride': forms.Select(attrs={'class': 'form-control'}),
            'groom_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'bride_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = Contact
        fields = ['message', 'name', 'email', 'subject', 'captcha']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Your Name'}),
            'message': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Write Message'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'})
        }