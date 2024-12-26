from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django_quill.fields import QuillField


class BlogCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Category title'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(BlogCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_category', args=[self.title])


class Blog(models.Model):
    STATUS_CHOICES = (('pub', 'Published'), ('drf', 'Draft'))
    cover = models.ImageField(upload_to='blogs/covers/', verbose_name=_('Blog cover'))
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name='blog_category', verbose_name=_('Blog category'))
    title = models.CharField(max_length=200, verbose_name=_('Blog title'))
    body = QuillField(verbose_name=_('Blog body'))
    date_creation = models.DateField(auto_now_add=True, verbose_name=_('Datetime of creation'))
    date_modification = models.DateField(auto_now=True, verbose_name=_('Datetime of modification'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, verbose_name=_('Blog status'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date_creation',)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])


comment_statuses = [
    ('acc', _('Accepted')),
    ('rej', _('Rejected')),
    ('wit', _('Waiting')),
]


class Comment(models.Model):
    COMMENT_STATUSES = comment_statuses
    name = models.CharField(max_length=40, verbose_name=_('Comment Name'))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=500, verbose_name=_('Comment Text'))
    status = models.CharField(max_length=30, choices=COMMENT_STATUSES, default='wit', verbose_name=_('Status'), blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} : {self.body[:30]}'

    class Meta:
        ordering = ['-date_creation']


class Reply(models.Model):
    COMMENT_STATUSES = comment_statuses
    reply_name = models.CharField(max_length=40, verbose_name=_('Reply Name'))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_replies', blank=True, null=True)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    parent_reply = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name="replies_pr", null=True, blank=True)
    body = models.CharField(max_length=500, verbose_name=_('Reply Text'))
    status = models.CharField(max_length=30, choices=COMMENT_STATUSES, default='wit', verbose_name=_('Status'), blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reply_name} : {self.body[:30]}'

    class Meta:
        ordering = ['date_creation']

