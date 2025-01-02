from django.urls import path, include
from .views import *
from .forms import *
from django.contrib.auth import views
urlpatterns = [
    path('', hoshomeview, name='hoshome'),
    path('about/', aboutview, name='habout'),
    path('mission/', missionview, name='hmission'),
    path('facilities/', facilitiesview, name='hfacilities'),
    path('hcontact/', hcontactview, name='hcontact'),
    path('hactivities/', hactivitiesview, name='hactivities'),
    path('doctors/', hdoctorview, name='hdoctors'),
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('editprofile/', EditProfileview.as_view(), name="editprofile"),
    path('seeprofile/', seeprofile, name="seeprofile"),
    path('passwordchange/', views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm), name='passwordchange'),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name="password_change_done"),
    
    path('passwordchange/', views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm), name='passwordchange'),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name="password_change_done"),
    path("password_reset/", views.PasswordResetView.as_view(template_name='passwordreset.html', form_class=MyPasswordResetForm), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(template_name='passwordresetdone.html'),name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(template_name='passwordresetconfirm.html', form_class=MySetPasswordForm),name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(template_name='passwordresetcomplete.html'),
        name="password_reset_complete"),
]