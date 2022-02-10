from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404

from users.models import Profile

from group.models import Group

class GroupPkRequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        return profile_user in group.administrator.all()



class RequestUserIsInTheGroup(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        return profile_user in group.member.all()


class RequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return profile_user in group.administrator.all()
