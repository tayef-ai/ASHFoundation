from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import *
from django.utils.html import format_html

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = MyUser
        fields = ["email", "name"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ["email", "password", "name", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "is_active"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Customer)
admin.site.register(HActiviti)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Prescription)

@admin.action(description='Export selected items as CSV')
def export_as_csv(modeladmin, request, queryset):
    # Create HTTP response for CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    
    # Add UTF-8 BOM for better compatibility with Excel
    response.write('\ufeff'.encode('utf-8'))
    
    # Create a CSV writer with UTF-8 encoding
    writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Write headers
    field_names = [field.verbose_name for field in NikahRegistration._meta.fields]
    writer.writerow(field_names)

    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in NikahRegistration._meta.fields])

    return response

class YourModelAdmin(admin.ModelAdmin):
    actions = [export_as_csv]

@admin.register(NikahRegistration)
class NikahRegistrationAdmin(admin.ModelAdmin):
    # Display all fields in the admin list view
    list_display = [
        'groom_name',
        'groom_mobile',
        'groom_father_mobile',
        'groom_present_address',
        'bride_name',
        'bride_mobile',
        'bride_father_mobile',
        'bride_present_address',
        'show_groom_image',
        'show_bride_image',
    ]

    # Add search functionality
    search_fields = ['groom_name', 'bride_name', 'groom_mobile', 'bride_mobile']

    # Add actions
    actions = [export_as_csv]

    # Add filter options for related fields
    # list_filter = ['event', 'groom_education', 'bride_education']

    # Display images in admin panel
    readonly_fields = ('show_groom_image', 'show_bride_image')

    def show_groom_image(self, obj):
        if obj.groom_image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.groom_image.url)
        return "No Image"

    def show_bride_image(self, obj):
        if obj.bride_image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.bride_image.url)
        return "No Image"

    show_groom_image.short_description = "Groom's Photo"
    show_bride_image.short_description = "Bride's Photo"

# admin.site.register(NikahRegistration, YourModelAdmin)
