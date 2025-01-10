from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import EventRegistrationForm, ContactForm, NikahRegistrationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
import random
from itertools import chain
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.paginator import Paginator
import json
from django.urls import reverse
# from django.contrib.gis.geoip2 import GeoIP2

# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def redirect_to_bangladesh(request):
    url = reverse('home', kwargs={'country': 'Bangladesh'})
    return redirect(url)

def map_view(request):
    region = request.GET.get('country', 'Bangladesh')
    locations = Location.objects.all().values('name', 'latitude', 'longitude', 'url')
    locations_list = list(locations)  # Convert QuerySet to a list of dictionaries
    locations_json = json.dumps(locations_list)  # Serialize list to JSON
    return render(request, 'map.html', {'locations_json': locations_json, 'country': region})

def homeview(request, country):
    # user_ip = request.META.get('REMOTE_ADDR', '127.0.0.1') 
    # g = GeoIP2()
    # if user_ip == '127.0.0.1':
    #     country = 'Bangladesh'
    # else:
    #     country = g.country_name(user_ip)
    # if country == 'Bangladesh':
    # country = request.GET.get('country', 'Bangladesh')
    print("======================", country)
    r = Region.objects.get(name=country)
    query = Setting.objects.get(region=r)
    # today = timezone.now().date()
    events = None
    activities = None
    videos = None
    volunteers = None
    locations_json = None
    b_query = Blog.objects.filter(region=r).order_by('-created_at')[:6]
    p_query = Project.objects.filter(region=r).order_by('-created_at')[:6]
    c_query = Campaign.objects.filter(region=r).order_by('-created_at')[:6]
    if not activities:
        activities = Activiti.objects.filter(region=r).order_by('-created_at')[:6]
    # if not events:
    #     ongoing_events = Event.objects.filter(region=r, open_date__lte=today, close_date__gte=today)
    #     upcoming_events = Event.objects.filter(region=r, open_date__gt=today)
    #     closed_events = Event.objects.filter(region=r, close_date__lt=today)

    #         # Combine the querysets
    #     events = list(chain(ongoing_events, upcoming_events, closed_events))[:3]

        # Cache the events result for 10 minutes (600 seconds)
        # cache.set('home_events', events, timeout=CACHE_TTL)

    if not videos:
        videos = Video.objects.filter(region=r).order_by('-created_at')[:6]
        # Cache the videos result for 10 minutes (600 seconds)
        # cache.set('home_videos', videos, timeout=CACHE_TTL)

    if not volunteers:
        volunteers = Volunteer.objects.filter(region=r)[:3]
        # Cache the volunteers result for 10 minutes (600 seconds)
        # cache.set('home_volunteers', volunteers, timeout=CACHE_TTL)
    if not locations_json:
        locations = Location.objects.all().values('name', 'latitude', 'longitude', 'url')
        locations_list = list(locations)  # Convert QuerySet to a list of dictionaries
        locations_json = json.dumps(locations_list)  # Serialize list to JSON

    # Render the response with cached or freshly fetched data
    return render(request, 'home.html', {'projects': p_query, 'videos': videos, 'campaigns': c_query, 'setting': query, 'activities':activities, 'locations_json': locations_json, 'country': country, 'blogs': b_query})

