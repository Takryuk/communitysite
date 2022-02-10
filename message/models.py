from django.db import models

from users.models import Profile
from group.models import Group
from events.models import Event
# Create your models here.

class GroupApplyMessage(models.Model):
    administrator = models.ForeignKey(Profile,related_name='apply_receiver', on_delete=models.CASCADE, verbose_name='管理者')
    has_read = models.BooleanField(default=False, verbose_name='既読')
    applied_user = models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, verbose_name='応募者')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True,related_name='applied_message', verbose_name='応募したグループ')
    sent_at = models.DateTimeField(auto_now=True)

class InnerGroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='sender', verbose_name='投稿グループ')
    sent_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name='タイトル')
    content = models.CharField(max_length=500, verbose_name='内容')


    def __str__(self):
        return str(self.group) + '　' + self.content[:20]


class HasReadInnerGroupMessage(models.Model):
    group_message = models.ForeignKey(InnerGroupMessage, on_delete=models.CASCADE, verbose_name='グループ内メッセージ')
    has_read = models.BooleanField(default=False, verbose_name='既読')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='受取人')

    def __str__(self):
        return str(self.group_message) + '  to ' + str(self.user)


# class GroupApproveMessage(models.Model):
#     administrator = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='投稿者')
#     has_read = models.BooleanField(default=False, verbose_name='既読')
#     group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='承認グループ')

class EventMessage(models.Model):
    administrator = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='送信者')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='紐付くイベント')
    title = models.CharField(max_length=100, verbose_name='タイトル')
    content = models.CharField(max_length=500, verbose_name='内容')
    sent_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.event) + '  ' + self.content[:20]


class HasReadEventMessage(models.Model):
    event_message = models.ForeignKey(EventMessage, on_delete=models.CASCADE, verbose_name='イベントメッセージ')
    has_read = models.BooleanField(default=False, verbose_name='既読')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='受取人')

    def __str__(self):
        return str(self.event_message)[:20] + '  ' + str(self.user)


class AdminMessage(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='受取人')
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    sent_at = models.DateTimeField(auto_now=True)
    has_read = models.BooleanField(default=False, verbose_name='既読')

    def __str__(self):
        return self.content + '  to  ' + str(self.user)


class EventJoinedMessage(models.Model):
    administrator = models.ForeignKey(Profile,related_name='event_apply_receiver', on_delete=models.CASCADE, verbose_name='管理者')
    has_read = models.BooleanField(default=False, verbose_name='既読')
    applied_user = models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, verbose_name='応募者')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, verbose_name='応募したイベント')
    joined_at = models.DateTimeField(auto_now=True)


class ApplyAdministratorMessage(models.Model):
    administrator = models.ForeignKey(Profile,on_delete=models.SET_DEFAULT,default='脱退した管理者', related_name='applied_administrator', verbose_name='管理者')
    user = models.ForeignKey(Profile,related_name='asked_user', on_delete=models.CASCADE, verbose_name='受取人')
    group = models.ForeignKey(Group,on_delete=models.CASCADE, verbose_name='管理者となるグループ')
    reason = models.CharField(max_length=200, verbose_name='申請理由', default='', null=True, blank=True)
    has_read = models.BooleanField(default=False, verbose_name='既読')
    sent_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'from' + str(self.administrator) + 'to' + str(self.user) + 'for' + str(self.group)
