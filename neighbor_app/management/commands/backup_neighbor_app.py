import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Merchandise, Talk, Comment, Inquiry, Announce, DefaultCard, Report, MerchandiseQuestion
from accounts.models import CustomUser, Faculty, Department, University
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = "Backup Diary data"

    def handle(self, *args, **options):
        # 実行時のYYYYMMDDを取得
        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        """------------------Customuser_is_active_True_include_passwordオブジェクト-------------------------------"""
        # 保存ファイルの相対パス
        file_path = settings.BACKUP_PATH + 'Customuser_is_active_True_include_password/' + 'customeuser_is_active_True_include_password' + date + '.csv'
        # 保存ディレクトリが存在しなければ作成
        os.makedirs(settings.BACKUP_PATH + '/Customuser_is_active_True_include_password', exist_ok=True)

        # バックアップファイルの作成
        with open(file_path, 'w', encoding="utf_8_sig") as file:
            writer = csv.writer(file)

            # ヘッダーの書き込み
            header = ['id', 'email', 'username', 'university', 'profile', 'special_user_status', 'email_permission', 'is_active', 'password', 'image']
            writer.writerow(header)

            # CustomUserテーブルの全データを取得
            users = CustomUser.objects.filter(is_active=True)

            # データ部分の書き込み
            for user in users:
                writer.writerow([str(user.id),
                                 str(user.email),
                                 str(user.username),
                                 str(user.university),
                                 str(user.profile),
                                 str(user.special_user_status),
                                 str(user.email_permission),
                                 str(user.is_active),
                                 str(user.password),
                                 str(user.image),
                                 ])

        # 保存ディレクトリのファイルリストを取得
        files = os.listdir(settings.BACKUP_PATH + '/Customuser_is_active_True_include_password')
        # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
        if len(files) > 9:
            files.sort()
            os.remove(settings.BACKUP_PATH + '/Customuser_is_active_True_include_password/' + files[0])

    """------------------Customuser_is_active_True_exclude_passwordオブジェクト------------------------------------"""

    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'Customuser_is_active_True_exclude_password/' + 'customeuser_is_active_True_exclude_password' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/Customuser_is_active_True_exclude_password', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'email', 'username', 'university', 'profile', 'special_user_status', 'email_permission',
                  'is_active', 'image']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        users = CustomUser.objects.filter(is_active=True)

        # データ部分の書き込み
        for user in users:
            writer.writerow([str(user.id),
                             str(user.email),
                             str(user.username),
                             str(user.university),
                             str(user.profile),
                             str(user.special_user_status),
                             str(user.email_permission),
                             str(user.is_active),
                             str(user.image),
                             ])

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/Customuser_is_active_True_exclude_password')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/Customuser_is_active_True_exclude_password/' + files[0])

    """------------------Customuser_is_active_False_include_passwordオブジェクト-------------------------------------"""

    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'Customuser_is_active_False_include_password/' + 'customeuser_is_active_False_include_password' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/Customuser_is_active_False_include_password', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'email', 'username', 'university', 'profile', 'special_user_status', 'email_permission',
                  'is_active', 'password', 'image']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        users = CustomUser.objects.filter(is_active=False)

        # データ部分の書き込み
        for user in users:
            writer.writerow([str(user.id),
                             str(user.email),
                             str(user.username),
                             str(user.university),
                             str(user.profile),
                             str(user.special_user_status),
                             str(user.email_permission),
                             str(user.is_active),
                             str(user.password),
                             str(user.image),
                             ])

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/Customuser_is_active_False_include_password')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/Customuser_is_active_False_include_password/' + files[0])

    """------------------Customuser_is_active_False_exclude_passwordオブジェクト-------------------------------------"""

    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'Customuser_is_active_False_exclude_password/' + 'customeuser_is_active_False_exclude_password' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/Customuser_is_active_False_exclude_password', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'email', 'username', 'university', 'profile', 'special_user_status', 'email_permission',
                  'is_active', 'image']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        users = CustomUser.objects.filter(is_active=False)

        # データ部分の書き込み
        for user in users:
            writer.writerow([str(user.id),
                             str(user.email),
                             str(user.username),
                             str(user.university),
                             str(user.profile),
                             str(user.special_user_status),
                             str(user.email_permission),
                             str(user.is_active),
                             str(user.image),
                             ])

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/Customuser_is_active_False_exclude_password')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/Customuser_is_active_False_exclude_password/' + files[0])

    """------------------Merchandiseオブジェクト---------------------------------------------------------------"""
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'merchandise/' + 'merchandise_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/merchandise', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'created_at', 'updated_at', 'user', 'merchandise_name', 'value', 'explanation', 'category', 'merchandise_status', 'display_status', 'merchandise_buyer_id', 'merchandise_buyer_account', 'region',
                  'image', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'image_7', 'image_8', 'image_9', 'image_10',
                  'sell_commission', 'faculty', 'department', 'charge_id', 'first_sell', 'class_name']

        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        merchandises = Merchandise.objects.order_by('id')

        # データ部分の書き込み
        for merchandise in merchandises:
            writer.writerow(
                [
                    str(merchandise.id),
                    str(merchandise.created_at),
                    str(merchandise.updated_at),
                    str(merchandise.user),
                    str(merchandise.merchandise_name),
                    str(merchandise.value),
                    str(merchandise.explanation),
                    str(merchandise.category),
                    str(merchandise.merchandise_status),
                    str(merchandise.display_status),
                    str(merchandise.merchandise_buyer_id),
                    str(merchandise.merchandise_buyer_account),
                    str(merchandise.region),
                    str(merchandise.image),
                    str(merchandise.image_2),
                    str(merchandise.image_3),
                    str(merchandise.image_4),
                    str(merchandise.image_5),
                    str(merchandise.image_6),
                    str(merchandise.image_7),
                    str(merchandise.image_8),
                    str(merchandise.image_9),
                    str(merchandise.image_10),
                    str(merchandise.sell_commission),
                    str(merchandise.faculty),
                    str(merchandise.department),
                    str(merchandise.charge_id),
                    str(merchandise.first_sell),
                    str(merchandise.class_name),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/merchandise')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/merchandise/' + files[0])

    """------------------Talkオブジェクト------------------------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'talk/' + 'talk_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/talk', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'talk_seller', 'talk_buyer', 'merchandise', 'last_comment', 'refund_request_status', 'refund_result', 'pay_status', 'created_at', 'updated_at']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        talks = Talk.objects.order_by('id')

        # データ部分の書き込み
        for talk in talks:
            writer.writerow(
                [
                    str(talk.id),
                    str(talk.talk_seller),
                    str(talk.talk_buyer),
                    str(talk.merchandise),
                    str(talk.last_comment),
                    str(talk.refund_request_status),
                    str(talk.refund_result),
                    str(talk.pay_status),
                    str(talk.created_at),
                    str(talk.updated_at),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/talk')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/talk/' + files[0])

    """------------------Commentオブジェクト------------------------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'comment/' + 'comment_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/comment', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'user', 'merchandise', 'comment', 'delete', 'talk', 'comment_image', 'created_at']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        comments = Comment.objects.order_by('id')
        # データ部分の書き込み
        for comment in comments:
            writer.writerow(
                [
                    str(comment.id),
                    str(comment.user),
                    str(comment.merchandise),
                    str(comment.comment),
                    str(comment.delete),
                    str(comment.talk),
                    str(comment.comment_image),
                    str(comment.created_at),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/comment')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/comment/' + files[0])

    """------------------Inquiryオブジェクト------------------------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'inquiry/' + 'inquiry_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/inquiry', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'name', 'email', 'content', 'created_at']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        inquirys = Inquiry.objects.order_by('id')
        # データ部分の書き込み
        for inquiry in inquirys:
            writer.writerow(
                [
                    str(inquiry.id),
                    str(inquiry.name),
                    str(inquiry.email),
                    str(inquiry.content),
                    str(inquiry.created_at),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/inquiry')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/inquiry/' + files[0])

    """------------------Announceオブジェクト------------------------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'announce/' + 'announce_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/announce', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'title', 'content', 'created_at', 'deleted']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        announces = Announce.objects.order_by('id')
        # データ部分の書き込み
        for announce in announces:
            writer.writerow(
                [
                    str(announce.id),
                    str(announce.title),
                    str(announce.content),
                    str(announce.created_at),
                    str(announce.deleted),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/announce')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/announce/' + files[0])

    """------------------DefaultCardオブジェクト--------------------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'defaultcard/' + 'defaultcard_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/defaultcard', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'user', 'default_card_status']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        defaultcards = DefaultCard.objects.order_by('id')
        # データ部分の書き込み
        for defaultcard in defaultcards:
            writer.writerow(
                [
                    str(defaultcard.id),
                    str(defaultcard.user),
                    str(defaultcard.default_card_status),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/defaultcard')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/defaultcard/' + files[0])

    """------------------Reportオブジェクト------------------------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'report/' + 'report_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/report', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'reporter', 'reported_user', 'content']
        writer.writerow(header)

        # CustomUserテーブルの全データを取得
        reports = Report.objects.order_by('id')
        # データ部分の書き込み

        for report in reports:
            writer.writerow(
                [
                    str(report.id),
                    str(report.reporter),
                    str(report.reported_user),
                    str(report.content),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/report')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/report/' + files[0])

    """------------------MerchandiseQuestionオブジェクト---------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'merchandisequestion/' + 'merchandisequestion_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/merchandisequestion', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'merchandise', 'question', 'question_user', 'answer', 'created_at', 'updated_at']
        writer.writerow(header)
        # CustomUserテーブルの全データを取得
        merchandisequestions = MerchandiseQuestion.objects.order_by('id')
        # データ部分の書き込み
        for merchandisequestion in merchandisequestions:
            writer.writerow(
                [
                    str(merchandisequestion.id),
                    str(merchandisequestion.merchandise),
                    str(merchandisequestion.question),
                    str(merchandisequestion.question_user),
                    str(merchandisequestion.answer),
                    str(merchandisequestion.created_at),
                    str(merchandisequestion.updated_at),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/merchandisequestion')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/merchandisequestion/' + files[0])

    """------------------Universityオブジェクト---------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'university/' + 'university_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/university', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'university', 'initial', 'email_domain']
        writer.writerow(header)
        # CustomUserテーブルの全データを取得
        universitys = University.objects.order_by('id')
        # データ部分の書き込み
        for university in universitys:
            writer.writerow(
                [
                    str(university.id),
                    str(university.university),
                    str(university.initial),
                    str(university.email_domain),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/university')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/university/' + files[0])

    """------------------Facultyオブジェクト---------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'faculty/' + 'faculty_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/faculty', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'university', 'faculty', 'initial']
        writer.writerow(header)
        # CustomUserテーブルの全データを取得
        facultys = Faculty.objects.order_by('id')
        # データ部分の書き込み
        for faculty in facultys:
            writer.writerow(
                [
                    str(faculty.id),
                    str(faculty.university),
                    str(faculty.faculty),
                    str(faculty.initial),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/faculty')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/faculty/' + files[0])

    """------------------Departmentオブジェクト---------------------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'department/' + 'department_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/department', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'university', 'faculty', 'department', 'initial']
        writer.writerow(header)
        # CustomUserテーブルの全データを取得
        departments = Department.objects.order_by('id')
        # データ部分の書き込み
        for department in departments:
            writer.writerow(
                [
                    str(department.id),
                    str(department.university),
                    str(department.faculty),
                    str(department.department),
                    str(department.initial),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/department')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/department/' + files[0])


    """------------------allauthのaccountのEmailAddressオブジェクト---------------------------------------------"""

    # 保存ファイルの相対パス
    file_path = settings.BACKUP_PATH + 'emailaddress/' + 'emailaddress_' + date + '.csv'
    # 保存ディレクトリが存在しなければ作成
    os.makedirs(settings.BACKUP_PATH + '/emailaddress', exist_ok=True)

    # バックアップファイルの作成
    with open(file_path, 'w', encoding="utf_8_sig") as file:
        writer = csv.writer(file)

        # ヘッダーの書き込み
        header = ['id', 'user', 'email', 'verified', 'primary', 'created_at', 'updated_at']
        writer.writerow(header)
        # CustomUserテーブルの全データを取得
        emailaddresses = EmailAddress.objects.order_by('id')
        # データ部分の書き込み
        for emailaddress in emailaddresses:
            writer.writerow(
                [
                    str(emailaddress.id),
                    str(emailaddress.user),
                    str(emailaddress.email),
                    str(emailaddress.verified),
                    str(emailaddress.primary),
                ]
            )

    # 保存ディレクトリのファイルリストを取得
    files = os.listdir(settings.BACKUP_PATH + '/emailaddress')
    # ファイルが設定数以上あったら一番古いファイルを削除(現状では3日分保存されるようになっている)
    if len(files) > 9:
        files.sort()
        os.remove(settings.BACKUP_PATH + '/emailaddress/' + files[0])


