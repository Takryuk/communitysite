from django.db import models
from django.core.validators import MinLengthValidator

# from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFill

from users.models import Profile



CATEGORY_CHOICES = (
    ('1', 'スポーツ全般'),
    ('2', 'ランニング'),
    ('3', '野球'),
    ('4', 'サッカー'),
    ('5', 'テニス'),
    ('6', 'ソフトボール'),
    ('7', 'フットサル'),
    ('8', 'バスケットボール'),
    ('9', 'バレーボール'),
    ('10', 'バドミントン'),
    ('11', '卓球'),
    ('12', '登山'),
    ('13', 'ハイキング'),
    ('14', 'ダンス'),
    ('15', 'ヨガ・ピラティス'),
    ('16', 'ボルダリング'),
    ('17', 'ダーツ'),
    ('18', '筋トレ'),
    ('19', 'スキー'),
    ('20', 'スノーボード'),
    ('21', 'ゴルフ'),
    ('22', '水泳'),
    ('23', 'サーフィン'),
    ('24', 'ダイビング'),
    ('25', 'トライアスロン'),
    ('99', 'その他のスポーツ・アウトドア'),
    ('101', '飲み会'),
    ('102', '勉強会'),
    ('103', '芸術'),
    ('104', '散歩'),
    ('105', '料理'),
    ('106', 'グルメ'),
    ('107', '写真'),
    ('108', '映画'),
    ('109', '音楽'),
    ('110', 'ビジネス'),
    ('111', 'ゲーム'),
    ('112', '旅行'),
    ('113', '健康・ダイエット'),
    ('114', 'ボランティア'),
    ('115', '起業'),
    ('116', '釣り'),
    ('117', '手芸'),
    ('118', 'イベント'),
    ('119', 'その他の趣味'),
    ('201', '交流会'),
    ('202', '国際交流'),
    ('203', '企画'),
    ('204', 'その他の社会・交流'),
)

CATEGORY_SORT = (
    ('1', 'スポーツ・アウトドア'),
    ('2', '文化系'),
    ('3', '社会活動'),
)
class GroupCategory(models.Model):
    category = models.CharField(unique=True, max_length=100, choices=CATEGORY_CHOICES, verbose_name='カテゴリー')
    category_sort = models.CharField(max_length=100, choices=CATEGORY_SORT, default='1')




    def __str__(self):
        return self.get_category_display()

    # def get_category_name(self):
    #     return dict(CATEGORY_CHOICES)[self.category]


    # class Meta:
    #     ordering = ['-category']
    #     order_with_respect_to = ['-category']


GENERATION_CHOICES = (
    ('1', '学生'),
    ('2', '社会人'),
    ('3', 'シニア'),
)

class GroupGeneration(models.Model):
    generation = models.CharField(unique=True, max_length=100, choices=GENERATION_CHOICES, verbose_name='年代')

    def __str__(self):
        return self.get_generation_display()


PREFECTURE_CHOICES = (
    ('1', '北海道'),
    ('2', '青森県'),
    ('3', '岩手県'),
    ('4', '宮城県'),
    ('5', '秋田県'),
    ('6', '山形県'),
    ('7', '福島県'),
    ('8', '茨城県'),
    ('9', '栃木県'),
    ('10', '群馬県'),
    ('11', '埼玉県'),
    ('12', '千葉県'),
    ('13', '東京都'),
    ('14', '神奈川県'),
    ('15', '新潟県'),
    ('16', '富山県'),
    ('17', '石川県'),
    ('18', '福井県'),
    ('19', '山梨県'),
    ('20', '長野県'),
    ('21', '岐阜県'),
    ('22', '静岡県'),
    ('23', '愛知県'),
    ('24', '三重県'),
    ('25', '滋賀県'),
    ('26', '京都府'),
    ('27', '大阪府'),
    ('28', '兵庫県'),
    ('29', '奈良県'),
    ('30', '和歌山県'),
    ('31', '鳥取県'),
    ('32', '島根県'),
    ('33', '岡山県'),
    ('34', '広島県'),
    ('35', '山口県'),
    ('36', '徳島県'),
    ('37', '香川県'),
    ('38', '愛媛県'),
    ('39', '高知県'),
    ('40', '福岡県'),
    ('41', '佐賀県'),
    ('42', '長崎県'),
    ('43', '熊本県'),
    ('44', '大分県'),
    ('45', '宮崎県'),
    ('46', '鹿児島県'),
    ('47', '沖縄県'),
)

