from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Blog
from group.models import Group
from users.models import Profile, CustomUser

# def request_user_is_administrator(view):
#     def wrapper(request, pk, *args, **kwargs):
#         profile_user = get_object_or_404(Profile, user=request.user)
#         group = get_object_or_404(Group, pk=pk)
#         if profile_user in group.administrator.all():
#             return view(request, pk, *args, **kwargs)
#         else:
#             redirect('group:group_list')
#
#     return wrapper

