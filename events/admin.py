from django.contrib import admin

# Register your models here.
from .models import Event, EventComment, EventCommentMessage

admin.site.register(Event)
admin.site.register(EventComment)
admin.site.register(EventCommentMessage)