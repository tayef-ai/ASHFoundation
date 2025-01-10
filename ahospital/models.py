from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from ckeditor.fields import RichTextField
from PIL import Image as PilImage
from io import BytesIO
from django.core.files import File
from aashfApp.models import Event

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name = name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

STATUS = (
    ('Patient', 'রোগী'),
    ('Doctor', 'ডাক্তার'),
)
SEX = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
class Customer(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='see_user')
    name = models.CharField(max_length=255)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    role = models.CharField(default='Patient', choices=STATUS, max_length=100)
    gender = models.CharField(choices=SEX, max_length=100)
    def __str__(self):
        return self.user.email
    
class HActiviti(models.Model):
    a_name = models.CharField(max_length=255)
    a_details = RichTextField()
    created_at = models.DateField(null=True)
    image = models.ImageField(upload_to='hospital_activity')
            
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

class Doctor(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="doctor_cus")
    degree = models.CharField(max_length=100, verbose_name="Designation")
    specialization = models.CharField(max_length=100, verbose_name="Specialization")
    
    def __str__(self):
        return f"{self.customer.name} - {self.specialization}"

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availabilities")
    day = models.CharField(
        max_length=20, 
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday')
        ],
        verbose_name="Day"
    )
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")

    def __str__(self):
        return f"{self.doctor.customer.name} - {self.day} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = "Availability"
        verbose_name_plural = "Availabilities"
        ordering = ['doctor', 'day', 'start_time']
    
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    patient = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateField(verbose_name="Appointment Date")
    appointment_time = models.TimeField(verbose_name="Appointment Time")
    notes = models.TextField(verbose_name="Doctor Notes", blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.patient.name} with {self.doctor.customer.name} on {self.appointment_date} at {self.appointment_time}"
    
class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="prescription")
    prescribed_date = models.DateTimeField(auto_now_add=True, verbose_name="Prescribed Date")
    medications = models.TextField(verbose_name="Medications")
    instructions = models.TextField(verbose_name="Instructions", blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.name} by {self.appointment.doctor.customer.name}"

app_groom=(('মামা/চাচা/খালু', 'মামা/চাচা/খালু'), ('মামী/চাচী/খালা', 'মামী/চাচী/খালা'), ('ফুফু/ফুফা', 'ফুফু/ফুফা'), ('অন্যান্য', 'অন্যান্য'))
app_bride=(('মামা/চাচা/খালু', 'মামা/চাচা/খালু'), ('মামী/চাচী/খালা', 'মামী/চাচী/খালা'), ('ফুফু/ফুফা', 'ফুফু/ফুফা'), ('অন্যান্য', 'অন্যান্য'))
class NikahRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='nikah_reg_event')
    email = models.EmailField(null=True, blank=True, verbose_name="ইমেইল")
    groom_name = models.CharField(max_length=255, verbose_name="বরের পুরো নাম (জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন অনুযায়ী) লিখুন")
    groom_present_address = models.TextField(verbose_name="বরের বর্তমান ঠিকানা (জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন অনুযায়ী) লিখুন")
    groom_permanent_address = models.TextField(verbose_name="বরের স্থায়ী ঠিকানা (জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন অনুযায়ী) লিখুন")
    groom_occupation = models.TextField(verbose_name="বরের পেশা (পদবীসহ প্রতিষ্ঠানের নাম, ঠিকানা)")
    groom_education = models.CharField(max_length=255, verbose_name="বরের সর্বোচ্চ শিক্ষাগত যোগ্যতা")
    groom_nid = models.CharField(max_length=255, verbose_name="বরের জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন নম্বর")
    groom_mobile = models.CharField(max_length=255, verbose_name="বরের মোবাইল নম্বর")
    groom_alternate_mobile = models.CharField(max_length=255, blank=True, null=True, verbose_name="বরের বিকল্প মোবাইল নম্বর (যদি থাকে)")
    groom_father = models.CharField(max_length=255, verbose_name="বরের পিতার নাম (জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন অনুযায়ী) লিখুন")
    groom_father_mobile = models.CharField(max_length=255, verbose_name="বরের পিতা/মাতার মোবাইল নম্বর")
    bride_name = models.CharField(max_length=255, verbose_name="কনের পুরো নাম (জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন অনুযায়ী) লিখুন")
    bride_present_address = models.TextField(verbose_name="কনের বর্তমান ঠিকানা (জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন অনুযায়ী) লিখুন")
    bride_permanent_address = models.TextField(verbose_name="কনের স্থায়ী ঠিকানা (জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন অনুযায়ী) লিখুন")
    bride_occupation = models.TextField(verbose_name="কনের পেশা (চাকুরিরত হলে, প্রতিষ্ঠানের নাম, ঠিকানা)")
    bride_education = models.CharField(max_length=255, verbose_name="কনের সর্বোচ্চ শিক্ষাগত যোগ্যতা")
    bride_nid = models.CharField(max_length=255, verbose_name="কনের জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন নম্বর")
    bride_mobile = models.CharField(max_length=255, verbose_name="কনের মোবাইল নম্বর")
    bride_alternate_mobile = models.CharField(max_length=255, blank=True, null=True, verbose_name="কনের বিকল্প মোবাইল নম্বর (যদি থাকে)")
    bride_father = models.CharField(max_length=255, verbose_name="কনের পিতা/অভিভাবকের নাম (জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন অনুযায়ী) লিখুন")
    bride_father_mobile = models.CharField(max_length=255, verbose_name="কনের পিতা/মাতার মোবাইল নম্বর")
    applicant_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="আবেদনকারীর নাম (বর/কনের পক্ষে অন্য কেউ আবেদনকারী হলে)")
    applicant_mobile = models.CharField(max_length=255, blank=True, null=True, verbose_name="আবেদনকারীর মোবাইল নম্বর")
    applicant_groom = models.CharField(choices=app_groom, max_length=255, blank=True, null=True, verbose_name="আবেদনকারীর সাথে বরের সম্পর্ক কী? বর নিজে আবেদনকারী হলে এ প্রশ্ন এড়িয়ে চলুন")
    applicant_bride = models.CharField(choices=app_bride, max_length=255, blank=True, null=True, verbose_name="আবেদনকারীর সাথে কনের সম্পর্ক কী? কনে নিজে আবেদনকারী হলে এ প্রশ্ন এড়িয়ে চলুন")
    groom_image = models.ImageField(upload_to='event_groom', verbose_name="বরের ছবি (সদ্য তোলা পাসপোর্ট সাইজের ছবি, কোন সেলফি গ্রহণযোগ্য হবে না)")
    bride_image = models.ImageField(upload_to='event_bride', verbose_name="কনের ছবি (সদ্য তোলা পাসপোর্ট সাইজের ছবি, কোন সেলফি গ্রহণযোগ্য হবে না)")

    def __str__(self):
        return self.groom_name
    