from django.contrib import admin

# Register your models here.

from .models import (
    Group,
    GroupPrefecture,
    GroupGeneration,
    GroupCategory,
    # Group10,
)



# class GroupAdmin(admin.ModelAdmin):
#     fields = [
#         'name',
#         'subtitle',
#         'activity_description',
#         'mood',
#         'welcome_person',
#         'number_of_members',
#         'sex_ratio',
#         'max_age',
#         'min_age',
#         'cost',
#         'day',
#         'generation',
#         'category',
#         'last_comment',
#         'detail_place',
#         'founded_date',
#         'prefecture',
#         'image1',
#         'image2',
#         'image3',
#         'administrator'
#     ]




admin.site.register(Group)
# admin.site.register(Blog)
admin.site.register(GroupGeneration)
admin.site.register(GroupPrefecture)
admin.site.register(GroupCategory)
