from django.urls import path

from . import views

urlpatterns = [
    # Counseling URLs
    path('counseling/', views.counseling_view, name='counseling'),
    path('counseling/registration', views.counseling_registration_view, name='counseling_registration'),
    path('counseling/verification', views.counseling_verification_view, name='counseling_verification'),
    path('counseling_detail/<int:pk>/', views.counseling_detail, name='counseling_detail'),
    # Session URLs
    path('session/', views.session_view, name='session'),
    path('session/registration', views.session_registration_view, name='session_registration'),
    path('session/verification', views.session_verification_view, name='session_verification'),
    path('session_detail/<int:pk>/', views.session_detail, name='session_detail'),
    # Visit URLs
    path('visit/', views.visit_view, name='visit'),
    path('visit/registration', views.visit_registration_view, name='visit_registration'),
    path('visit/verification', views.visit_verification_view, name='visit_verification'),
    path('visit_detail/<int:pk>/', views.visit_detail, name='visit_detail'),
]


