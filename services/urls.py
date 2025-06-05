from django.urls import path

from . import views


urlpatterns = [
    path('load_cities/', views.load_cities, name='load_cities'),
    path('load_districts/', views.load_districts, name='load_districts'),
    path('get-cities/', views.load_cities_list, name='load_cities_list'),
    path('get-districts/', views.load_districts_list, name='load_districts_list'),
    # Counseling URLs
    path('counseling/', views.counseling_view, name='counseling'),
    path('counseling/registration', views.counseling_registration_view, name='counseling_registration'),
    path('counseling/verification', views.counseling_verification_view, name='counseling_verification'),
    path('counseling_detail/<int:pk>/<str:code>/', views.counseling_detail, name='counseling_detail'),
    # Session URLs
    path('session/', views.session_view, name='session'),
    path('session/registration', views.session_registration_view, name='session_registration'),
    path('session/verification', views.session_verification_view, name='session_verification'),
    path('session_detail/<int:pk>/<str:code>/', views.session_detail, name='session_detail'),
    # Visit URLs
    path('visit/', views.visit_view, name='visit'),
    path('visit/registration', views.visit_registration_view, name='visit_registration'),
    path('visit/verification', views.visit_verification_view, name='visit_verification'),
    path('visit_detail/<int:pk>/<str:code>/', views.visit_detail, name='visit_detail'),
]


