from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.contrib import messages
from .forms import SellForm, SearchForm, TalkRoomForm, AccountEditForm, TenantForm, InquiryForm, OpenCommentForm, \
    ReportForm, MerchandiseQuestionForm, MerchandiseAnswerForm, EmailRequestForm, AnnounceForm, FacultyForm, \
    DepartmentForm, TestSellForm, TestSellFormEdit
from .models import Merchandise, Talk, Comment, Request, Inquiry, Announce, OpenComment, DefaultCard, Report, \
    MerchandiseQuestion
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail
from accounts.models import CustomUser, Faculty, Department, University
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests  # curlコマンドと同等の処理が可能
from django.http import JsonResponse  # ajaxで利用
import datetime
import math
import os
import payjp
from datetime import date, timedelta
from django.utils import timezone
import pytz
from django.core.mail import EmailMessage
import uuid
from io import BytesIO
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

from functools import reduce
from operator import or_  # 論理演算子をインポート
from django.conf import settings
from django.core.files.images import get_image_dimensions
import logging

logger = logging.getLogger(__name__)
from PIL import Image


class TopListView(generic.TemplateView):
    template_name = "merchandise_list.html"
    model = Merchandise

    def get(self, request, *args, **kwargs):

        self.request.session.set_expiry(60 * 60 * 24 * 14)  # sessionを2週間に設定

        if self.request.user.id:  # ログインしている場合

            if self.request.GET.get('university'):
                search_word = self.request.GET.get('university')
                merchandise = Merchandise.objects.filter(
                    user__university=search_word).order_by('-created_at').exclude(
                    Q(display_status="stop") | Q(user=self.request.user))

            elif self.request.GET.get('faculty'):
                search_word = self.request.GET.get('faculty')
                merchandise = Merchandise.objects.filter(faculty__faculty=search_word).order_by(
                    '-created_at').exclude(
                    Q(display_status="stop") | Q(user=self.request.user))

            elif self.request.GET.get('department'):
                search_word = self.request.GET.get('department')
                merchandise = Merchandise.objects.filter(
                    department__department=search_word).order_by('-created_at').exclude(
                    Q(display_status="stop") | Q(user=self.request.user))

            else:
                search_word = None
                merchandise = Merchandise.objects.order_by('-created_at').exclude(
                    Q(display_status="stop") | Q(user=self.request.user))

        else:  # AnonymousUserの場合（ログインしてない場合）

            if self.request.GET.get('university'):
                search_word = self.request.GET.get('university')
                merchandise = Merchandise.objects.filter(
                    user__university=search_word).order_by('-created_at').exclude(display_status="stop")

            elif self.request.GET.get('faculty'):
                search_word = self.request.GET.get('faculty')
                merchandise = Merchandise.objects.filter(faculty__faculty=search_word).order_by(
                    '-created_at').exclude(display_status="stop")

            elif self.request.GET.get('department'):
                search_word = self.request.GET.get('department')
                merchandise = Merchandise.objects.filter(
                    department__department=search_word).order_by('-created_at').exclude(display_status="stop")

            else:
                search_word = None
                merchandise = Merchandise.objects.order_by('-created_at').exclude(display_status="stop")

        params = {
            'merchandise': merchandise,
            'search_word': search_word,
        }

        return render(self.request, 'merchandise_list.html', params)

    def post(self, request, *args, **kwargs):
        search_word = self.request.POST.get('search_word')
        if self.request.user.id:  # AnonymousUserでない場合
            merchandise = Merchandise.objects.order_by('-created_at').exclude(
                Q(display_status="stop") | Q(user=self.request.user))

            if search_word:  # 検索された場合
                search_words = search_word.split()
                query_1 = reduce(or_, [Q(merchandise_name__contains=q) for q in search_words])
                query_2 = reduce(or_, [Q(explanation__contains=q) for q in search_words])
                query_3 = reduce(or_, [Q(class_name__contains=q) for q in search_words])
                query_4 = reduce(or_, [Q(region__contains=q) for q in search_words])
                query_5 = reduce(or_, [Q(user__university__contains=q) for q in search_words])
                query_6 = reduce(or_, [Q(faculty__faculty__contains=q) for q in search_words])
                query_7 = reduce(or_, [Q(department__department__contains=q) for q in search_words])
                merchandise = Merchandise.objects.order_by('-created_at').filter(
                    query_1 | query_2 | query_3 | query_4 | query_5 | query_6 | query_7).exclude(
                    Q(display_status="stop") | Q(user=self.request.user))

        else:  # AnonymousUserの場合
            merchandise = Merchandise.objects.order_by('-created_at').exclude(display_status="stop")

            if search_word:  # 検索された場合
                search_words = search_word.split()
                query_1 = reduce(or_, [Q(merchandise_name__contains=q) for q in search_words])
                query_2 = reduce(or_, [Q(explanation__contains=q) for q in search_words])
                query_3 = reduce(or_, [Q(class_name__contains=q) for q in search_words])
                query_4 = reduce(or_, [Q(region__contains=q) for q in search_words])
                query_5 = reduce(or_, [Q(user__university__contains=q) for q in search_words])
                query_6 = reduce(or_, [Q(faculty__faculty__contains=q) for q in search_words])
                query_7 = reduce(or_, [Q(department__department__contains=q) for q in search_words])
                merchandise = Merchandise.objects.order_by('-created_at').filter(
                    query_1 | query_2 | query_3 | query_4 | query_5 | query_6 | query_7).exclude(display_status="stop")

        params = {
            'merchandise': merchandise,
            'search_word': search_word,
        }

        return render(self.request, 'merchandise_list.html', params)


class SellRightCheckMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        if not DefaultCard.objects.filter(
                user=user).first().default_card_status and not user.free_sell_right and not user.special_user_status:  # カード登録してなければ登録ページに強制遷移
            return False
        return True

    def handle_no_permission(self):  # test_funcで不可だった場合のリダイレクト先を設定
        if self.request.user.id:  # 既にログインしている場合
            messages.success(self.request, "出品するには、販売手数料の支払い方法を登録して下さい。")
        return redirect("neighbor_app:method_of_payment")


class SellFormView(LoginRequiredMixin, generic.FormView):
    template_name = "sell_form.html"
    form_class = TestSellForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SellFormView, self).get_form_kwargs(*args, **kwargs)
        user = self.request.user

        university = user.university
        facultys = Faculty.objects.filter(university__university=university)

        # 入れ子のリストを作成
        faculty_selection_contents_list = [['', '選択して下さい']]
        for faculty in facultys:
            selection_element = [faculty.faculty, faculty.faculty]
            faculty_selection_contents_list = faculty_selection_contents_list + [selection_element]

        faculty_selection_contents_list = faculty_selection_contents_list + [['', '追加する']]

        # タプルに変換
        taple = ()
        for e in faculty_selection_contents_list:
            if isinstance(e, list):
                sub_taple = ()
                for e in e:
                    sub_taple += (e,)
                taple += (sub_taple,)
            else:
                taple += (e,)
        kwargs["selection"] = taple

        return kwargs


