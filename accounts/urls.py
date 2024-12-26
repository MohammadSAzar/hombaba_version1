from django.urls import path, re_path

from . import views

urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('verification/', views.verification_view, name='verification'),
    path('profile/', views.profile_info_now_view, name='profile_info_now'),
    path('info_auth/', views.profile_info_auth_view, name='profile_info_auth'),
    path('info_edit/', views.profile_info_edit_view, name='profile_info_edit'),
    path('your_services/', views.profile_your_services_view, name='profile_your_services'),
]

