from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('404/', views.four_o_four_view, name='404'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('rules/', views.rules_view, name='rules'),
    path('faq/', views.faq_view, name='faq'),
]