class CardRegister(LoginRequiredMixin, generic.TemplateView):  # 出品者のクレジットカードを登録
    template_name = "404.html"

    def post(self, request, *args, **kwargs):

        user = self.request.user
        user_id = str(user.id)  # payjpのretrieveの中はstr()でないとエラー
        customer = payjp.Customer.retrieve(user_id)

        not_pay_talks = Talk.objects.filter(pay_status=False, merchandise__user=user)

        payjp_token = self.request.POST.get("payjp-token")
        card = customer.cards.create(card=payjp_token, default=True)  # cardオブジェクトを作成
        card_id = card.id
        if not DefaultCard.objects.filter(user=user).first():  # userのDefaultCardオブジェクトが存在しなければ、payjpと連動してモデルを作成
            DefaultCard.objects.create(user=user, default_card_status=True)

        DefaultCard.objects.filter(user=user).update(default_card_status=True)

        not_pay_talk_status = False
        if not_pay_talks:

            not_pay_talk_status = True

            for talk in not_pay_talks:
                merchandise = talk.merchandise

                try:  # 支払い成功

                    # 支払いを行う
                    charge = payjp.Charge.create(
                        amount=math.floor(merchandise.sell_commission),  # 支払い額（商品価格の10％）
                        currency="jpy",
                        customer=str(customer.id),  # 売り手がプラットフォーム利用料を支払う
                        metadata={'merchandise_id': merchandise.pk, 'value': merchandise.value,
                                  'seller_id': merchandise.user.pk,
                                  'merchandise_name': merchandise.merchandise_name, 'time': datetime.date.today()}
                    )

                    merchandise.charge_id = charge.id
                    merchandise.save()

                    # 最後にpay_statusを更新
                    talk.pay_status = True
                    talk.save()

                except payjp.error.CardError as e:  # カード関係のエラーがあった場合
                    body = e.json_body
                    err = body['error']
                    logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
                    logger.info(err)
                    logger.info(err['message'])
                    logger.info(err['code'])
                    logger.info(err['type'])
                    logger.info(err['param'])

                    if err['code'] == 'incorrect_card_data':
                        messages.success(self.request, 'ご入力頂いたお支払い方法の情報のいずれかに誤りがあるため支払いに失敗しました。修正をお願いします。')

                    elif err['code'] == 'invalid_expiry_month':
                        messages.success(self.request, 'ご入力頂いたお支払い方法が、不正な有効期限月なため支払いに失敗しました。修正をお願いします。')

                    elif err['code'] == 'invalid_expiry_year':
                        messages.success(self.request, 'ご入力頂いたお支払い方法が、不正な有効期限年なため支払いに失敗しました。修正をお願いします。')

                    elif err['code'] == 'expired_card':
                        messages.success(self.request, 'ご入力頂いたお支払い方法が、有効期限切れなため支払いに失敗しました。修正をお願いします。')

                    elif err['code'] == 'card_declined':
                        messages.success(self.request, 'ご入力頂いたお支払い方法が、カード会社によって拒否されたため支払いに失敗しました。修正をお願いします。')

                    elif err['code'] == 'unacceptable_brand':
                        messages.success(self.request, 'ご入力頂いたお支払い方法のカードブランドが、本サービスに対応していないため支払いに失敗しました。修正をお願いします。')

                    elif err['code'] == 'missing_card':
                        messages.success(self.request, 'お支払い方法が登録されていないため、支払いに失敗しました。登録をお願いします。')

                    elif err['code'] == 'card_flagged':
                        messages.success(self.request, 'エラーが複数回続いた事によって、一時的にロックがかかりました。24時間後に利用可能となります。')

                    elif err['code'] == 'processing_error':
                        messages.success(self.request, '決済ネットワーク上でエラーが発生したため、支払いに失敗しました。時間をおいて再度お試し下さい。')

                    else:
                        messages.success(self.request, 'エラーが発生したため支払いに失敗しました。')

                    # エラーが起きた場合は支払い方法を削除
                    card = customer.cards.retrieve(card_id)
                    card.delete()
                    DefaultCard.objects.filter(user=user).update(default_card_status=False)
                    return redirect("neighbor_app:method_of_payment")

                except payjp.error.InvalidRequestError as e:
                    body = e.json_body
                    err = body['error']
                    logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
                    logger.info(err)
                    logger.info(err['message'])
                    logger.info(err['code'])
                    logger.info(err['type'])
                    logger.info(err['param'])

                    messages.success(self.request, "無効なリクエストです。支払いに失敗しました。")

                    # エラーが起きた場合は支払い方法を削除
                    card = customer.cards.retrieve(card_id)
                    card.delete()
                    DefaultCard.objects.filter(user=user).update(default_card_status=False)

                    return redirect("neighbor_app:method_of_payment")

                except payjp.error.AuthenticationError as e:
                    body = e.json_body
                    err = body['error']
                    logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
                    logger.info(err)
                    logger.info(err['message'])
                    logger.info(err['code'])
                    logger.info(err['type'])

                    messages.success(self.request, "認証エラーが発生したため、支払いに失敗しました。")

                    # エラーが起きた場合は支払い方法を削除
                    card = customer.cards.retrieve(card_id)
                    card.delete()
                    DefaultCard.objects.filter(user=user).update(default_card_status=False)

                    return redirect("neighbor_app:method_of_payment")

                except payjp.error.APIConnectionError as e:
                    body = e.json_body
                    err = body['error']
                    logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
                    logger.info(err)
                    logger.info(err['message'])
                    logger.info(err['code'])
                    logger.info(err['type'])

                    messages.success(self.request, "ネットワーク接続に失敗したため、支払いに失敗しました。")

                    # エラーが起きた場合は支払い方法を削除
                    card = customer.cards.retrieve(card_id)
                    card.delete()
                    DefaultCard.objects.filter(user=user).update(default_card_status=False)

                    return redirect("neighbor_app:method_of_payment")

                except payjp.error.PayjpException as e:
                    body = e.json_body
                    err = body['error']
                    logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
                    logger.info(err)
                    logger.info(err['message'])
                    logger.info(err['code'])
                    logger.info(err['type'])

                    messages.success(self.request, "エラーが発生したため、支払いに失敗しました。")

                    # エラーが起きた場合は支払い方法を削除
                    card = customer.cards.retrieve(card_id)
                    card.delete()
                    DefaultCard.objects.filter(user=user).update(default_card_status=False)

                    return redirect("neighbor_app:method_of_payment")

                except Exception as e:
                    body = e.json_body
                    err = body['error']
                    logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
                    logger.info(err)
                    logger.info(err['message'])
                    logger.info(err['code'])
                    logger.info(err['type'])

                    messages.success(self.request, "エラーが発生したため、支払いに失敗しました。")

                    # エラーが起きた場合は支払い方法を削除
                    card = customer.cards.retrieve(card_id)
                    card.delete()
                    DefaultCard.objects.filter(user=user).update(default_card_status=False)

                    return redirect("neighbor_app:method_of_payment")

        if not_pay_talk_status:
            messages.success(self.request, "支払い方法の登録が完了しました。手数料の支払いが完了しました。履歴はサイドバーメニューの「販売手数料の履歴」から確認できます。")
            return redirect("neighbor_app:method_of_payment")

        messages.success(self.request, "支払い方法の登録が完了しました。")

        return redirect("neighbor_app:method_of_payment")


class CardDeleteView(LoginRequiredMixin, generic.TemplateView):
    template_name = '404.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_id = str(user.id)

        # payjpのcardオブジェクトを削除
        customer = payjp.Customer.retrieve(user_id)
        card_id = str(customer.cards["data"][0]["id"])
        customer.cards.retrieve(card_id).delete()

        # DefaultCardのdefault_card_statusをfalseに
        default_card = DefaultCard.objects.filter(user=user).first()
        default_card.default_card_status = False
        default_card.save()

        messages.success(self.request, "支払い方法を削除しました。")

        return redirect("neighbor_app:method_of_payment")


class CardUpdateView(LoginRequiredMixin, generic.TemplateView):
    template_name = '404.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_id = str(user.id)

        # payjpのcardオブジェクトを削除して作成し直す
        customer = payjp.Customer.retrieve(user_id)
        card_id = str(customer.cards["data"][0]["id"])
        customer.cards.retrieve(card_id).delete()  # cardオブジェクトを削除

        payjp_token = self.request.POST.get("payjp-token")
        customer.cards.create(card=payjp_token, default=True)  # cardオブジェクトを作成

        messages.success(self.request, "支払い方法を更新しました。")

        return redirect("neighbor_app:method_of_payment")


