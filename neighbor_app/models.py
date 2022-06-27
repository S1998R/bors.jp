from django.db import models
from accounts.models import CustomUser, Faculty, Department
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
    pre_hash_name = '%s%s%s' % (instance.user.email, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'images/'

    return '%s%s' % (saved_path, hs_filename)


SELECTION1 = (
        ('textbook', '教科書'),
        ('other', 'その他'),
    )

SELECTION2 = (
        ('未使用', '未使用'),
        ('新品に近い', '新品に近い'),
        ('良い', '良い'),
        ('可', '可'),
)


class Merchandise(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, verbose_name='売り手のアカウント情報', on_delete=models.CASCADE, related_name="user")
    merchandise_name = models.CharField(verbose_name='商品名', max_length=300, null=True)
    image = models.ImageField(verbose_name='商品の画像', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_2 = models.ImageField(verbose_name='商品の画像2', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_3 = models.ImageField(verbose_name='商品の画像3', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_4 = models.ImageField(verbose_name='商品の画像4', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_5 = models.ImageField(verbose_name='商品の画像5', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_6 = models.ImageField(verbose_name='商品の画像6', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_7 = models.ImageField(verbose_name='商品の画像7', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_8 = models.ImageField(verbose_name='商品の画像8', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_9 = models.ImageField(verbose_name='商品の画像9', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    image_10 = models.ImageField(verbose_name='商品の画像10', upload_to=_user_profile_avator_upload_to, null=True, blank=True)
    value = models.IntegerField('商品の価格', blank=False)
    sell_commission = models.IntegerField('販売手数料', blank=True, null=True)
    explanation = models.CharField(verbose_name='商品説明', max_length=300)
    category = models.CharField(verbose_name='カテゴリ', max_length=300, blank=False, null=True, choices=SELECTION1)
    merchandise_status = models.CharField(verbose_name='商品の状態', max_length=300, blank=False, null=True, choices=SELECTION2)
    display_status = models.CharField(verbose_name='売れたか、出品を取りやめたか否か', max_length=300, blank=True, null=True)  # soldで売り切れ、stopで出品取りやめ、noneで売っている最中
    merchandise_buyer_id = models.CharField(verbose_name='購入者のid', max_length=300, blank=True, null=True)  # 要らないので後で消す。互換性を考えて一旦残してある。
    merchandise_buyer_account = models.ForeignKey(CustomUser, verbose_name='購入者のアカウント情報', on_delete=models.CASCADE, related_name="merchandise_buyer", blank=True, null=True)
    class_name = models.CharField(verbose_name='授業名（教科書の場合）', max_length=300, blank=True)
    region = models.CharField(verbose_name='受け渡し可能な場所', max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 出品した時刻
    updated_at = models.DateTimeField(auto_now=True)  # 編集・更新した時刻  .save()でしか自動更新されない
    faculty = models.ForeignKey(Faculty, verbose_name='学部', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, verbose_name='学科', on_delete=models.CASCADE, null=True, blank=True)
    charge_id = models.CharField(verbose_name='payjpのchargeのid', max_length=300, blank=True, null=True)
    first_sell = models.BooleanField(verbose_name='ユーザーの最初の出品かどうか（無料かどうか）。Trueで最初の出品', null=True, blank=True, default=False)


class Request(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    request_seller = models.ForeignKey(CustomUser, verbose_name='売り手', on_delete=models.CASCADE, related_name='request_seller')
    request_buyer = models.ForeignKey(CustomUser, verbose_name='買い手', on_delete=models.CASCADE, related_name='request_buyer')
    merchandise = models.ForeignKey(Merchandise, verbose_name='商品', on_delete=models.CASCADE)
    status = models.CharField(verbose_name='リクエストが承認されたか否か', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # トークルームが生成した時刻


class Talk(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    talk_seller = models.ForeignKey(CustomUser, verbose_name='売り手', on_delete=models.CASCADE, related_name='talk_seller')
    talk_buyer = models.ForeignKey(CustomUser, verbose_name='買い手', on_delete=models.CASCADE, related_name='talk_buyer')
    merchandise = models.ForeignKey(Merchandise, verbose_name='商品', on_delete=models.CASCADE)
    last_comment = models.CharField(verbose_name='最後のコメント', max_length=100000, null=True, blank=True)
    refund_request_status = models.BooleanField(verbose_name='返金リクエストをしているか否か', null=True, blank=True)
    refund_result = models.CharField(verbose_name='返金審査の結果。「返金済み」or「返金不可」', max_length=100000, null=True, blank=True)
    pay_status = models.BooleanField(verbose_name='支払いを終えているかどうか。（Trueで終えている）', null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # トークルームが生成した時刻
    updated_at = models.DateTimeField(auto_now=True, null=True)  # 編集・更新した時刻  .save()でしか自動更新されない


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, verbose_name='コメント主', on_delete=models.CASCADE, blank=True, null=False)
    merchandise = models.ForeignKey(Merchandise, verbose_name='コメントと関係のある商品', on_delete=models.CASCADE, blank=True)
    comment = models.CharField(verbose_name='コメント', null=True, blank=True, max_length=200)
    delete = models.CharField(verbose_name='削除',  null=True, blank=True,  max_length=200)
    comment_image = models.ImageField(verbose_name='トークルームでの画像添付', blank=True, null=True, upload_to=_user_profile_avator_upload_to)
    talk = models.ForeignKey(Talk, verbose_name='トークルーム', on_delete=models.CASCADE, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)  # コメントした時刻


class Inquiry(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='お問い合わせ者の名前', max_length=200)
    email = models.CharField(verbose_name='タイトル', max_length=200)
    content = models.CharField(verbose_name='内容', max_length=100000)
    created_at = models.DateTimeField(auto_now_add=True)  # お問い合わせ時刻


class Announce(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='タイトル', max_length=200)
    content = models.CharField(verbose_name='内容', max_length=100000)
    created_at = models.DateTimeField(auto_now_add=True)  # お知らせ時刻
    image1 = models.ImageField(verbose_name='画像1', blank=True, null=True, upload_to=_user_profile_avator_upload_to)  # image1は最低限必要
    image2 = models.ImageField(verbose_name='画像2', blank=True, null=True, upload_to=_user_profile_avator_upload_to)
    image3 = models.ImageField(verbose_name='画像3', blank=True, null=True, upload_to=_user_profile_avator_upload_to)
    deleted = models.CharField(verbose_name='削除したか否か', max_length=100000, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # お問い合わせ時刻


class OpenComment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    merchandise = models.ForeignKey(Merchandise, verbose_name='商品', on_delete=models.CASCADE)
    commenter = models.ForeignKey(CustomUser, verbose_name='コメントしたユーザー', on_delete=models.CASCADE)
    comment = models.CharField(verbose_name='コメント内容', max_length=100000, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # お問い合わせ時刻


class DefaultCard(models.Model):  # stripeにデータの有無を確認する変わりにこのモデルで確認
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    default_card_status = models.BooleanField(verbose_name='デフォルトカードを設定しているか否か', null=True, blank=True)


class Report(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(CustomUser, verbose_name='通報者', on_delete=models.CASCADE, related_name='通報者')
    reported_user = models.ForeignKey(CustomUser, verbose_name='通報されたユーザー', on_delete=models.CASCADE, related_name='通報されたユーザー')
    content = models.CharField(verbose_name='通報内容', max_length=100000, null=True)


class MerchandiseQuestion(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    merchandise = models.ForeignKey(Merchandise, verbose_name='商品', on_delete=models.CASCADE)
    question = models.CharField(verbose_name='商品への質問', max_length=100000, null=True)
    question_user = models.ForeignKey(CustomUser, verbose_name='質問者', on_delete=models.CASCADE, null=True)
    answer = models.CharField(verbose_name='質問への回答', max_length=100000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # トークルームが生成した時刻
    updated_at = models.DateTimeField(auto_now=True, null=True)  # 編集・更新した時刻  .save()でしか自動更新されない