class GroupPrefecture(models.Model):
    prefecture =  models.CharField(unique=True, max_length=10, choices=PREFECTURE_CHOICES, verbose_name='都道府県')

    def __str__(self):
        return self.get_prefecture_display()




class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='グループ名', default='')
    subtitle = models.CharField(null=True, blank=True, default='', max_length=60, verbose_name='サブタイトル')
    activity_description = models.CharField(max_length=3000,default='', verbose_name='活動内容', validators=[MinLengthValidator])
    mood = models.CharField(max_length=500, null=True, blank=True, default='',  verbose_name='雰囲気')
    welcome_person = models.CharField(max_length=500, null=True, blank=True, default='', verbose_name='こんな人に来て欲しい')
    number_of_members = models.IntegerField(default=1, verbose_name='会員数')
    sex_ratio = models.CharField(null=True, blank=True, default='', max_length=300, verbose_name='ジェンダー比')
    max_age = models.PositiveIntegerField(null=True, blank=True, default=30)
    min_age = models.PositiveIntegerField(null=True, blank=True, default=30)
    cost = models.CharField(max_length=300, verbose_name='会費', default='')
    day = models.CharField(max_length=200, verbose_name='活動日・活動頻度', default='')
    generation = models.ManyToManyField(GroupGeneration, verbose_name='年代',  help_text='複数選択可')
    last_comment = models.CharField(null=True, blank=True, default='', max_length=100, verbose_name='最後に一言')
    category = models.ManyToManyField(GroupCategory, help_text='最大5個まで選択可')
    member = models.ManyToManyField(Profile, related_name='belonging_group')
    applied_user = models.ManyToManyField(Profile, related_name='applied_group', blank=True, default='なし')
    administrator = models.ManyToManyField(Profile, related_name='managing_group')
    before_administrator = models.ManyToManyField(Profile, related_name='before_administrator',blank=True)
    recruiting = models.BooleanField(default=True, verbose_name='メンバー募集')
    prefecture = models.ManyToManyField(GroupPrefecture, verbose_name='都道府県', help_text='最大5つまで選択可')
    detail_place = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name='詳細な活動場所')
    founded_date = models.DateField(null=True, blank=True, verbose_name='設立年')
    display = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False, verbose_name='承認済み')
    recruit_member = models.BooleanField(default=True, verbose_name='新規メンバー募集')

    image1 = models.ImageField(
            upload_to="group_profile_image1/%y/%m/%d/",
            verbose_name='グループトップ画像',
            default=''
        )
    # thumbnail1 = ImageSpecField(source='image1',
    #                            processors=[ResizeToFill(800, 800)],
    #                            format="JPEG",
    #                            # options={'quality': 60}
    #                            )


    image2 = models.ImageField(
        upload_to="group_profile_image2/%y/%m/%d/",
        null=True,
        blank=True,
        verbose_name='グループ画像2枚目',
    )
    # thumbnail2 = ImageSpecField(source='image2',
    #                            processors=[ResizeToFill(500, 500)],
    #                            format="JPEG",
    #                            # options={'quality': 60}
    #                            )


    image3 = models.ImageField(
        upload_to="group_profile_image3/%y/%m/%d/",
        null=True,
        blank=True,
        verbose_name='グループ画像3枚目',
    )
    # thumbnail3 = ImageSpecField(source='image3',
    #                            processors=[ResizeToFill(500, 500)],
    #                            format="JPEG",
    #                            # options={'quality': 60}
    #                            )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['-number_of_members'])
        ]
        ordering = ['-number_of_members']


# class GroupOrderByMembers(models.Model):
#     group = models.OneToOneField(Group, on_delete=models.CASCADE)