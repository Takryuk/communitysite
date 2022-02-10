from django.shortcuts import render, redirect, reverse, get_object_or_404

from group.models import Group
from users.models import Profile, CustomUser


def get_user_profile_id(view):
  def _wrapped_view(request, *args, **kwargs):
      request_user_id = request.user.id
      context = {}
      try:
          profile_user_id = CustomUser.objects.get(id=request_user_id).profile_set.id
          context['profile_user_id'] = profile_user_id
      except:
          pass
      return view(request,context, *args, **kwargs)

  return _wrapped_view

def group_pk_request_user_is_administrator(view):
    def wrapper(request, *args, **kwargs):
        profile_user = get_object_or_404(Profile, user=request.user)
        group = get_object_or_404(Group, pk=kwargs['group_pk'])
        if profile_user in group.administrator.all():
            return view(request, *args, **kwargs)
        else:
            return redirect('group:group_list')

    return wrapper
