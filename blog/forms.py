from django import forms
from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {'body': forms.Textarea()}

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_name', 'body', 'parent_comment', 'parent_reply']
        widgets = {'body': forms.Textarea()}