class SellSaveView(LoginRequiredMixin, generic.CreateView):
    model = Merchandise
    form_class = SellForm
    template_name = "404.html"

    def post(self, request, *args, **kwargs):

        image_1 = None
        image_2 = None
        image_3 = None
        image_4 = None
        image_5 = None
        image_6 = None
        image_7 = None
        image_8 = None
        image_9 = None
        image_10 = None

        # 以下画像のバリデーション
        for i in range(1, 11):  # 画像1~10まで繰り返す
            if i == 1:
                image_name = 'image'
                if not self.request.FILES.get(image_name):  # トップ画像がNoneなら通さない
                    return JsonResponse({'message': "商品の画像は必須です。"})

            else:
                image_name = 'image_' + str(i)

            if self.request.FILES.get(image_name):
                image = request.FILES.get(image_name)
                if not image.name.endswith(('.png', '.jpg', '.jpeg', 'PNG', 'JPG', 'JPEG', 'svg', 'gif', 'tif', 'tiff',
                                            'psd', 'bmp', 'webp', 'blob')):
                    return JsonResponse({'message': "画像" + str(i) + "はアップロードできません。"})

                if i == 1:
                    image_1 = image
                elif i == 2:
                    image_2 = image
                elif i == 3:
                    image_3 = image
                elif i == 4:
                    image_4 = image
                elif i == 5:
                    image_5 = image
                elif i == 6:
                    image_6 = image
                elif i == 7:
                    image_7 = image
                elif i == 8:
                    image_8 = image
                elif i == 9:
                    image_9 = image
                elif i == 10:
                    image_10 = image

        user = self.request.user

        merchandise_name = self.request.POST.get('merchandise_name')
        value = self.request.POST.get('value')
        sell_commission = math.floor(int(value) * 0.08)
        if sell_commission < 50:  # 50円以下であれば50円に更新
            sell_commission = 50
        merchandise_status = self.request.POST.get('merchandise_status')
        category = self.request.POST.get('category')
        region = self.request.POST.get('region')
        explanation = self.request.POST.get('explanation')

        if not merchandise_name:
            return JsonResponse({'message': "商品名は必須です。"})
        if not value:
            return JsonResponse({'message': "価格は必須です。"})
        # 無料版ではコメントアウト
        # if int(value) > 30000:
        #     return JsonResponse({'message': "価格は30000円以下に設定して下さい。"})
        # if int(value) < 50:
        #     return JsonResponse({'message': "価格は50円以上に設定して下さい。"})  # 最低でも手数料と同じになるように
        if not merchandise_status:
            return JsonResponse({'message': "商品の状態は必須です。"})
        if not category:
            return JsonResponse({'message': "カテゴリは必須です。"})
        if not region:
            return JsonResponse({'message': "商品の受け渡しが可能なエリアは必須です。"})
        if not explanation:
            return JsonResponse({'message': "商品説明は必須です。"})

        faculty = self.request.POST.get('faculty')
        department = self.request.POST.get('department')
        plus_faculty = self.request.POST.get('plus_faculty')
        plus_department = self.request.POST.get('plus_department')
        university = University.objects.filter(university=user.university).first()
        faculty_obj = Faculty.objects.filter(university=university, faculty=faculty).first()
        department_obj = Department.objects.filter(university=university, faculty=faculty_obj,
                                                   department=department).first()

        if plus_faculty and not faculty:
            faculty_initial = plus_faculty[0]
            new_faculty_obj = Faculty.objects.create(university=university, faculty=plus_faculty,
                                                     initial=faculty_initial)

            # plus_facultyもplus_departmentも存在する場合
            if plus_department and not department:
                department_initial = plus_department[0]
                new_department_obj = Department.objects.create(university=university, faculty=new_faculty_obj,
                                                               initial=department_initial, department=plus_department)

                merchandise = Merchandise.objects.create(user=user, image=image_1, image_2=image_2, image_3=image_3,
                                                         image_4=image_4,
                                                         image_5=image_5, image_6=image_6, image_7=image_7,
                                                         image_8=image_8,
                                                         image_9=image_9,
                                                         image_10=image_10, merchandise_name=merchandise_name,
                                                         value=value, sell_commission=sell_commission,
                                                         merchandise_status=merchandise_status,
                                                         category=category, region=region, explanation=explanation,
                                                         faculty=new_faculty_obj, department=new_department_obj)

            # plus_facultyのみ存在する場合
            else:
                merchandise = Merchandise.objects.create(user=user, image=image_1, image_2=image_2, image_3=image_3,
                                                         image_4=image_4,
                                                         image_5=image_5, image_6=image_6, image_7=image_7,
                                                         image_8=image_8,
                                                         image_9=image_9,
                                                         image_10=image_10, merchandise_name=merchandise_name,
                                                         value=value, sell_commission=sell_commission,
                                                         merchandise_status=merchandise_status,
                                                         category=category, region=region, explanation=explanation,
                                                         faculty=new_faculty_obj, department=department_obj)

        elif plus_department and not department:
            department_initial = plus_department[0]
            new_department_obj = Department.objects.create(university=university, faculty=faculty_obj,
                                                           initial=department_initial,
                                                           department=plus_department)

            merchandise = Merchandise.objects.create(user=user, image=image_1, image_2=image_2, image_3=image_3,
                                                     image_4=image_4,
                                                     image_5=image_5, image_6=image_6, image_7=image_7, image_8=image_8,
                                                     image_9=image_9,
                                                     image_10=image_10, merchandise_name=merchandise_name, value=value,
                                                     sell_commission=sell_commission,
                                                     merchandise_status=merchandise_status,
                                                     category=category, region=region, explanation=explanation,
                                                     faculty=faculty_obj, department=new_department_obj)

        else:  # 新しい学部も学科も追加されてない場合
            merchandise = Merchandise.objects.create(user=user, image=image_1, image_2=image_2, image_3=image_3,
                                                     image_4=image_4,
                                                     image_5=image_5, image_6=image_6, image_7=image_7, image_8=image_8,
                                                     image_9=image_9,
                                                     image_10=image_10, merchandise_name=merchandise_name, value=value,
                                                     sell_commission=sell_commission,
                                                     merchandise_status=merchandise_status,
                                                     category=category, region=region, explanation=explanation,
                                                     faculty=faculty_obj, department=department_obj)

        # サーバーサイドでの画像のリサイズ
        merchandise_image_list = [merchandise.image, merchandise.image_2, merchandise.image_3, merchandise.image_4,
                                  merchandise.image_5, merchandise.image_6, merchandise.image_7, merchandise.image_8,
                                  merchandise.image_9, merchandise.image_10]

        for merchandise_image in merchandise_image_list:

            if merchandise_image:
                image = Image.open(merchandise_image)
                width, height = image.size

                if width > 301 or height > 301:
                    if width > height:  # widthが大きい場合
                        ratio = height / width
                        max_width = 300
                        height = max_width * ratio
                        image = image.resize((int(max_width), int(height)))

                    else:  # heightが大きい場合
                        ratio = width / height
                        max_height = 300
                        width = max_height * ratio
                        image = image.resize((int(width), int(max_height)))

                    url = merchandise_image.url  # /media/....が出力される
                    image.save(url[1:])  # [1:]で、最初の/を消して、media/...で同じurlに保存することで、リサイズした画像を上書き保存

        messages.success(self.request, "出品が完了しました。")

        return redirect("neighbor_app:sell_list")


def set_submit_token(request):  # 2重送信対策のトークンを作成
    submit_token = str(uuid.uuid4())
    request.session['submit_token'] = submit_token
    return submit_token


def exists_submit_token(request):  # 2重送信対策のトークンを確認
    token_in_request = request.POST.get('submit_token')
    token_in_session = request.session['submit_token']
    if not token_in_request:
        return False
    if not token_in_session:
        return False

    return token_in_request == token_in_session


class MerchandiseDetailTestView(generic.TemplateView):
    template_name = "merchandise_detail_test.html"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        merchandise = Merchandise.objects.filter(pk=pk).first()
        user = self.request.user
        if not merchandise:
            messages.success(self.request, "商品が見つかりません。")

            return render(self.request, '500.html')

        if not merchandise.user == user:  # 出品者では無くて商品が出品中でない場合リダイレクト

            if merchandise.display_status == "stop":  # 商品が出品中でなければリダイレクト
                messages.success(self.request, "その商品は現在出品されておりません。")

                return render(self.request, '403.html')

        self.request.session['merchandise_pk'] = pk  # merchandiseのpkをsessionに設定
        self.request.session.set_expiry(60 * 60 * 24 * 14)  # sessionを2週間に設定

        user = self.request.user
        form = MerchandiseQuestionForm()

        merchandise_questions = MerchandiseQuestion.objects.filter(merchandise=merchandise).order_by('pk')
        merchandise_question_count = merchandise_questions.count()

        submit_token = set_submit_token(request)  # 2重送信対策のトークンを作成

        if user == merchandise.user:  # userが商品の出品者の場合

            form = MerchandiseAnswerForm()

            params = {
                'merchandise': merchandise,
                'merchandise_user': 'merchandise_user',
                'form': form,
                'merchandise_questions': merchandise_questions,
                'merchandise_question_count': merchandise_question_count,
                'scroll_position': 0,
                'submit_token': submit_token,
            }

        else:  # userが商品の出品者でない場合
            params = {
                'merchandise': merchandise,
                'form': form,
                'merchandise_questions': merchandise_questions,
                'merchandise_question_count': merchandise_question_count,
                'scroll_position': 0,
                'submit_token': submit_token,
            }

        return render(self.request, 'merchandise_detail_test.html', params)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        merchandise_pk = self.request.session['merchandise_pk']  # sessionのmerchandise_pk

        if not self.request.session.get('merchandise_pk', False):  # sessionが無ければリダイレクト
            messages.success(self.request, "商品ページに戻って再度お試しください。")
            return render(self.request, '500.html')
        if not exists_submit_token(request):  # 2重送信対策
            return redirect("neighbor_app:merchandise_detail", pk=merchandise_pk)
        submit_token = set_submit_token(request)  # 新たに2重送信対策のトークンを作成

        merchandise = Merchandise.objects.filter(pk=merchandise_pk).first()

        if not merchandise:  # 該当する商品が無ければリダイレクト
            messages.success(self.request, "商品が見つかりません。")
            return render(self.request, '500.html')

        if self.request.POST.get('question_pk'):  # 質問への回答の場合
            question_pk = self.request.POST.get('question_pk')
            question = MerchandiseQuestion.objects.filter(pk=question_pk, merchandise=merchandise).first()

            if not question:  # 該当する質問が無い場合
                messages.success(self.request, "質問が見つかりません。")
                return render(self.request, '500.html')

            if question.answer:  # 既に回答がある場合（回答の編集の場合）
                question.answer = self.request.POST.get('answer')
                question.save()
                messages.success(self.request, "回答を編集しました。")

                if user == merchandise.user:  # ユーザーが出品者の場合
                    merchandise_user = True
                    form = MerchandiseAnswerForm()  # 回答用のフォームを設定

                else:  # ユーザーが購入者の場合
                    merchandise_user = False
                    form = MerchandiseQuestionForm()  # 質問作成用のフォームを設定

                scroll_position = self.request.POST.get("body_scroll_px")
                merchandise_questions = MerchandiseQuestion.objects.filter(merchandise=merchandise).order_by('pk')
                merchandise_question_count = merchandise_questions.count()

                params = {
                    'merchandise': merchandise,
                    'merchandise_user': merchandise_user,
                    'form': form,
                    'scroll_position': scroll_position,
                    'merchandise_questions': merchandise_questions,
                    'merchandise_question_count': merchandise_question_count,
                    'submit_token': submit_token,
                }

                return render(self.request, 'merchandise_detail_test.html', params)

            question.answer = self.request.POST.get('answer')
            question.save()

            # 質問者に通知のメール送信
            context = {
                'question_user_name': question.question_user.username,
                'merchandise_name': merchandise.merchandise_name,
                'url': "http://bors.jp/merchandise_detail/" + str(merchandise.pk) + "/",
            }

            subject = render_to_string('merchandise_question_questioner_mail_template/subject.txt', context)
            message = render_to_string('merchandise_question_questioner_mail_template/message.txt', context)
            send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">",
                      [question.question_user.email], fail_silently=False)

            messages.success(self.request, "質問に回答しました。")

        else:  # 質問作成の場合
            question = self.request.POST.get('question')
            MerchandiseQuestion.objects.create(question=question, question_user=user, merchandise=merchandise)

            # 出品者に通知のメール送信
            context = {
                'seller_name': merchandise.user.username,
                'url': "http://bors.jp/merchandise_detail/" + str(merchandise.pk) + "/"
            }

            subject = render_to_string('merchandise_question_seller_mail_template/subject.txt', context)
            message = render_to_string('merchandise_question_seller_mail_template/message.txt', context)
            send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [merchandise.user.email],
                      fail_silently=False)

            messages.success(self.request, "質問を作成しました。")

        if user == merchandise.user:  # ユーザーが出品者の場合
            merchandise_user = True
            form = MerchandiseAnswerForm()  # 回答用のフォームを設定

        else:  # ユーザーが購入者の場合
            merchandise_user = False
            form = MerchandiseQuestionForm()  # 質問作成用のフォームを設定

        scroll_position = self.request.POST.get("body_scroll_px")
        merchandise_questions = MerchandiseQuestion.objects.filter(merchandise=merchandise).order_by('pk')
        merchandise_question_count = merchandise_questions.count()

        params = {
            'merchandise': merchandise,
            'merchandise_user': merchandise_user,
            'form': form,
            'scroll_position': scroll_position,
            'merchandise_questions': merchandise_questions,
            'merchandise_question_count': merchandise_question_count,
            'submit_token': submit_token,
        }

        return render(self.request, 'merchandise_detail_test.html', params)


class TalkListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "talk_list.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user

        self_talks = Talk.objects.order_by('-updated_at').filter(Q(talk_seller=user) | Q(talk_buyer=user))  # 新しい順に

        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        one_month_ago_from_today = now - timedelta(days=30)

        params = {
            'user': self.request.user,
            'talks': self_talks,
            'one_month_ago_from_today': one_month_ago_from_today,
        }

        return render(self.request, 'talk_list.html', params)


class TalkRoomView(LoginRequiredMixin, generic.TemplateView):
    template_name = "talk_room.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        pk = self.kwargs['pk']
        talk = Talk.objects.filter(pk=pk).first()

        not_pay_talk = Talk.objects.filter(pay_status=False, merchandise__user=user)
        if not_pay_talk and talk.talk_seller == user and not user.special_user_status:  # userが出品者で、支払いが残っていて、スペシャルユーザーでない場合場合
            messages.success(self.request, "トークを見るには、販売手数料のお支払いが必要です。")
            return redirect("neighbor_app:method_of_payment")
        if not talk:
            messages.success(self.request, "トークルームが見つかりません。")
            return render(self.request, '403.html')
        if not talk.talk_buyer == user and not talk.talk_seller == user:  # 関係ないユーザーがアクセスした場合にブロック
            return render(self.request, '403.html')
        self.request.session['talk_room'] = pk  # talkroomのpkをsessionに設定
        self.request.session.set_expiry(60 * 60 * 24 * 14)  # sessionを2週間に設定
        comments = Comment.objects.order_by('created_at').filter(talk=talk).exclude(delete="delete")
        form = TalkRoomForm
        merchandise = talk.merchandise
        merchandise_questions = MerchandiseQuestion.objects.filter(merchandise=merchandise).order_by('pk')
        merchandise_question_count = merchandise_questions.count()

        submit_token = set_submit_token(request)  # 2重送信対策のトークンを作成

        talk_open_day = talk.created_at

        talk_close_day = talk_open_day + timedelta(days=30)

        if talk.merchandise.user == self.request.user:  # 出品者の場合、返金リクエストボタンを入れる
            params = {
                'talk': talk,
                'comments': comments,
                'form': form,
                'user': self.request.user,
                'seller': 'seller',
                'scroll_position': 0,
                'merchandise': merchandise,
                'merchandise_questions': merchandise_questions,
                'merchandise_question_count': merchandise_question_count,
                'submit_token': submit_token,
                'talk_close_day': talk_close_day,
            }
            return render(self.request, 'talk_room.html', params)

        params = {
            'talk': talk,
            'comments': comments,
            'form': form,
            'user': self.request.user,
            'scroll_position': 0,
            'merchandise': merchandise,
            'merchandise_questions': merchandise_questions,
            'merchandise_question_count': merchandise_question_count,
            'submit_token': submit_token,
            'talk_close_day': talk_close_day,
        }

        return render(self.request, 'talk_room.html', params)


class TalkRoomPostView(LoginRequiredMixin, generic.TemplateView):
    template_name = "404.html"

    def post(self, request, *args, **kwargs):
        user = self.request.user
        pk = self.request.session['talk_room']

        if not exists_submit_token(request):  # 2重送信対策
            return JsonResponse({'message': "保存に失敗しました。"})
        talk = Talk.objects.filter(pk=pk).first()
        if not talk:  # 該当するtalkが無ければ403ページにリダイレクト
            return JsonResponse({'message': "保存に失敗しました。"})
        if not talk.talk_seller == user and not talk.talk_buyer == user:  # talkに自分が関係ない場合は通さない
            return JsonResponse({'message': "保存に失敗しました。"})
        merchandise = talk.merchandise
        comment = self.request.POST.get('comment')
        talk_image = request.FILES.get("talk_image")

        if comment and talk_image:  # コメントと画像がどちらもある場合

            # 以下画像のバリデーション
            if not talk_image.name.endswith(
                    ('.png', '.jpg', '.jpeg', 'PNG', 'JPG', 'JPEG', 'svg', 'gif', 'tif', 'tiff',
                     'psd', 'bmp', 'webp', 'blob')):
                return JsonResponse({'message': "その画像はアップロードできません。"})

            comment = Comment.objects.create(user=user, merchandise=merchandise, comment=comment, talk=talk,
                                             comment_image=talk_image)

            image = Image.open(comment.comment_image)
            width, height = image.size

            if width > 301 or height > 301:
                if width > height:  # widthが大きい場合
                    ratio = height / width
                    max_width = 300
                    height = max_width * ratio
                    image = image.resize((int(max_width), int(height)))

                else:  # heightが大きい場合
                    ratio = width / height
                    max_height = 300
                    width = max_height * ratio
                    image = image.resize((int(width), int(max_height)))

                url = comment.comment_image.url  # /media/....が出力される
                image.save(url[1:])  # [1:]で、最初の/を消して、media/...で同じurlに保存することで、リサイズした画像を上書き保存

        elif talk_image and not comment:  # 画像のみがアップロードされている場合
            # 以下画像のバリデーション
            if not talk_image.name.endswith(
                    ('.png', '.jpg', '.jpeg', 'PNG', 'JPG', 'JPEG', 'svg', 'gif', 'tif', 'tiff',
                     'psd', 'bmp', 'webp', 'blob')):
                return JsonResponse({'message': "その画像はアップロードできません。"})

            comment = Comment.objects.create(user=user, merchandise=merchandise, talk=talk, comment_image=talk_image)

            image = Image.open(comment.comment_image)
            width, height = image.size

            if width > 301 or height > 301:
                if width > height:  # widthが大きい場合
                    ratio = height / width
                    max_width = 300
                    height = max_width * ratio
                    image = image.resize((int(max_width), int(height)))

                else:  # heightが大きい場合
                    ratio = width / height
                    max_height = 300
                    width = max_height * ratio
                    image = image.resize((int(width), int(max_height)))
                url = comment.comment_image.url  # /media/....が出力される
                image.save(url[1:])  # [1:]で、最初の/を消して、media/...で同じurlに保存することで、リサイズした画像を上書き保存

        elif comment and not talk_image:  # コメントのみの場合
            Comment.objects.create(user=user, merchandise=merchandise, comment=comment, talk=talk)
        else:  # どれも無い場合
            return JsonResponse({'message': "保存に失敗しました。"})

        comments = Comment.objects.order_by('pk').filter(talk=talk).exclude(delete="delete")

        talk = Talk.objects.filter(pk=pk).first()
        talk.last_comment = comment
        if talk_image:  # 画像があれば更新。
            talk.last_comment = '画像を送信しました。'
        talk.save()
        talk = Talk.objects.filter(pk=pk).first()

        form = TalkRoomForm

        scroll_position = self.request.POST.get("body_scroll_px")

        merchandise_questions = MerchandiseQuestion.objects.filter(merchandise=merchandise).order_by('pk')
        merchandise_question_count = merchandise_questions.count()

        submit_token = set_submit_token(request)  # 新たに2重送信対策のトークンを作成

        # コメント主が売り手の場合のparams
        if talk.merchandise.user == self.request.user:
            params = {
                'talk': talk,
                'comments': comments,
                'form': form,
                'user': self.request.user,
                'scroll_position': scroll_position,
                'merchandise': merchandise,
                'merchandise_questions': merchandise_questions,
                'merchandise_question_count': merchandise_question_count,
                'seller': 'seller',
                'submit_token': submit_token,
            }

        # コメント主が買い手の場合のparams
        else:
            params = {
                'talk': talk,
                'comments': comments,
                'form': form,
                'user': self.request.user,
                'scroll_position': scroll_position,
                'merchandise': merchandise,
                'merchandise_questions': merchandise_questions,
                'merchandise_question_count': merchandise_question_count,
                'submit_token': submit_token,
            }

        # コメント主が売り手の場合
        if merchandise.user == user:
            context = {
                'self_name': user.username,
                'partner_name': talk.talk_buyer.username,
                'url': "https://bors.jp/talk_room/" + str(talk.pk) + "/"
            }

            subject = render_to_string('talk_mail_template/subject.txt', context)
            message = render_to_string('talk_mail_template/message.txt', context)
            send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [talk.talk_buyer.email],
                      fail_silently=False)

        # コメント主が買い手の場合
        else:
            context = {
                'self_name': user.username,
                'partner_name': talk.talk_seller.username,
                'url': "https://bors.jp/talk_room/" + str(talk.pk) + "/"
            }

            subject = render_to_string('talk_mail_template/subject.txt', context)
            message = render_to_string('talk_mail_template/message.txt', context)
            send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [talk.talk_seller.email],
                      fail_silently=False)
        return render(self.request, 'talk_room.html', params)


class SellListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "sell_list.html"

    def get(self, request, *args, **kwargs):
        self.request.session.set_expiry(60 * 60 * 24 * 14)  # sessionを2週間に設定

        user = self.request.user

        self_merchandise = Merchandise.objects.order_by('-created_at').filter(user=user)

        params = {
            'self_merchandise': self_merchandise,
        }

        return render(self.request, 'sell_list.html', params)


class PayView(LoginRequiredMixin, generic.TemplateView):
    template_name = "404.html"  # getでアクセスしたときには「ページが見つかりませんとなるように」

    def post(self, request, *args, **kwargs):
        if not self.request.session.get('merchandise_pk', False):  # sessionが無ければリダイレクト
            messages.success(self.request, "トークページに戻って再度お試しください。")
            return render(self.request, '500.html')

        session_merchandise_pk = self.request.session['merchandise_pk']  # sessionでpkを取得
        merchandise = Merchandise.objects.filter(pk=session_merchandise_pk,
                                                 display_status=None).first()  # 出品中かつ、まだ売れてない商品のみを検索

        if not merchandise:  # 該当する商品が無ければリダイレクト
            messages.success(self.request, "商品が見つかりません。")
            return render(self.request, '500.html')

        # 無料版ではコメントアウト
        # merchandise_value = merchandise.value
        # if merchandise_value > 30000:  # 商品価格が3万円を超えていた場合は決済させない
        #     messages.success(self.request, '商品価格が3万円を超えているためトークルームを作成できません。')
        #     return redirect("neighbor_app:merchandise_detail", pk=session_merchandise_pk)

        merchandise_seller = merchandise.user

        user = self.request.user

        # 無料版のみ
        new_talk = Talk.objects.create(talk_seller=merchandise_seller, talk_buyer=user,
                                       merchandise=merchandise, pay_status=True)

        # 無料版ではコメントアウト
        # customer = payjp.Customer.retrieve(str(merchandise_seller.id))  # 売り手がプラットフォーム利用料を支払う
        # if DefaultCard.objects.filter(user=merchandise_seller).first().default_card_status:  # 支払い方法が登録されている場合
        #     if not merchandise_seller.special_user_status:  # 売り手のspecial_user_statusがFalseであれば決済する。
        #
        #         try:  # 支払い成功
        #             # 支払いを行う
        #             charge = payjp.Charge.create(
        #                 amount=math.floor(merchandise.sell_commission),  # 支払い額（商品価格の8％）
        #                 currency="jpy",
        #                 customer=str(customer.id),  # 売り手がプラットフォーム利用料を支払う
        #                 metadata={'merchandise_id': merchandise.pk, 'value': merchandise_value,
        #                           'seller_id': merchandise_seller.pk,
        #                           'merchandise_name': merchandise.merchandise_name, 'time': datetime.date.today()}
        #             )
        #             merchandise.charge_id = charge.id
        #             merchandise.save()
        #
        #             new_talk = Talk.objects.create(talk_seller=merchandise_seller, talk_buyer=user,
        #                                            merchandise=merchandise, pay_status=True)

        #         except payjp.error.CardError as e:  # カード関係のエラーがあった場合
        #             body = e.json_body
        #             err = body['error']
        #             logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
        #             logger.info(err)
        #             logger.info(err['message'])
        #             logger.info(err['code'])
        #             logger.info(err['type'])
        #
        #             count = 0
        #
        #             if err['code'] == 'incorrect_card_data':
        #                 to_seller_message = 'ご登録頂いたお支払い方法の情報のいづれかに誤りがあるためトークルーム作成に失敗しました。修正をお願いします。'
        #                 to_buyer_message = '出品者のお支払い方法に誤りがあるためトークルームを作成できません。修正されるまでお待ちください。'
        #
        #             elif err['code'] == 'invalid_expiry_month':
        #                 to_seller_message = 'ご登録頂いたお支払い方法が、不正な有効期限月なためトークルーム作成に失敗しました。修正をお願いします。'
        #                 to_buyer_message = '出品者のお支払い方法に誤りがあるためトークルームを作成できません。修正されるまでお待ちください。'
        #
        #             elif err['code'] == 'invalid_expiry_year':
        #                 to_seller_message = 'ご登録頂いたお支払い方法が、不正な有効期限年なためトークルーム作成に失敗しました。修正をお願いします。'
        #                 to_buyer_message = '出品者のお支払い方法に誤りがあるためトークルームを作成できません。修正されるまでお待ちください。'
        #
        #             elif err['code'] == 'expired_card':
        #                 to_seller_message = 'ご登録頂いたお支払い方法が、有効期限切れなためトークルーム作成に失敗しました。修正をお願いします。'
        #                 to_buyer_message = '出品者のお支払い方法に誤りがあるためトークルームを作成できません。修正されるまでお待ちください。'
        #
        #             elif err['code'] == 'card_declined':
        #                 to_seller_message = 'ご登録頂いたお支払い方法が、カード会社によって拒否されたためトークルーム作成に失敗しました。修正をお願いします。'
        #                 to_buyer_message = '出品者のお支払い方法に誤りがあるためトークルームを作成できません。修正されるまでお待ちください。'
        #
        #             elif err['code'] == 'unacceptable_brand':
        #                 to_seller_message = '登録したカードブランドが、本サービスに対応していないためトークルーム作成に失敗しました。修正をお願いします。'
        #                 to_buyer_message = '出品者のお支払い方法に誤りがあるためトークルームを作成できません。修正されるまでお待ちください。'
        #
        #             elif err['code'] == 'missing_card':
        #                 to_seller_message = 'お支払い方法が登録されていないため、トークルーム作成に失敗しました。登録をお願いします。'
        #                 to_buyer_message = '出品者のお支払い方法が未登録なためトークルームを作成できません。修正されるまでお待ちください。'
        #
        #             elif err['code'] == 'card_flagged':
        #                 to_buyer_message = 'エラーが複数回続いた事によって、一時的にロックがかかりました。24時間後に利用可能となります。'
        #                 count = 1
        #
        #             elif err['code'] == 'processing_error':
        #                 to_buyer_message = '出品者の決済ネットワーク上でエラーが発生したため、トークルームを作成できません。時間をおいて再度お試し下さい。'
        #                 count = 1
        #
        #             else:
        #                 to_buyer_message = '出品者のお支払い方法にエラーが発生したためトークルームを作成できません。'
        #                 count = 1
        #
        #             if count == 0:  # to_seller_messageが定義されている場合のみ通知
        #                 # 売り手にエラーを通知
        #                 context = {
        #                     'to_seller_message': to_seller_message,
        #                     'seller_username': merchandise_seller.username,
        #                 }
        #
        #                 subject = render_to_string('pay_error_seller_mail_template/subject.txt', context)
        #                 message = render_to_string('pay_error_seller_mail_template/message.txt', context)
        #                 send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">",
        #                           [merchandise_seller.email], fail_silently=False)
        #
        #             messages.success(self.request, to_buyer_message)
        #
        #             return redirect("neighbor_app:merchandise_detail", pk=session_merchandise_pk)
        #
        #         except payjp.error.InvalidRequestError as e:
        #             body = e.json_body
        #             err = body['error']
        #             logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
        #             logger.info(err)
        #             logger.info(err['message'])
        #             logger.info(err['code'])
        #             logger.info(err['type'])
        #
        #             messages.success(self.request, "無効なリクエストです。")
        #             return redirect("neighbor_app:merchandise_detail", pk=session_merchandise_pk)
        #
        #         except payjp.error.AuthenticationError as e:
        #             body = e.json_body
        #             err = body['error']
        #             logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
        #             logger.info(err)
        #             logger.info(err['message'])
        #             logger.info(err['code'])
        #             logger.info(err['type'])
        #
        #             messages.success(self.request, "認証エラーが発生しました。")
        #             return redirect("neighbor_app:merchandise_detail", pk=session_merchandise_pk)
        #
        #         except payjp.error.APIConnectionError as e:
        #             body = e.json_body
        #             err = body['error']
        #             logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
        #             logger.info(err)
        #             logger.info(err['message'])
        #             logger.info(err['code'])
        #             logger.info(err['type'])
        #
        #             messages.success(self.request, "ネットワーク接続に失敗しました。")
        #             return redirect("neighbor_app:merchandise_detail", pk=session_merchandise_pk)
        #
        #         except payjp.error.PayjpException as e:
        #             body = e.json_body
        #             err = body['error']
        #             logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
        #             logger.info(err)
        #             logger.info(err['message'])
        #             logger.info(err['code'])
        #             logger.info(err['type'])
        #
        #             messages.success(self.request, "エラーが発生しました。")
        #             return redirect("neighbor_app:merchandise_detail", pk=session_merchandise_pk)
        #
        #         except Exception as e:
        #             body = e.json_body
        #             err = body['error']
        #             logger.info('user_id:' + str(user.id) + 'username:' + str(user.username))
        #             logger.info(err)
        #             logger.info(err['message'])
        #             logger.info(err['code'])
        #             logger.info(err['type'])
        #
        #             messages.success(self.request, "エラーが発生しました。")
        #             return redirect("neighbor_app:merchandise_detail", pk=session_merchandise_pk)
        #
        # else:  # 支払い方法が登録されていない場合
        #     new_talk = Talk.objects.create(talk_seller=merchandise_seller, talk_buyer=user, merchandise=merchandise,
        #                                    pay_status=False)

        merchandise.merchandise_buyer = user.id
        merchandise.merchandise_buyer_account = user
        merchandise.display_status = "sold"
        merchandise.save()  # .update()だとupdate_atが更新されない

        # 買い手にメール送信
        context = {
            'username': user.username,
            'merchandise_name': merchandise.merchandise_name,
            'value': merchandise.value,
            'url': "https://bors.jp/talk_room/" + str(new_talk.pk) + "/",
        }

        subject1 = render_to_string('pay_buyer_mail_template/subject.txt', context)
        message = render_to_string('pay_buyer_mail_template/message.txt', context)
        send_mail(subject1, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [user.email],
                  fail_silently=False)

        # 売り手にメール送信
        context = {
            'seller_name': merchandise_seller.username,
            'buyer_name': user.username,
            'merchandise_name': merchandise.merchandise_name,
            'value': merchandise.value,
            'url': "https://bors.jp/talk_room/" + str(new_talk.pk) + "/",
        }

        subject2 = render_to_string('pay_seller_mail_template/subject.txt', context)
        message = render_to_string('pay_seller_mail_template/message.txt', context)
        send_mail(subject2, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [merchandise_seller.email],
                  fail_silently=False)

        messages.success(self.request, "取引相手とのトークルームが作成されました！商品を受け取りましょう！")

        return redirect("neighbor_app:talk_list")


class AccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = "account.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user

        params = {
            'user': user,
        }

        return render(self.request, "account.html", params)


class AccountEditView(LoginRequiredMixin, generic.TemplateView):
    template_name = "account_edit.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user

        data = {
            'profile': user.profile,
        }

        form = AccountEditForm(initial=data)

        params = {
            'user': user,
            'form': form,
        }

        return render(self.request, "account_edit.html", params)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile = self.request.POST.get("profile")

        if request.POST.get("image_clear") == 'clear':  # 画像が取り消された場合
            user.image = None

        elif request.POST.get("image_clear") == 'initial':  # 画像に変更が無ければ何もせずにpass
            pass

        elif request.POST.get("image_clear") == 'change':  # 画像を更新した場合
            image = request.FILES.get("image")
            user.image = image

            # 画像のリサイズ
            image = Image.open(user.image)
            width, height = image.size

            if width > 301 or height > 301:
                if width > height:  # widthが大きい場合
                    ratio = height / width
                    max_width = 300
                    height = max_width * ratio
                    image = image.resize((int(max_width), int(height)))

                else:  # heightが大きい場合
                    ratio = width / height
                    max_height = 300
                    width = max_height * ratio
                    image = image.resize((int(width), int(max_height)))

                url = user.image.url  # /media/....が出力される
                image.save(url[1:])  # [1:]で、最初の/を消して、media/...で同じurlに保存することで、リサイズした画像を上書き保存

        else:
            pass

        user.profile = profile
        user.save()

        params = {
            'user': user,
        }

        messages.success(self.request, "アカウント情報を更新しました。")

        return render(self.request, "account.html", params)


class MethodOfPaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = "method_of_payment.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_id = str(user.id)
        customer = payjp.Customer.retrieve(user_id)

        if DefaultCard.objects.filter(user=user).first().default_card_status:  # カードが登録されている場合
            card = customer.cards.retrieve(customer.default_card)
            params = {
                'card': card,
                'public_key': os.environ['TEST_PK'],
                'already_default_card': 'already_default_card',
            }

            return render(self.request, "method_of_payment.html", params)

        no_pay_talks = Talk.objects.filter(pay_status=False, merchandise__user=user)

        if user.special_user_status:  # special_userではno_pay_talksを表示しない
            no_pay_talks = None

        params = {
            "no_pay_talks": no_pay_talks,
            'no_default_card': 'no_default_card',
            'public_key': os.environ['TEST_PK'],
        }

        return render(self.request, "method_of_payment.html", params)


class DisplayStopView(LoginRequiredMixin, generic.TemplateView):
    template_name = "sell_list.html"

    def post(self, request, *args, **kwargs):
        user = self.request.user
        merchandise_pk = self.request.POST.get("merchandise_pk")
        merchandise = Merchandise.objects.filter(pk=merchandise_pk).first()

        if merchandise.user == user:  # pkが本当に自分の商品か確認

            if self.request.POST.get("stop_status"):

                if self.request.POST.get("stop_status") == "stop":
                    merchandise.display_status = "stop"
                    merchandise.save()
                    messages.success(self.request, "出品を停止しました。")

                elif self.request.POST.get("stop_status") == "stop_clear":

                    # 無料版ではコメントアウト
                    # if not DefaultCard.objects.filter(user=user).first().default_card_status:  # カードが登録されていない場合
                    #     messages.success(self.request, "お支払い方法が登録されていないため出品できません。")
                    #     return redirect("neighbor_app:merchandise_detail", pk=merchandise_pk)

                    merchandise.display_status = None
                    merchandise.save()
                    messages.success(self.request, "出品を再開しました。")

        else:
            messages.success(self.request, "ステータスの変更に失敗しました。再度お試しください。")

        return redirect("neighbor_app:merchandise_detail", pk=merchandise_pk)


class MerchandiseEditView(LoginRequiredMixin, generic.FormView):
    template_name = "merchandise_edit.html"
    form_class = TestSellFormEdit

    def get_form_kwargs(self, *args, **kwargs):

        kwargs = super().get_form_kwargs(*args, **kwargs)
        pk = self.kwargs['pk']
        merchandise = Merchandise.objects.filter(pk=pk).first()

        user = self.request.user
        university = user.university
        facultys = Faculty.objects.filter(university__university=university)

        # 学部の入れ子のリストを作成
        faculty_selection_contents_list = [['', '選択して下さい']]
        for faculty in facultys:
            selection_element = [faculty.faculty, faculty.faculty]
            faculty_selection_contents_list = faculty_selection_contents_list + [selection_element]

        faculty_selection_contents_list = faculty_selection_contents_list + [['', '追加する']]

        # タプルに変換
        taple = ()
        for e in faculty_selection_contents_list:
            if isinstance(e, list):
                sub_taple = ()
                for e in e:
                    sub_taple += (e,)
                taple += (sub_taple,)
            else:
                taple += (e,)
        kwargs["faculty_selection"] = taple

        faculty = merchandise.faculty
        departments = Department.objects.filter(university__university=university, faculty=faculty)
        # 学科の入れ子のリストを作成
        department_selection_contents_list = [['', '選択して下さい']]
        for department in departments:
            selection_element = [department.department, department.department]
            department_selection_contents_list = department_selection_contents_list + [selection_element]

        department_selection_contents_list = department_selection_contents_list + [['', '追加する']]
        # タプルに変換
        taple = ()
        for e in department_selection_contents_list:
            if isinstance(e, list):
                sub_taple = ()
                for e in e:
                    sub_taple += (e,)
                taple += (sub_taple,)
            else:
                taple += (e,)
        kwargs["department_selection"] = taple

        if not merchandise.user == user:  # 関係ないユーザーがアクセスした場合にブロック
            return render(self.request, '403.html')

        kwargs['merchandise_name'] = merchandise.merchandise_name
        kwargs['value'] = merchandise.value
        kwargs['category'] = merchandise.category
        kwargs['explanation'] = merchandise.explanation
        kwargs['merchandise_status'] = merchandise.merchandise_status
        kwargs['region'] = merchandise.region
        if merchandise.faculty:
            kwargs['faculty'] = merchandise.faculty.faculty
        if merchandise.department:
            kwargs['department'] = merchandise.department.department
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        pk = self.kwargs['pk']
        merchandise = Merchandise.objects.filter(pk=pk).first()

        if not merchandise.user == user:  # 関係ないユーザーがアクセスした場合にブロック
            return render(self.request, '403.html')

        context['merchandise'] = merchandise

        return context


