from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.db import transaction

    

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

class RegisterAdmin(admin.ModelAdmin):
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        # Perform your custom save logic if needed
        super().save_model(request, obj, form, change)
        
    list_display = ('id', 'event', 'name', 'address', 'mobile', 'email', 'display_image')
    list_per_page = 20
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="70" height="50" />'.format(obj.image.url))
        return "No Image"
    
    display_image.short_description = 'Image'
admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegisterAdmin)
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