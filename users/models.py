from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFill

class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('メールアドレス'), unique=True)
    # username = models.CharField(max_length=30, verbose_name='ニックネーム')
    user_name = models.CharField(max_length=30, verbose_name='ニックネーム')
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('入会日'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')



    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email




SEX_CHOICES = (
    ('M', '男性'),
    ('F', '女性'),
    ('X', '第3の性'),
    ('N/A', '回答しない')

)

class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='profile_set',
    )
    origin = models.ImageField(
        upload_to="profile_image/%y/%m/%d/",
        null=True,
        blank=True,
        verbose_name='プロフィール画像',
        width_field=''
    )
    # thumbnail = ImageSpecField(source='origin',
    #                            processors=[ResizeToFill(800, 800)],
    #                            format="JPEG",
    #                            # options={'quality': 60}
    #                            )
    profile = models.CharField(
        max_length=500,
        verbose_name='プロフィール',
        null=True,
        blank=True,
        default='',
    )
    sex = models.CharField(max_length=3, choices=SEX_CHOICES, verbose_name='性別', default=None)
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='年齢')
    twitter_link = models.URLField(null=True, blank=True, default='', verbose_name='Twitterアカウントのリンク')
    facebook_link = models.URLField(null=True, blank=True, default='', verbose_name='Facebookアカウントリンク')
    instagram_link = models.URLField(null=True, blank=True, default='', verbose_name='Instagramアカウントのリンク')

    def __str__(self):
        return str(self.user)

