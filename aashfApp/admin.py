from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.db import transaction
from django.http import HttpResponse
import csv

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  

class EventAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('e_name', 'open_date', 'close_date', 'display_image')
    search_fields = ('e_name',)
    list_per_page = 20
    # list_filter = ('date',)
    ordering = ('-close_date',)
    
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    @transaction.atomic
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
    
    def display_image(self, obj):
        if obj.event_image.exists():
            first_image = obj.event_image.first()
            if first_image and first_image.event_image:
                return format_html('<img src="{}" width="70" height="50" />'.format(first_image.event_image.url))
        return "No Image"
    
    display_image.short_description = 'Image'

# class RegisterAdmin(admin.ModelAdmin):
#     @transaction.atomic
#     def save_model(self, request, obj, form, change):
#         # Perform your custom save logic if needed
#         super().save_model(request, obj, form, change)
        
#     list_display = ('id', 'event', 'name', 'address', 'mobile', 'email', 'display_image')
#     list_per_page = 20
#     def display_image(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" width="70" height="50" />'.format(obj.image.url))
#         return "No Image"
    
#     display_image.short_description = 'Image'

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
    field_names = [field.verbose_name for field in myVol_Registration._meta.fields]
    writer.writerow(field_names)

    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in myVol_Registration._meta.fields])

    return response

class YourModelAdmin(admin.ModelAdmin):
    actions = [export_as_csv]

@admin.register(myVol_Registration)
class MyVolRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Full_Name', 
        'mobile', 
        'Present_Address', 
        'Permanent_Address', 
        'show_image', 
        'show_nid',
        'facebook_link'
    )
    search_fields = ('Full_Name', 'email', 'mobile')
    readonly_fields = ('show_image', 'show_nid')
    actions = [export_as_csv]
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "No Image"

    def show_nid(self, obj):
        if obj.nid:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.nid.url)
        return "No NID"
        
    def facebook_link(self, obj):
        if obj.facebook:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.facebook, obj.facebook)
        return "No Link"

    facebook_link.short_description = "Facebook Profile"
    show_image.short_description = "Picture"
    show_nid.short_description = "NID Image"


admin.site.register(Event, EventAdmin)
# admin.site.register(myVol_Registration)
admin.site.register(Video)
admin.site.register(Volunteer)
admin.site.register(Setting)
admin.site.register(Region)
admin.site.register(Campaign)
admin.site.register(Project)
admin.site.register(Blog)
admin.site.register(GoverningBodie)
admin.site.register(Advisor)
admin.site.register(Awards)
admin.site.register(Mission)
admin.site.register(Contact)
admin.site.register(Rohingya)
admin.site.register(LegalDocument)
admin.site.register(Activiti)
admin.site.register(Location)
admin.site.register(ShariahAdvisor)