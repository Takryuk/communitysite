from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
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

def only_request_pk_user(view):
  def _wrapped_view(request,pk, *args, **kwargs):
      request_user_profile = get_object_or_404(Profile, pk=request.user.pk)
      url_pk_user_profile =get_object_or_404(Profile, pk=pk)
      if request_user_profile == url_pk_user_profile or request.user.is_superuser:
          return view(request,pk , *args, **kwargs)
      else: HttpResponseForbidden()
  return _wrapped_view


def only_request_user_pk_user(view):
  def _wrapped_view(request,user_pk, *args, **kwargs):
      request_user_profile = get_object_or_404(Profile, pk=request.user.pk)
      url_pk_user_profile = get_object_or_404(Profile, pk=user_pk)
      if request.user.pk == user_pk or request.user.is_superuser:
          return view(request,user_pk , *args, **kwargs)
      else: HttpResponseForbidden()
  return _wrapped_view
