from django.urls import path, re_path, include

from . import views


urlpatterns = [
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    re_path(r'^blog/(?P<slug>[-\w]+)/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog-category/homebia/', views.blog_category_hombaba, name='category_hombaba'),
    path('blog-category/educational/', views.blog_category_educational, name='category_educational'),
    path('blog-category/analytical/', views.blog_category_analytical, name='category_analytical'),
    path('blog-category/news/', views.blog_category_news, name='category_news'),
]

