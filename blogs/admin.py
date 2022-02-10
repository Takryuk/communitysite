from django.contrib import admin

# Register your models here.
from .models import Blog, BlogComment, BlogCommentMessage

admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(BlogCommentMessage)