def eventview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    today = timezone.now().date()
    events = None
    banner_image = None
    if not events or not banner_image:
        # If the cache is empty, query the database
        if not events:
            ongoing_events = Event.objects.filter(region=r, open_date__lte=today, close_date__gte=today)
            upcoming_events = Event.objects.filter(region=r, open_date__gt=today)
            closed_events = Event.objects.filter(region=r, close_date__lt=today)

            # Combine the querysets
            events = list(chain(ongoing_events, upcoming_events, closed_events))
            paginator = Paginator(events, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        if events:
            # Get the last event and its banner image
           
            banner_image = events[0].event_image.filter(is_banner=True).first()
        else:
            banner_image = None
        # Cache the events and banner image
        # cache.set('events_cache', events, timeout=CACHE_TTL)
        # cache.set('banner_image_cache', banner_image, timeout=CACHE_TTL)

    context = {
        'events': page_obj,
        'banner': banner_image,
        'country': region,
    }
    return render(request, 'event.html', context)

def event_detail(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = Event.objects.get(pk=id)
    banner_image = query.event_image.filter(is_banner=True).first()
    # print("==================", banner_image) 
    return render(request, 'event_details.html', {'query': query, 'banner': banner_image, 'country': region})

def vol_event_register(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = Event.objects.get(pk=id)
    banner_image = query.event_image.filter(is_banner=True).first()
    
    if request.method == 'GET':
        form = EventRegistrationForm()
        return render(request, 'vol_event_register.html', {'query': query, 'form': form, 'banner': banner_image, 'country': region})
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.event = query
            form.save()
            messages.success(request, "আপনার আবেদনটি সফলভাবে গৃহীত হয়েছে!!!")
            return redirect('vol_event_register', id=id)
        else:
            error_message = "ফর্ম জমা দেওয়ার সময় একটি ত্রুটি ছিল৷ বিস্তারিত চেক করুন এবং আবার চেষ্টা করুন।"
            messages.warning(request, error_message)
    return render(request, 'vol_event_register.html', {'query': query, 'form': form, 'banner': banner_image, 'country': region})

def event_register(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = Event.objects.get(pk=id)
    banner_image = query.event_image.filter(is_banner=True).first()
    event = get_object_or_404(Event, id=id)
    today = timezone.now().date()
    if today > event.close_date:
        return render(request, 'event_unavailable.html', {'country': region})
        
    if request.method == 'GET':
        form = NikahRegistrationForm()
        return render(request, 'event_register.html', {'query': query, 'form': form, 'banner': banner_image, 'country': region})
    
    if request.method == 'POST':
        form = NikahRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.event = query
            form.save()
            messages.success(request, "আপনার আবেদনটি সফলভাবে গৃহীত হয়েছে!!! নির্বাচিত হলে খুব শিঘ্রই আপনাকে জানানো হবে।")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': "Your form has been submitted successfully!"})
            return redirect('event_register', id=id)
        else:
            error_message = "ফর্ম জমা দেওয়ার সময় একটি ত্রুটি ছিল৷ বিস্তারিত চেক করুন এবং আবার চেষ্টা করুন।"
            messages.warning(request, error_message)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': error_message})
    return render(request, 'event_register.html', {'query': query, 'form': form, 'banner': banner_image, 'country': region})
            
def gallery(request):
    region = request.GET.get('country', 'Bangladesh')
    query = None
    banner_image = None
    if not query:
        query = Image.objects.all().order_by('-id')
        paginator = Paginator(query, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # cache.set('all_images', query)
    if not banner_image:
        banner_image = Image.objects.filter(is_banner=True).first()
        # cache.set('banner_image', banner_image)
    return render(request, 'gallery.html', {'banner': banner_image, 'query': page_obj, 'country': region})

def contactview(request):
    region = request.GET.get('country', 'Bangladesh')
    query = None
    # map_iframe = cache.get('google_map_iframe')
    map_iframe = None
    if not query:
        query = Image.objects.all().order_by('-id')
        # cache.set('images', query, timeout=CACHE_TTL)
    if not map_iframe:
        # If not cached, render the iframe HTML
        map_iframe = """
            <div class="d-none d-sm-block mb-5 pb-4">
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1844.741367879672!2d91.85352633936633!3d22.373152038879955!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x30acd942e1dd4e4b%3A0x185a64b7b8defff0!2sAlhaj%20Shamsul%20Hoque%20Foundation%20(ASHF)!5e0!3m2!1sen!2sbd!4v1728715541149!5m2!1sen!2sbd" width="1000" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>
        """
        # Store the iframe in the cache
        # cache.set('google_map_iframe', map_iframe, timeout=CACHE_TTL)
    form = ContactForm()
    banner_image = Image.objects.filter(is_banner=True).first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, "Your form has been submitted successfully!")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': "Your form has been submitted successfully!"})
            return redirect('contact')
        else:
            error_message = "There was an error submitting the form. Please check the details and try again."
            messages.error(request, error_message)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': error_message})

    return render(request, 'contact.html', {'banner': banner_image, 'query': query, 'map': map_iframe, 'form': form, 'country': region})

def projectview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = Project.objects.filter(region=r).order_by('-created_at')
    paginator = Paginator(query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'project.html', {'query': page_obj, 'country': region})

def videoview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = Video.objects.filter(region=r).order_by('-created_at')
    paginator = Paginator(query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'video.html', {'query': page_obj, 'country': region})

def project_detail(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = Project.objects.get(pk=id)
    return render(request, 'project_details.html', {'query': query, 'country': region})

def activityview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = Activiti.objects.filter(region=r).order_by('-created_at')
    paginator = Paginator(query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'activity.html', {'query': page_obj, 'country':region})

def activity_detail(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = Activiti.objects.get(pk=id)
    return render(request, 'activity_detail.html', {'query': query, 'country':region})

def campaignview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = Campaign.objects.filter(region=r).order_by('-created_at')
    paginator = Paginator(query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'campaign.html', {'query': page_obj, 'country': region})

def campaign_detail(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = Campaign.objects.get(pk=id)
    return render(request, 'campaign_details.html', {'query': query, 'country': region})

def rohingyaview(request):
    region = request.GET.get('country', 'Bangladesh')
    query = Rohingya.objects.all().order_by('-id')
    paginator = Paginator(query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'rohingya.html', {'query': page_obj, 'country':region})

def rohingya_detail(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = Rohingya.objects.get(pk=id)
    return render(request, 'rohingya_details.html', {'query': query, 'country': region})

def legalview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = LegalDocument.objects.filter(region=r).order_by('-id')
    # paginator = Paginator(query, 6)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'legal.html', {'query': query, 'country': region})

def legal_detail(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = LegalDocument.objects.get(pk=id)
    return render(request, 'legal_details.html', {'query': query, 'country': region})

def blogview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = Blog.objects.filter(region=r).order_by('-created_at')
    paginator = Paginator(query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'query': page_obj, 'country': region})

def blog_detail(request, id):
    region = request.GET.get('country', 'Bangladesh')
    query = Blog.objects.get(pk=id)
    return render(request, 'blog_details.html', {'query': query, 'country': region})

def gbview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = GoverningBodie.objects.filter(region=r)
    ad_query = Advisor.objects.filter(region=r)
    return render(request, 'gb.html', {'query': query, 'ad_query': ad_query, 'country': region})

def apview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = ShariahAdvisor.objects.filter(region=r)
    return render(request, 'ap.html', {'query': query, 'country': region})

def volunteerview(request):
    region = request.GET.get('country', 'Bangladesh')
    r = Region.objects.get(name=region)
    query = Volunteer.objects.filter(region=r).order_by('-id')
    paginator = Paginator(query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'volunteer.html', {'query': page_obj, 'country': region})

def awardview(request):
    region = request.GET.get('country', 'Bangladesh')
    query = Awards.objects.all().order_by('-id')
    return render(request, 'awards.html', {'query': query, 'country': region})

def missionview(request):
    region = request.GET.get('country', 'Bangladesh')
    query = Mission.objects.all()[:3]
    return render(request, 'mission.html', {'query': query, 'country': region})

def search(request):
    region = request.GET.get('country', 'Bangladesh')
    query = request.GET.get('q')
    region = Region.objects.filter(name__iexact=region).first()
    results = {
        'events': Event.objects.filter(
            models.Q(e_name__icontains=query) | models.Q(e_details__icontains=query), region=region
        ) if query else Event.objects.none(),
        'projects': Project.objects.filter(
            models.Q(p_name__icontains=query) | models.Q(p_details__icontains=query), region=region
        ) if query else Project.objects.none(),
        'blogs': Blog.objects.filter(
            models.Q(b_name__icontains=query) | models.Q(b_details__icontains=query), region=region
        ) if query else Blog.objects.none(),
        'volunteers': Volunteer.objects.filter(
            models.Q(name__icontains=query) | models.Q(address__icontains=query) | models.Q(role__icontains=query), region=region
        ) if query else Volunteer.objects.none(),
        'campaigns': Campaign.objects.filter(
            models.Q(c_name__icontains=query) | models.Q(c_details__icontains=query), region=region
        ) if query else Campaign.objects.none(),
        'rohingyas': Rohingya.objects.filter(
            models.Q(r_name__icontains=query) | models.Q(r_details__icontains=query)
        ) if query else Rohingya.objects.none(),
        'legal_documents': LegalDocument.objects.filter(
            models.Q(l_title__icontains=query), region=region
        ) if query else LegalDocument.objects.none(),
    }
    
    return render(request, 'search_results.html', {'query': query, 'results': results, 'country': region})

