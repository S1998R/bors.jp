from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
import os
import logging
import datetime
import pytz

logger = logging.getLogger(__name__)


class AdminProtect:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        url = request.get_full_path()

        # DEBUGがFalseであり、管理サイトに対するアクセスである
        if settings.ADMIN_PATH in url and not settings.DEBUG:

            # 送信元のIPアドレスを手に入れる
            ip_list = request.META.get('HTTP_X_FORWARDED_FOR')
            if ip_list:
                ip = ip_list.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            # 送信元IPが許可IPアドレスリストに含まれていない場合はForbiddenを返す。
            if ip not in settings.ALLOWED_ADMIN:
                logger.info('アクセスしたIPアドレス')
                logger.info(ip)
                now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                logger.info('アクセスされた時間')
                logger.info(now)

                subject = '許可していないIPアドレスから管理画面にアクセスがありました。'
                message = '許可していないIPアドレスから管理画面にアクセスがありました。心当たりが無い場合、確認をお願いします。from middleware.py url:' + str(url) + 'ipアドレス：' + str(ip)
                send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">",
                          [os.environ['MANAGEMENT_EMAIL']], fail_silently=False)

                return HttpResponseForbidden()

            logger.info('アクセスしたIPアドレス')
            logger.info(ip)
            now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            logger.info('アクセスされた時間')
            logger.info(now)

            subject = '管理画面にアクセスがありました。'
            message = '管理画面にアクセスがありました。心当たりが無い場合、確認をお願いします。from middleware.py url:' + str(url)
            send_mail(subject, message, 'bors ボース ' + "<" + os.environ['INFO_EMAIL'] + ">",
                      [os.environ['MANAGEMENT_EMAIL']], fail_silently=False)

        response = self.get_response(request)

        return response

