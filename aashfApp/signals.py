from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Event, Video, Volunteer

# Clear the cache when an Event is created, updated, or deleted
@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
def clear_event_cache(sender, **kwargs):
    cache.delete('home_events')
    cache.delete('events_cache')
    cache.delete('banner_image_cache')

# Clear the cache when a Video is created, updated, or deleted
@receiver(post_save, sender=Video)
@receiver(post_delete, sender=Video)
def clear_video_cache(sender, **kwargs):
    cache.delete('home_videos')

# Clear the cache when a Volunteer is created, updated, or deleted
@receiver(post_save, sender=Volunteer)
@receiver(post_delete, sender=Volunteer)
def clear_volunteer_cache(sender, **kwargs):
    cache.delete('home_volunteers')