class MerchandiseEditPostView(LoginRequiredMixin, generic.UpdateView):
    template_name = "404.html"
    form_class = SellForm
    model = Merchandise

    def post(self, request, *args, **kwargs):
        user = self.request.user
        merchandise_pk = self.request.POST.get("merchandise_pk")
        merchandise = Merchandise.objects.filter(pk=merchandise_pk).first()

        if not merchandise.user == user:  # 関係ないユーザーがアクセスした場合にブロック
            return render(self.request, '403.html')

        merchandise_name = self.request.POST.get("merchandise_name")
        value = self.request.POST.get("value")
        sell_commission = int(value) * 0.08
        category = self.request.POST.get("category")
        explanation = self.request.POST.get("explanation")
        region = self.request.POST.get("region")
        merchandise_status = self.request.POST.get("merchandise_status")

        if merchandise.user == user:  # pkが本当に自分の商品か確認

            merchandise.merchandise_name = merchandise_name
            merchandise.value = value
            merchandise.category = category
            merchandise.explanation = explanation
            merchandise.region = region
            merchandise.merchandise_status = merchandise_status
            merchandise.sell_commission = sell_commission

            # 以下画像のバリデーション
            for i in range(1, 11):  # 画像1~10まで繰り返す
                if i == 1:
                    image_name = 'image'
                    image_clear = 'image_clear'
                    image = request.FILES.get(image_name)

                    if self.request.POST.get(image_clear) == 'clear':
                        return JsonResponse({'message': "商品の画像は必須です。"})

                else:
                    image_name = 'image_' + str(i)
                    image_clear = 'image_clear_' + str(i)
                    image = request.FILES.get(image_name)

                if image:
                    # image = request.FILES.get(image_name)
                    if not image.name.endswith(
                            ('.png', '.jpg', '.jpeg', 'PNG', 'JPG', 'JPEG', 'svg', 'gif', 'tif', 'tiff',
                             'psd', 'bmp', 'webp', 'blob')):
                        return JsonResponse({'message': "画像" + str(i) + "はアップロードできません。"})

                if i == 1:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image = None
                    elif image:
                        merchandise.image = image
                elif i == 2:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_2 = None
                    elif image:
                        merchandise.image_2 = image
                elif i == 3:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_3 = None
                    elif image:
                        merchandise.image_3 = image
                elif i == 4:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_4 = None
                    elif image:
                        merchandise.image_4 = image
                elif i == 5:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_5 = None
                    elif image:
                        merchandise.image_5 = image
                elif i == 6:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_6 = None
                    elif image:
                        merchandise.image_6 = image
                elif i == 7:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_7 = None
                    elif image:
                        merchandise.image_7 = image
                elif i == 8:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_8 = None
                    elif image:
                        merchandise.image_8 = image
                elif i == 9:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_9 = None
                    elif image:
                        merchandise.image_9 = image
                elif i == 10:
                    if self.request.POST.get(image_clear) == 'clear':
                        merchandise.image_10 = None
                    elif image:
                        merchandise.image_10 = image

            faculty = self.request.POST.get('faculty')
            department = self.request.POST.get('department')
            plus_faculty = self.request.POST.get('plus_faculty')
            plus_department = self.request.POST.get('plus_department')

            university = University.objects.filter(university=user.university).first()
            faculty_obj = Faculty.objects.filter(university=university, faculty=faculty).first()
            department_obj = Department.objects.filter(university=university, faculty=faculty_obj,
                                                       department=department).first()
            if plus_faculty and not faculty:
                faculty_initial = plus_faculty[0]
                new_faculty_obj = Faculty.objects.create(university=university, faculty=plus_faculty,
                                                         initial=faculty_initial)

                # plus_facultyもplus_departmentも存在する場合
                if plus_department and not department:
                    department_initial = plus_department[0]
                    new_department_obj = Department.objects.create(university=university, faculty=new_faculty_obj,
                                                                   initial=department_initial,
                                                                   department=plus_department)
                    merchandise.faculty = new_faculty_obj
                    merchandise.department = new_department_obj
                    merchandise.save()
                    return redirect("neighbor_app:merchandise_detail", pk=merchandise_pk)
                merchandise.faculty = new_faculty_obj
                merchandise.department = department_obj
                merchandise.save()
                return redirect("neighbor_app:merchandise_detail", pk=merchandise_pk)
            if plus_department and not department:
                department_initial = plus_department[0]
                new_department_obj = Department.objects.create(university=university, faculty=faculty_obj,
                                                               initial=department_initial,
                                                               department=plus_department)

                merchandise.faculty = faculty_obj
                merchandise.department = new_department_obj
                merchandise.save()
                return redirect("neighbor_app:merchandise_detail", pk=merchandise_pk)

            merchandise.faculty = faculty_obj
            merchandise.department = department_obj
            merchandise.save()

            # サーバーサイドでの画像のリサイズ
            merchandise_image_list = [merchandise.image, merchandise.image_2, merchandise.image_3, merchandise.image_4,
                                      merchandise.image_5, merchandise.image_6, merchandise.image_7,
                                      merchandise.image_8,
                                      merchandise.image_9, merchandise.image_10]

            for merchandise_image in merchandise_image_list:

                if merchandise_image:
                    image = Image.open(merchandise_image)
                    width, height = image.size

                    if width > 301 or height > 301:
                        if width > height:  # widthが大きい場合
                            ratio = height / width
                            max_width = 300
                            height = max_width * ratio
                            image = image.resize((int(max_width), int(height)))

                        else:  # heightが大きい場合
                            ratio = width / height
                            max_height = 300
                            width = max_height * ratio
                            image = image.resize((int(width), int(max_height)))

                        url = merchandise_image.url  # /media/....が出力される
                        image.save(url[1:])  # [1:]で、最初の/を消して、media/...で同じurlに保存することで、リサイズした画像を上書き保存

            messages.success(self.request, "編集が完了しました。")

        else:
            messages.success(self.request, "編集に失敗しました。再度お試しください。")

        return redirect("neighbor_app:merchandise_detail", pk=merchandise_pk)


class AboutServiceView(generic.TemplateView):
    template_name = "about_service.html"


class SCTL(generic.TemplateView):
    template_name = "sctl.html"


class TermsOfService(generic.TemplateView):
    template_name = "terms_of_service.html"


class PrivacyPolicy(generic.TemplateView):
    template_name = "privacy_policy.html"


class InquiryView(generic.CreateView):
    template_name = "inquiry_form.html"
    model = Inquiry
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        form = InquiryForm()

        params = {
            'form': form,
        }
        return render(self.request, 'inquiry_form.html', params)

    def form_valid(self, form):
        Data = form.save(commit=False)
        name = Data.name
        email = self.request.POST.get('email')
        content = Data.content
        Data.save()

        subject = 'お客様からのお問い合わせ from ' + str(name)
        send_mail(subject, content + '返信用メール：' + email, os.environ['STAFF_EMAIL'], [os.environ['STAFF_EMAIL']], fail_silently=False)  # 入力されたメールアドレスから運営へメール送信

        context = {
            'name': Data.name,
            'content': content,
        }

        subject1 = render_to_string('confirm_mail_template/inquiry_subject.txt', context)
        message = render_to_string('confirm_mail_template/inquiry_message.txt', context)
        send_mail(subject1, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [email],
                  fail_silently=False)  # 入力されたメールアドレスに確認メールを送信

        messages.success(self.request, "お問い合わせ内容を送信しました。確認の自動返信メールが届かない場合は、正確なメールアドレスが入力されていないか、迷惑メールに分類されている可能性があります。")

        return redirect('neighbor_app:inquiry')

    def form_invalid(self, form, **kwargs):
        messages.success(self.request, "送信に失敗しました。申し訳ございません、再度お試しください。")

        return redirect('neighbor_app:inquiry')


class InformationView(generic.ListView):
    template_name = "announce_list.html"
    model = Announce
    paginate_by = 10

    def get_queryset(self):
        announce = Announce.objects.order_by('-created_at').exclude(deleted='deleted')

        return announce


class InformationDetailView(generic.TemplateView):
    template_name = "information_detail.html"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        announce = Announce.objects.filter(pk=pk).first()

        params = {
            'announce': announce,
        }

        return render(self.request, 'information_detail.html', params)


class RetireView(generic.TemplateView):
    template_name = "retire.html"

    def post(self, request, *args, **kwargs):
        user = self.request.user

        merchandise = Merchandise.objects.filter(user=user)

        for item in merchandise:  # 出品されている商品をstop状態にする
            item.display_status = "stop"
            item.save()

        user.is_active = False
        user.save()

        messages.success(self.request, "退会が完了しました。")

        return redirect('account_login')


class AccountProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account_profile.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        partner_user = CustomUser.objects.filter(id=pk).first()  # 取引相手

        if not partner_user:  # 存在しないuserの場合は通さない
            messages.success(self.request, "ユーザーが見つかりません。")
            return render(self.request, '403.html')

        form = ReportForm()

        merchandise = Merchandise.objects.filter(user=partner_user).order_by('-created_at').exclude(display_status="stop")

        params = {
            'merchandise': merchandise,
            'partner_user': partner_user,
            'form': form,
        }

        return render(self.request, 'account_profile.html', params)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']  # 被通報者のpk
        reported_user = CustomUser.objects.filter(id=pk).first()
        reporter = self.request.user
        content = self.request.POST.get('content')

        Report.objects.create(reporter=reporter, reported_user=reported_user, content=content)

        context = {
            'username': self.request.user,
        }

        subject = render_to_string('report_mail_template/subject.txt', context)
        message = render_to_string('report_mail_template/message.txt', context)
        send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [os.environ['STAFF_EMAIL']],
                  fail_silently=False)

        messages.success(self.request, "通報が完了しました。")

        return redirect("neighbor_app:account_profile", pk=pk)


class RefundRequestView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'talk_room.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user

        cases = self.request.POST.get('cases')
        image = request.FILES.get("image_for_refund")
        if not cases == 'はい' and not cases == 'いいえ':
            return JsonResponse({'message': "選択してください。"})

        if cases == 'はい' and not image:  # トップ画像がNoneなら通さない
            return JsonResponse({'message': "画像のアップロードは必須です。"})

        if not self.request.session.get('talk_room', False):
            return JsonResponse({'message': 'トークページに戻って再度お試しください。'})
            # messages.success(self.request, "トークページに戻って再度お試しください。")
            # return render(self.request, '500.html')

        if cases == 'いいえ':
            image = None

        talk_room_pk = self.request.session['talk_room']  # sessionに保存したtalkのpkを保存
        talk_room = Talk.objects.filter(pk=talk_room_pk).first()

        if not talk_room.talk_seller == user:  # 出品者でなければ通さない

            return JsonResponse({'message': 'アクセス権限がありません。'})

        merchandise = talk_room.merchandise
        talk_buyer = talk_room.talk_buyer
        talk_room.refund_request_status = True  # refund_request_statusを更新
        talk_room.save()

        # 返金のリクエストの通知を買い手に送信
        context = {
            'seller_username': user.username,
            'talk_buyer_username': talk_buyer.username,
            'merchandise_name': merchandise.merchandise_name,
            'url': "https://bors.jp/talk_room/" + str(talk_room.pk) + "/",
        }

        subject = render_to_string('refund_request_mail_to_buyer_template/subject.txt', context)
        message = render_to_string('refund_request_mail_to_buyer_template/message.txt', context)
        send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [talk_buyer.email],
                  fail_silently=False)

        # 返金のリクエストを運営に送信
        context = {
            'talk_room_id': talk_room_pk,
            'username': user.username,
            'user_id': user.id,  # リクエストした人のuserid
            'user_email': user.email,  # リクエストした人のemail
            'merchandise_name': merchandise.merchandise_name,
            'cases': cases,
            'refund_page_url': 'https://bors.jp/refund_procedure/' + str(talk_room.pk) + '/',
        }

        subject = render_to_string('refund_request_mail_template/subject.txt', context)
        message = render_to_string('refund_request_mail_template/message.txt', context)

        email = EmailMessage(subject, message, from_email=os.environ['INFO_EMAIL'], to=[os.environ['REFUND_EMAIL']])

        if image:  # 画像が送信されていれば、メールに添付する

            email.attach('design.png', image.read(), 'image/png')  # 画像を添付、.read()じゃないとエラー

        email.send()
        messages.success(self.request, "返金リクエストが完了しました。運営が返金審査を行い、結果をメールにて返信いたします。")

        return redirect("neighbor_app:talk_room", pk=talk_room_pk)


class EmailRequestView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'email_request.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        email_permission = user.email_permission

        data = {
            'email_permission': email_permission
        }

        form = EmailRequestForm(initial=data)

        params = {
            'form': form,
        }

        return render(self.request, 'email_request.html', params)

    def post(self, request, *args, **kwargs):
        user = self.request.user

        email_permission = self.request.POST.get('email_permission')

        if email_permission is None:
            messages.success(self.request, "設定の変更に失敗しました。")

            return redirect("neighbor_app:email_request")

        user.email_permission = email_permission
        user.save()

        messages.success(self.request, "メールの受け取り設定を変更しました。")

        return redirect("neighbor_app:email_request")


class SendEmailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'send_email.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_superuser:  # スーパーユーザーで無ければ通さない

            return render(self.request, '404.html')

        form = AnnounceForm()

        params = {
            'form': form,
        }

        return render(self.request, 'send_email.html', params)

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_superuser:  # スーパーユーザーで無ければ通さない
            return render(self.request, '404.html')

        if not self.request.POST.get("title"):
            messages.success(self.request, "titleがNoneです。")
            return render(self.request, 'send_email.html')

        if not self.request.POST.get("content"):
            messages.success(self.request, "contentがNoneです。")
            return render(self.request, 'send_email.html')

        subject = self.request.POST.get("title")
        message = self.request.POST.get("content")  # お知らせに掲載用のテキスト

        Announce.objects.create(title=subject, content=message)

        email_message_bottom = '''


-------------------------------------------------------
※本メールは送信専用ですので返信には対応できません。ご了承ください。
お問い合わせはこちら
https://bors.jp/inquiry/

ログインページはこちら
https://bors.jp/accounts/login/

メール受け取り設定の変更はこちら
https://bors.jp/email_request/

※本メールに心当たりのない場合は至急こちらまでご連絡下さい。
https://bors.jp/inquiry/
-------------------------------------------------------
'''

        email_message = message + email_message_bottom  # メール送信用のテキスト

        send_users = CustomUser.objects.filter(email_permission=True, is_active=True)

        for send_user in send_users:
            email = send_user.email

            send_mail(subject, email_message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">", [email],
                      fail_silently=False)

        messages.success(self.request, "メールを送信しました。")

        return redirect('neighbor_app:send_email')


class DepartmentSelectionsView(LoginRequiredMixin, generic.TemplateView):
    template_name = '404.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user

        faculty = self.request.POST.get('faculty')
        university = user.university
        departments = Department.objects.filter(university__university=university, faculty__faculty=faculty)

        department_list = []
        for item in departments:
            department_list = department_list + [item.department]

        return JsonResponse({'department_list': department_list})


class SellCommissionHistoryView(LoginRequiredMixin, generic.TemplateView):
    template_name = "sell_commission_history.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user

        talks = Talk.objects.filter(talk_seller=user).exclude(pay_status=False).order_by(
            '-updated_at')  # 支払いを終えているものだけ表示

        params = {
            'talks': talks,
        }

        return render(self.request, 'sell_commission_history.html', params)


class RefundProcedureView(LoginRequiredMixin, generic.TemplateView):
    template_name = "refund_procedure.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_superuser:  # スーパーユーザーで無ければ通さない

            return render(self.request, '404.html')

        pk = self.kwargs['pk']
        self.request.session['refund_talk_pk'] = pk
        self.request.session.set_expiry(60 * 60 * 24 * 14)

        talk = Talk.objects.filter(pk=pk).first()

        params = {
            'talk': talk,
        }

        return render(self.request, 'refund_procedure.html', params)


class RefundProcedurePost(LoginRequiredMixin, generic.TemplateView):
    template_name = "404.html"

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_superuser:  # スーパーユーザーで無ければ通さない

            return render(self.request, '404.html')

        refund_talk_pk = self.request.session['refund_talk_pk']

        talk = Talk.objects.filter(pk=refund_talk_pk).first()

        if talk.refund_result:
            messages.success(self.request, "すでに返金審査は完了しています。")
            return redirect('neighbor_app:refund_procedure')

        merchandise = talk.merchandise
        merchandise_pk = merchandise.pk

        merchandise_charge_id = Merchandise.objects.filter(pk=merchandise_pk).first().charge_id

        if self.request.POST.get("refund") == 'True':
            charge = payjp.Charge.retrieve(merchandise_charge_id)
            charge.refund()
            talk.refund_result = '返金済み'
            talk.save()
            messages.success(self.request, "返金手続きが完了しました。")

        elif self.request.POST.get("refund") == 'False':

            talk.refund_result = '返金不可'
            talk.save()
            messages.success(self.request, "返金せず、不可としました。")

        else:
            messages.success(self.request, "返金手続きに失敗しました。")

        params = {
            'talk': talk,
        }

        return render(self.request, 'refund_procedure.html', params)


class TalkListForRefund(LoginRequiredMixin, generic.TemplateView):
    template_name = "talk_list_for_refund.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_superuser:  # スーパーユーザーで無ければ通さない

            return render(self.request, '404.html')

        talks = Talk.objects.all()

        params = {
            'talks': talks,
        }

        return render(self.request, 'talk_list_for_refund.html', params)


def ajax_get_customuser(request):
    entered_username = request.GET.get('entered_username')
    entered_username_exists = CustomUser.objects.filter(username=entered_username).exists()
    if entered_username_exists:
        return JsonResponse({'Username': 1})
    else:
        return JsonResponse({'Username': 0})
