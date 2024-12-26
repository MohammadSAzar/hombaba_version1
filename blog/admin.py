from django.contrib import admin
# from jalali_date.admin import ModelAdminJalaliMixin
from .models import Blog, BlogCategory, Comment, Reply

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [
    #     ReviewInProductInline,
    # ]

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'blog_category', 'date_creation', 'date_modification')
    ordering = ('-date_creation', )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'name', 'body', 'date_creation')
    ordering = ('-date_creation',)


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('blog', 'reply_name', 'body', 'parent_comment', 'parent_reply', 'date_creation')
    ordering = ('-date_creation',)

