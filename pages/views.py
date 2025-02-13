from django.shortcuts import render

from blog.models import Blog
from accounts.models import Task


def home_view(request):
    context = {}
    blogs = Blog.objects.select_related('blog_category').filter(status='pub').order_by('-date_creation')[:6]
    tasks = Task.objects.select_related('task_counseling').select_related('task_session').select_related('task_visit').order_by('-datetime_created')[:6]
    context['blogs'] = blogs
    context['tasks'] = tasks
    return render(request, 'pages/home.html', context)


# def four_o_four_view(request):
#     return render(request, 'pages/404.html')


def contact_view(request):
    return render(request, 'pages/contact.html')


def about_view(request):
    return render(request, 'pages/about.html')


def rules_view(request):
    return render(request, 'pages/rules.html')


def faq_view(request):
    return render(request, 'pages/faq.html')

