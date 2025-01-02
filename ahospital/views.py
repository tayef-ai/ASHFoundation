from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

def hoshomeview(request):
    query = HActiviti.objects.all().order_by('-created_at')
    return render(request, 'hhome.html', {'query': query})

def aboutview(request):
    return render(request, 'about.html')

def missionview(request):
    return render(request, 'hmission.html')

def facilitiesview(request):
    return render(request, 'facilities.html')

def hcontactview(request):
    return render(request, 'hcontact.html')

def hdoctorview(request):
    return render(request, 'doctors.html')

def hactivitiesview(request):
    query = HActiviti.objects.all().order_by('-created_at')
    return render(request, 'hactivities.html', {'query': query})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'register.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        print("==============================", form)
        if form.is_valid():
            messages.success(request, "Congratulations!! Registration Successful.")
            form.save()
            form = CustomerRegistrationForm()
            return redirect('/hospital/login/')
        else:
            # messages.warning(request, "Your Registration is not Completed!! Please try again.")
            return render(request, 'register.html', {'form': form})
        
    
@login_required    
def seeprofile(request):
    return render(request, 'profile.html')


@method_decorator(login_required, name='dispatch')
class EditProfileview(View):
    def get(self, request):
        customer = get_object_or_404(Customer, user=request.user)  # Fetch the Customer instance
        initial_data = {
            'role': customer.role,
            'name': customer.name,
            'dob': customer.dob,
            'address': customer.address,
            'phone': customer.phone,
            'email': request.user.email,  # Get email from User model
        }
        form = CustomerProfileForm(instance=request.user, initial=initial_data)
        return render(request, 'editprofile.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('seeprofile')  # Redirect to the profile page after saving
        else:
            messages.error(request, "There was an error updating your profile.")
        return render(request, 'editprofile.html', {'form': form})