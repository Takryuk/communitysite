from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404

from users.models import Profile

from group.models import Group
from .models import Blog, BlogComment


class RequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return profile_user in group.administrator.all()


class PostCommentPkRequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        comment = get_object_or_404(BlogComment, pk=self.kwargs['postcomment_pk'])
        adminisrators = comment.post.posted_group.administrator.all()
        return profile_user in adminisrators


class PostPkRequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        try:
            post_pk = self.kwargs['post_pk']
        except KeyError:
            post_pk = self.kwargs['pk']
        post = get_object_or_404(Blog, pk=post_pk)
        adminisrators = post.posted_group.administrator.all()
        return profile_user in adminisrators

# class PostPost_PkRequestUserIsAdministrator(UserPassesTestMixin):
#
#     def test_func(self):
#         profile_user = Profile.objects.get(user=self.request.user)
#
#         post = get_object_or_404(Blog, pk=self.kwargs['post_pk'])
#         adminisrators = post.posted_group.administrator.all()
#         return profile_user in adminisrators


class GroupPkRequestUserIsAdministrator(UserPassesTestMixin):

    def test_func(self):
        profile_user = Profile.objects.get(user=self.request.user)
        group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
        return profile_user in group.administrator.all()


# class GroupGroup_PkRequestUserIsAdministrator(UserPassesTestMixin):
#
#     def test_func(self):
#         profile_user = Profile.objects.get(user=self.request.user)
#         group = get_object_or_404(Group, pk=self.kwargs['group_pk'])
#         return profile_user in group.administrator.all()
#
