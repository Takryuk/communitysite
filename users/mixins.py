from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from .models import Profile, CustomUser

class GetRequestUseIdrMixin(object):



    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            request_user_id = self.request.user.id
            try:
                profile_user_id = CustomUser.objects.get(id=request_user_id).profile_set.id
                context['profile_user_id'] = profile_user_id
            except:
                pass
        return context


def get_user_id(request, **kwargs):
    context ={}
    if request.user.is_authenticated:
        request_user_pk = request.user.pk
        try:
            profile_user_id = CustomUser.objects.get(id=request_user_pk).profile_set.id
            # profile_user_id = get_object_or_404(CustomUser, pk=request_user_pk).profile_set.id
            context={'profile_user_id':profile_user_id}
        except:
            pass


    return context

class RequestUserOnlyMixin(UserPassesTestMixin):

    def test_func(self):
        request_user = self.request.user
        request_profile_pk = self.kwargs['pk']
        request_profile_user = get_object_or_404(Profile, pk=request_profile_pk).user

        # request_profile_user = Profile.objects.get(id=request_profile_pk).user
        return request_profile_user == request_user or request_user.is_superuser

class SuperuserNotDisplayMixin(UserPassesTestMixin):

    def test_func(self):
        user_profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        if not self.request.user.is_superuser and user_profile.user.is_superuser:
            return False
        return True