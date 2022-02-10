from django.shortcuts import render, redirect, reverse, get_object_or_404
from django import template


from users.models import Profile
from blogs.models import BlogCommentMessage
register = template.Library()


@register.simple_tag
def has_read(request, comment):
    user = get_object_or_404(Profile, user=request.user)
    try:
        comment_message =comment.blogcommentmessage_set.get(administrator=user)
    except BlogCommentMessage.DoesNotExist:
        return ''
    try:
        if comment_message.has_read:
            return ''
        else:
            comment_message.has_read = True
            comment_message.save()
            return '<small>未読</small>   '
    except UnboundLocalError:
        pass
