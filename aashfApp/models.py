from django.db import models
from django.utils import timezone
from PIL import Image as PilImage
from io import BytesIO
from django.core.files import File
from django.utils.timezone import make_aware
from ckeditor.fields import RichTextField
import re

def get_youtube_video_id(url):
    # Regex pattern to match YouTube video ID
    pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    match = re.match(pattern, url)
    if match:
        return match.group(6)
    return None

def get_youtube_thumbnail(video_url):
    video_id = get_youtube_video_id(video_url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    return None

class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    url = models.URLField()

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='vigetRegion', null=True)

    def save(self, *args, **kwargs):
        if not self.thumbnail_url:
            self.thumbnail_url = get_youtube_thumbnail(self.youtube_url)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):
    e_name = models.CharField(max_length=255)
    e_details = RichTextField()
    open_date = models.DateField()
    close_date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='egetRegion', null=True)
    @property
    def status(self):
        today = timezone.now().date()  # Get the current date (without time)
        
        if today > self.close_date:
            return "Closed"
        elif today < self.open_date:
            return "Upcoming"
        else:
            return "Ongoing"
            
    def __str__(self):
        return self.e_name

class Activiti(models.Model):
    a_name = models.CharField(max_length=255)
    a_details = RichTextField()
    created_at = models.DateField(null=True)
    image = models.ImageField(upload_to='activity')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='agetRegion', null=True)
            
    def __str__(self):
        return self.a_name
    
    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (500, 375)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

class Project(models.Model):
    p_name = models.CharField(max_length=255)
    p_details = RichTextField()
    image = models.ImageField(upload_to='project')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='pgetRegion', null=True)
    created_at = models.DateField(null=True)        
    def __str__(self):
        return self.p_name
    
    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (500, 375)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

class Campaign(models.Model):
    c_name = models.CharField(max_length=255)
    c_details = RichTextField()
    image = models.ImageField(upload_to='campaign')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cgetRegion', null=True)
    created_at = models.DateField(null=True)
    def __str__(self):
        return self.c_name
    
    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (500, 375)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

class Rohingya(models.Model):
    r_name = models.CharField(max_length=255)
    r_details = RichTextField()
    image = models.ImageField(upload_to='rohingya')
    created_at = models.DateField(null=True)            
    def __str__(self):
        return self.r_name
    
    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (500, 375)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

class LegalDocument(models.Model):
    l_title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='legal_documents')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='lgetRegion', null=True)
            
    def __str__(self):
        return self.l_title
    
    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (500, 375)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

class Blog(models.Model):
    b_name = models.CharField(max_length=255)
    b_details = RichTextField()
    image = models.ImageField(upload_to='project')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='bgetRegion', null=True)
    created_at = models.DateField(null=True)            
    def __str__(self):
        return self.b_name
    
    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (500, 375)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)
    
class Volunteer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='volunteer', default='event_reg/default.jpg')
    email = models.EmailField()
    nid = models.CharField(blank=True, null=True, max_length=255)
    mobile = models.CharField(max_length=255)
    facebook_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='vgetRegion', null=True)
    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (300, 225)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class GoverningBodie(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gb')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='ggetRegion', null=True)

    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (300, 225)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Advisor(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gb')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='adgetRegion', null=True)

    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (300, 225)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ShariahAdvisor(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gb')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='sadgetRegion', null=True)

    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (300, 225)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Mission(models.Model):
    title = models.CharField(max_length=255)
    details = RichTextField()
    image = models.ImageField(upload_to='mision')
    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (300, 225)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Awards(models.Model):
    name = models.CharField(max_length=255)
    details = RichTextField()
    image = models.ImageField(upload_to='gb')

    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (300, 225)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reg_event')
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    address = models.TextField()
    image = models.ImageField(upload_to='event_reg', default='event_reg/default.jpg')
    email = models.EmailField()
    nid = models.CharField(blank=True, null=True, max_length=255)
    mobile = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        img = PilImage.open(self.image)
        output_size = (300, 225)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.image.save(self.image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Image(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_image')
    event_image = models.ImageField(upload_to='event')    
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_banner = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        img = PilImage.open(self.event_image)
        output_size = (500, 375)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.event_image.name.lower().endswith('.jpg') or self.event_image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.event_image.save(self.event_image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.event.e_name}"
    
    
class Setting(models.Model):
    region = models.OneToOneField(Region, related_name='language', on_delete=models.DO_NOTHING)
    main_image = models.ImageField(upload_to='home_image')
    services = models.TextField()
    video_file = models.FileField(upload_to='videos/', null=True)
    main_title = models.CharField(max_length=255)
    a_name = models.CharField(max_length=255, null=True)
    e_name = models.CharField(max_length=255)
    watch_list = models.CharField(max_length=255)
    v_name = models.CharField(max_length=255)
    donation_name = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    service_details = models.TextField()
    def __str__(self):
        return f"Settings for {self.region.name}"
    
    def save(self, *args, **kwargs):
        img = PilImage.open(self.main_image)
        output_size = (1000, 636)
        img = img.resize(output_size)
        buffer = BytesIO()
        img_format = 'JPEG' if self.main_image.name.lower().endswith('.jpg') or self.main_image.name.lower().endswith('.jpeg') else 'PNG'
        img.save(buffer, format=img_format, quality=70)
        self.main_image.save(self.main_image.name, File(buffer), save=False)
        super().save(*args, **kwargs)

class Contact(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField()
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    