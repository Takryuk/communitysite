from django.contrib import admin

# Register your models here.
from .models import (
    GroupApplyMessage,
    InnerGroupMessage,
    HasReadEventMessage,
    HasReadInnerGroupMessage,
    EventMessage,
    AdminMessage,
    EventJoinedMessage,
    ApplyAdministratorMessage,
)


class CustomAdminMessage(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'sent_at', 'has_read')

admin.site.register(GroupApplyMessage)
admin.site.register(InnerGroupMessage)
admin.site.register(HasReadEventMessage)
admin.site.register(HasReadInnerGroupMessage)
admin.site.register(EventJoinedMessage)
admin.site.register(EventMessage)
admin.site.register(ApplyAdministratorMessage)
admin.site.register(AdminMessage, CustomAdminMessage)