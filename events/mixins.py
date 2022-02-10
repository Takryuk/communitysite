from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404

from users.models import Profile

from group.models import Group
from .models import Event, EventComment




class EventCommentPkRequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        comment = get_object_or_404(EventComment, pk=self.kwargs['eventcomment_pk'])
        adminisrators = comment.event.posted_group.administrator.all()
        return profile_user in adminisrators


class EventPkRequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        try:
            event_pk = self.kwargs['event_pk']
        except KeyError:
            event_pk = self.kwargs['pk']
        event = get_object_or_404(Event, pk=event_pk)
        administrators = event.posted_group.administrator.all()
        return profile_user in administrators

# class EventEvent_PkRequestUserIsAdministrator(UserPassesTestMixin):
#
#     def test_func(self):
#         profile_user = Profile.objects.get(user=self.request.user)
#         # event = Event.objects.get(pk=self.kwargs['pk'])
#         event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
#         adminisrators = event.posted_group.administrator.all()
#         return profile_user in adminisrators


class GroupPkRequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        return profile_user in group.administrator.all()


class GroupGroup_PkRequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)

        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        return profile_user in group.administrator.all() or self.request.user.is_superuser

class RequestUserIsInTheEvent(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        return profile_user in event.joinned_user.all()

