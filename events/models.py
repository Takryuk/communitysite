import datetime
from django.db import models

# from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFill

from group.models import Group, GroupPrefecture
from users.models import CustomUser, Profile





class Event(models.Model):
    posted_group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='投稿グループ')
    title = models.CharField(max_length=60, verbose_name='タイトル')
    content = models.CharField(max_length=1000, verbose_name='本文')
    posted_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日')
    prefecture = models.ManyToManyField(GroupPrefecture, verbose_name='都道府県')
    detail_place = models.CharField(max_length=200, verbose_name='活動場所')
    event_day = models.DateField(verbose_name='開催日')
    event_end_day = models.DateField(null=True, blank=True, default='')
    time_description = models.CharField(max_length=200,default='', null=True, blank=True, verbose_name='開催時間・予定日の補足情報')
    joinned_user = models.ManyToManyField(Profile, verbose_name='参加者', blank=True)


    image1 = models.ImageField(
        upload_to="group_event_image1/%y/%m/%d/",
        verbose_name='イベント画像1枚目',
        null=True,
        blank=True,
    )
    # thumbnail1 = ImageSpecField(source='image1',
    #                             processors=[ResizeToFill(800, 800)],
    #                             format="JPEG",
    #                             # options={'quality': 60}
    #                             )

    image2 = models.ImageField(
        upload_to="group_event_image2/%y/%m/%d/",
        null=True,
        blank=True,
        verbose_name='イベント画像2枚目',
    )
    # thumbnail2 = ImageSpecField(source='image2',
    #                             processors=[ResizeToFill(500, 500)],
    #                             format="JPEG",
    #                             # options={'quality': 60}
    #                             )

    image3 = models.ImageField(
        upload_to="group_event_image3/%y/%m/%d/",
        null=True,
        blank=True,
        verbose_name='イベント画像3枚目',
    )
    # thumbnail3 = ImageSpecField(source='image3',
    #                             processors=[ResizeToFill(500, 500)],
    #                             format="JPEG",
    #                             # options={'quality': 60}
    #                             )

    def __str__(self):
        return self.title

class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='紐付く投稿')
    comment = models.CharField(max_length=200, verbose_name='コメント')
    commented_at = models.DateTimeField(auto_now_add=True, verbose_name='コメント日')
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name='ユーザー',
    )

    def __str__(self):
        return self.comment

class EventCommentMessage(models.Model):
    administrator = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='管理者')
    has_read = models.BooleanField(default=False, verbose_name='既読')
    comment = models.ForeignKey(EventComment, on_delete=models.CASCADE, verbose_name='コメント')


    def __str__(self):
        return str(self.comment) + ' for ' + str(self.administrator)
