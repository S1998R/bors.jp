from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
import hashlib
import uuid

# ↓ここから追記開始↓
from json import JSONEncoder
from uuid import UUID

JSONEncoder_olddefault = JSONEncoder.default


def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)


JSONEncoder.default = JSONEncoder_newdefault
# ↑追記はここまで↑


def _user_profile_avator_upload_to(instance, filename):
    filename = 'png'  # png形式で保存する
    current_time = datetime.datetime.now()
    pre_hash_name = '%s%s%s' % (instance.email, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'images/'

    return '%s%s' % (saved_path, hs_filename)


class Initial(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    initial = models.CharField('あ行～わ行', null=True, max_length=255)

    def __str__(self):
        return self.initial


class University(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    university = models.CharField('大学', null=True, max_length=255)
    initial = models.ForeignKey(Initial, verbose_name='あ行～わ行', null=True, on_delete=models.PROTECT)
    email_domain = models.CharField('メールアドレスのドメイン', null=True, max_length=255)

    def __str__(self):
        return self.university


class Faculty(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, null=True, on_delete=models.PROTECT)
    faculty = models.CharField('学部', null=True, max_length=255, blank=True)
    initial = models.CharField('学部の最初の文字', null=True, max_length=255, blank=True)

    def __str__(self):
        return self.faculty


class Department(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, null=True, on_delete=models.PROTECT)
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.PROTECT)
    department = models.CharField('学科', null=True, max_length=255, blank=True)
    initial = models.CharField('学科の最初の文字', null=True, max_length=255, blank=True)

    def __str__(self):
        return self.department


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    class Meta:
        verbose_name_plural = 'CustomUser'
        db_table = 'custom_user'

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(verbose_name='プロフィール画像', blank=True, null=True, upload_to=_user_profile_avator_upload_to)
    university = models.CharField(verbose_name='大学', blank=False, max_length=100)
    profile = models.CharField(verbose_name='プロフィール', max_length=10000, null=True, default='よろしくお願いします！')
    stripe_account_id = models.CharField(verbose_name='stripeアカウントid', max_length=10000, null=True, blank=True)
    special_user_status = models.BooleanField(verbose_name='特別なユーザーか否か', null=True, blank=True)  # Trueで特別なユーザー
    email_permission = models.BooleanField(verbose_name='運営からのメールを受け取るか否か', null=True, blank=True, default=True)  # Trueで受け取る
    free_sell_right = models.BooleanField(verbose_name='無料で出品できる権利（Trueで権利あり）', null=True, blank=True, default=True)
