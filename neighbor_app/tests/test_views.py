from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from ..models import Merchandise, Talk, Comment, Inquiry, Announce, OpenComment, DefaultCard, Report, MerchandiseQuestion
from accounts.models import CustomUser, Faculty, Department, University
from django.core.files.uploadedfile import SimpleUploadedFile
import payjp
import pprint
import inspect
import time

# selenium用
from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import Select


######### seleniumテスト
class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver(executable_path='C:\\Users\\sato4\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe')  # ドライバの配置場所を指定

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):  # sato50でログイン
        # ログインページを開く
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('account_login')))

        # ログイン
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('sato50@dc.tohoku.ac.jp')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("abcabcabca")
        self.selenium.find_element_by_class_name('register_button').click()

        # ページタイトル確認
        self.assertEqual('bors ボース | 大学生向けのフリマプラットフォーム', self.selenium.title)

    def test_login2(self):  # sato200でログイン
        # ログインページを開く
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('account_login')))
        time.sleep(3)
        # ログイン
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('sato200@dc.tohoku.ac.jp')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("abcabcabca")
        self.selenium.find_element_by_class_name('register_button').click()

        # ページタイトル確認
        self.assertEqual('bors ボース | 大学生向けのフリマプラットフォーム', self.selenium.title)

    def test_login3(self):  # sato310(カード登録なし)でログイン
        # ログインページを開く
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('account_login')))

        # ログイン
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('sato310@dc.tohoku.ac.jp')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("abcabcabca")
        self.selenium.find_element_by_class_name('register_button').click()

        # ページタイトル確認
        self.assertEqual('bors ボース | 大学生向けのフリマプラットフォーム', self.selenium.title)

    def test_login4(self):  # sato330(カード登録なし、special_user_status=True)でログイン
        # ログインページを開く
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('account_login')))

        # ログイン
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('sato330@dc.tohoku.ac.jp')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("abcabcabca")
        self.selenium.find_element_by_class_name('register_button').click()

        # ページタイトル確認
        self.assertEqual('bors ボース | 大学生向けのフリマプラットフォーム', self.selenium.title)


class SellForm(TestLogin):

    def sell_form(self):
        self.test_login()
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:sell_form')))

        # ページタイトル確認
        self.assertEqual('出品する | bors', self.selenium.title)

        for i in range(1, 7):
            if i == 1:
                value = 624
            elif i == 2:
                value = 30001
            elif i == 3:
                value = 30000
            elif i == 4:
                value = 625
            elif i == 5:
                value = 49
            elif i == 6:
                value = 50

            # 通常の送信
            image_input = self.selenium.find_element_by_name("image")
            image_input.send_keys("C:\\Users\\sato4\\Downloads\\女子アイコン.png")  # 画像のパスを指定
            merchandise_name_input = self.selenium.find_element_by_name("merchandise_name")
            merchandise_name_input.send_keys("商品名_test")
            value_input = self.selenium.find_element_by_name("value")
            value_input.send_keys(value)
            category_input = self.selenium.find_element_by_name("category")
            select = Select(category_input)  # select boxを生成
            select.select_by_index(2)  # 選択
            explanation_input = self.selenium.find_element_by_name("explanation")
            explanation_input.send_keys("商品の説明_test")
            region_input = self.selenium.find_element_by_name("region")
            region_input.send_keys("受け渡し可能なエリア")
            merchandise_status_input = self.selenium.find_element_by_name("merchandise_status")
            merchandise_status_input.send_keys("未使用")
            self.selenium.find_element_by_class_name('register_button').click()

            # time.sleep(3)  # 待機させないとajaxの挙動が最後まで確認できない
            self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:sell_form')))  # もう一度sell_formにアクセス


class SellFormCardTrue(TestLogin):

    def sell_form(self):
        self.test_login()
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:sell_form')))

        # ページタイトル確認
        self.assertEqual('出品する | bors', self.selenium.title)

        # 通常の送信
        image_input = self.selenium.find_element_by_name("image")
        image_input.send_keys("C:\\Users\\sato4\\Downloads\\女子アイコン.png")  # 画像のパスを指定
        merchandise_name_input = self.selenium.find_element_by_name("merchandise_name")
        merchandise_name_input.send_keys("商品名_test")
        value_input = self.selenium.find_element_by_name("value")
        value_input.send_keys(500)
        category_input = self.selenium.find_element_by_name("category")
        select = Select(category_input)  # select boxを生成
        select.select_by_index(2)  # 選択
        explanation_input = self.selenium.find_element_by_name("explanation")
        explanation_input.send_keys("商品の説明_test")
        region_input = self.selenium.find_element_by_name("region")
        region_input.send_keys("受け渡し可能なエリア")
        merchandise_status_input = self.selenium.find_element_by_name("merchandise_status")
        merchandise_status_input.send_keys("未使用")
        self.selenium.find_element_by_class_name('register_button').click()

        time.sleep(10)  # 待機させないとajaxの挙動が最後まで確認できない

        self.selenium.find_element_by_id('side_bar_button').click()
        self.selenium.find_element_by_id('logout_a').click()  # ログアウト

        self.test_login2()

        time.sleep(2)

        self.selenium.find_element_by_class_name('image_div').click()  # 最初の商品を選択
        self.selenium.find_element_by_id('buy_button_div').click()  # 購入ボタンを押す
        self.selenium.find_element_by_id('popup_buy_button').click()  # ポップアップの購入ボタンを押す
        time.sleep(3)

        self.selenium.find_element_by_id('side_bar_button').click()
        self.selenium.find_element_by_id('logout_a').click()  # ログアウト

        self.test_login()


class SellFormCardFalse(TestLogin):

    def sell_form(self):
        self.test_login3()
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:sell_form')))

        # ページタイトル確認
        self.assertEqual('出品する | bors', self.selenium.title)

        # 通常の送信
        image_input = self.selenium.find_element_by_name("image")
        image_input.send_keys("C:\\Users\\sato4\\Downloads\\女子アイコン.png")  # 画像のパスを指定
        merchandise_name_input = self.selenium.find_element_by_name("merchandise_name")
        merchandise_name_input.send_keys("商品名_test")
        value_input = self.selenium.find_element_by_name("value")
        value_input.send_keys(500)
        category_input = self.selenium.find_element_by_name("category")
        select = Select(category_input)  # select boxを生成
        select.select_by_index(2)  # 選択
        explanation_input = self.selenium.find_element_by_name("explanation")
        explanation_input.send_keys("商品の説明_test")
        region_input = self.selenium.find_element_by_name("region")
        region_input.send_keys("受け渡し可能なエリア")
        merchandise_status_input = self.selenium.find_element_by_name("merchandise_status")
        merchandise_status_input.send_keys("未使用")
        self.selenium.find_element_by_class_name('register_button').click()

        time.sleep(10)  # 待機させないとajaxの挙動が最後まで確認できない

        self.selenium.find_element_by_id('side_bar_button').click()
        self.selenium.find_element_by_id('logout_a').click()  # ログアウト

        self.test_login2()

        time.sleep(2)

        self.selenium.find_element_by_class_name('image_div').click()  # 最初の商品を選択
        self.selenium.find_element_by_id('buy_button_div').click()  # 購入ボタンを押す
        self.selenium.find_element_by_id('popup_buy_button').click()  # ポップアップの購入ボタンを押す
        time.sleep(5)

        self.selenium.find_element_by_id('side_bar_button').click()
        self.selenium.find_element_by_id('logout_a').click()  # ログアウト

        self.test_login3()


class TalkRoomCardTrue(SellFormCardTrue):

    def talk_room(self):
        self.sell_form()
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:talk_list')))
        self.selenium.find_element_by_class_name('image_and_talk').click()  # 最新のトークルームを選択
        time.sleep(3)

        comment_input = self.selenium.find_element_by_name("comment")
        comment_input.send_keys("コメント_test")
        self.selenium.find_element_by_id('talk_submit_button').click()
        time.sleep(3)
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:talk_list')))
        self.selenium.find_element_by_class_name('image_and_talk').click()  # 最新のトークルームを選択
        time.sleep(3)

        talk_image_input = self.selenium.find_element_by_name("talk_image")
        talk_image_input.send_keys("C:\\Users\\sato4\\Downloads\\女子アイコン.png")  # 画像のパスを指定
        self.selenium.find_element_by_id('talk_submit_button').click()
        time.sleep(3)
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:talk_list')))
        self.selenium.find_element_by_class_name('image_and_talk').click()  # 最新のトークルームを選択
        time.sleep(3)

        talk_image_input = self.selenium.find_element_by_name("talk_image")
        talk_image_input.send_keys("C:\\Users\\sato4\\Downloads\\女子アイコン.png")  # 画像のパスを指定
        comment_input = self.selenium.find_element_by_name("comment")
        comment_input.send_keys("コメント_test")
        self.selenium.find_element_by_id('talk_submit_button').click()
        time.sleep(3)
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:talk_list')))
        self.selenium.find_element_by_class_name('image_and_talk').click()  # 最新のトークルームを選択
        time.sleep(3)


class TalkRoomCardFalse(SellFormCardFalse):

    def talk_room(self):
        self.sell_form()
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:talk_list')))
        self.selenium.find_element_by_class_name('image_and_talk').click()  # 最新のトークルームを選択 → カード登録画面に遷移
        time.sleep(5)


class RefundSeleniumTest(SellFormCardTrue):

    def refund(self):
        self.sell_form()
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:talk_list')))
        self.selenium.find_element_by_class_name('image_and_talk').click()  # 最新のトークルームを選択
        time.sleep(3)

        self.selenium.find_element_by_id('refund_form_button').click()

        cases_input = self.selenium.find_element_by_name("cases")
        select = Select(cases_input)  # select boxを生成
        select.select_by_index(0)  # 選択

        self.selenium.find_element_by_id('refund_request_button').click()  # セレクトボックスを選択しないと送信できない
        time.sleep(3)

        select.select_by_index(1)  # 選択
        self.selenium.find_element_by_id('refund_request_button').click()  # 画像を選択しないと送信できない
        time.sleep(3)

        image_input = self.selenium.find_element_by_name("image_for_refund")
        image_input.send_keys("C:\\Users\\sato4\\Downloads\\女子アイコン.png")  # 画像のパスを指定
        self.selenium.find_element_by_id('refund_request_button').click()  # 送信完了
        time.sleep(5)


class CardRegister(TestLogin):

    def card(self):
        self.test_login4()
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('neighbor_app:method_of_payment')))
        self.selenium.find_element_by_id('card_update_button').click()
        time.sleep(3)

        # iframeに切り替え
        iframe = self.selenium.find_element_by_id('payjp-checkout-iframe')
        self.selenium.switch_to.frame(iframe)

        payjp_cardNumber_input = self.selenium.find_element_by_id("payjp_cardNumber")
        payjp_cardNumber_input.send_keys("4242 4242 4242 4242")
        payjp_cardExpiresMonth_input = self.selenium.find_element_by_id("payjp_cardExpiresMonth")
        payjp_cardExpiresMonth_input.send_keys("7")
        payjp_cardExpiresYear_input = self.selenium.find_element_by_id("payjp_cardExpiresYear")
        payjp_cardExpiresYear_input.send_keys("22")
        payjp_cardCvc_input = self.selenium.find_element_by_id("payjp_cardCvc")
        payjp_cardCvc_input.send_keys("123")
        payjp_cardName_input = self.selenium.find_element_by_id("payjp_cardName")
        payjp_cardName_input.send_keys("TEST TEST")

        self.selenium.find_element_by_id('payjp_cardSubmit').click()

        time.sleep(5)

        self.selenium.switch_to.default_content()

        self.selenium.find_element_by_id('card_delete_button').click()

        time.sleep(5)

######################### ここまでseleniumテスト


class LoggedInTestCaseDefaultCardTrue(TestCase):  # default_card_status=Trueのユーザー
    card_id = None  # クラス変数に定義。とりあえずNone。後から値を上書きする。

    def setUp(self):
        print('LoggedInTestCaseDefaultCardTrue')
        print('LoggedInTestCaseDefaultCardTrue')
        print('LoggedInTestCaseDefaultCardTrue')
        print('LoggedInTestCaseDefaultCardTrue')
        print('LoggedInTestCaseDefaultCardTrue')
        payjp.Customer.retrieve('1').delete()  # 前に残ったpayjpのcustomerオブジェクトを削除
        self.password = 'abcabcabca'

        self.test_seller = get_user_model().objects.create_user(
            username='sato_test_seller',
            email='sato_test_seller@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )

        self.client.login(email=self.test_seller.email, password=self.password)
        user_id = str(self.test_seller.id)
        payjp.Customer.create(id=user_id)
        # 出品者のデフォルトカードを作成
        payjp_token = payjp.Token.create(
            card={
                'number': '4242424242424242',
                'cvc': '123',
                'exp_month': '2',
                'exp_year': '2024',
            },
            headers={'X-Payjp-Direct-Token-Generate': 'true'}
        )

        card = payjp.Customer.retrieve(user_id).cards.create(card=str(payjp_token.id), default=True)  # cardオブジェクトを作成

        self.card_id = str(card.id)

        DefaultCard.objects.create(user=self.test_seller, default_card_status=True)  # default_card_status=True


class LoggedInTestCaseDefaultCardFalse(TestCase):  # default_card_status=Falseのユーザー

    def setUp(self):
        print('LoggedInTestCaseDefaultCardFalse')
        print('LoggedInTestCaseDefaultCardFalse')
        print('LoggedInTestCaseDefaultCardFalse')
        print('LoggedInTestCaseDefaultCardFalse')
        print('LoggedInTestCaseDefaultCardFalse')
        payjp.Customer.retrieve('1').delete()  # 前に残ったpayjpのcustomerオブジェクトを削除
        self.password = 'abcabcabca'
        self.test_seller = get_user_model().objects.create_user(
            username='sato_test_seller',
            email='sato_test_seller@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )

        self.client.login(email=self.test_seller.email, password=self.password)
        user_id = self.test_seller.id
        payjp.Customer.create(id=user_id)
        DefaultCard.objects.create(user=self.test_seller, default_card_status=False)  # default_card_status=False
        print('default_card')
        print('default_card')
        print('default_card')
        print('default_card')
        print(DefaultCard.objects.all().first().default_card_status)


class LoggedInSuperUser(TestCase):  # default_card_status=Trueのユーザー
    card_id = None  # クラス変数に定義。とりあえずNone。後から値を上書きする。

    def setUp(self):
        payjp.Customer.retrieve('1').delete()  # 前に残ったpayjpのcustomerオブジェクトを削除
        self.password = 'abcabcabca'

        self.test_seller = get_user_model().objects.create_user(
            username='sato_test_seller',
            email='sato_test_seller@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
            is_superuser=True,
        )

        self.client.login(email=self.test_seller.email, password=self.password)
        user_id = str(self.test_seller.id)
        payjp.Customer.create(id=user_id)
        # 出品者のデフォルトカードを作成
        payjp_token = payjp.Token.create(
            card={
                'number': '4242424242424242',
                'cvc': '123',
                'exp_month': '2',
                'exp_year': '2024',
            },
            headers={'X-Payjp-Direct-Token-Generate': 'true'}
        )

        card = payjp.Customer.retrieve(user_id).cards.create(card=str(payjp_token.id), default=True)  # cardオブジェクトを作成

        self.card_id = str(card.id)

        DefaultCard.objects.create(user=self.test_seller, default_card_status=True)  # default_card_status=True


class SellFormTest(LoggedInTestCaseDefaultCardTrue):

    def get_sell_form(self):  # カードを登録した場合にアクセスできるかテスト
        response = self.client.get(reverse('neighbor_app:sell_form'))
        self.assertEqual(response.status_code, 200)  # リダイレクトではない
        self.assertTemplateUsed(response, 'sell_form.html')

    def post_merchandise(self):
        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
        }

        response = self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証
        self.assertRedirects(response, reverse('neighbor_app:sell_list'))  # あくまでサーバーエンドではリダイレクトすることになってるが、実際はajaxなので動作確認は別途必要。

    def post_merchandise_default_faculty_department(self):
        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')

        university = University.objects.create(university='東北大学')
        faculty = Faculty.objects.create(faculty='工学部', university=university, initial='工')
        department = Department.objects.create(university=university, department='材料科学総合学科', faculty=faculty, initial='材')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
            'faculty': faculty.faculty,
            'department': department.department,
        }

        response = self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().faculty, faculty)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().department, department)
        self.assertRedirects(response, reverse('neighbor_app:sell_list'))  # あくまでサーバーエンドではリダイレクトすることになってるが、実際はajaxなので動作確認は別途必要。

    def post_merchandise_only_new_faculty(self):
        university = University.objects.create(university='東北大学')
        faculty = Faculty.objects.create(faculty='工学部', university=university, initial='工')
        Department.objects.create(department='材料科学総合学科', faculty=faculty, initial='材')

        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
            'plus_faculty': '新学部',
        }

        response = self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().faculty.faculty, '新学部')
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().department, None)
        self.assertRedirects(response, reverse('neighbor_app:sell_list'))  # あくまでサーバーエンドではリダイレクトすることになってるが、実際はajaxなので動作確認は別途必要。

    def post_merchandise_only_new_department(self):
        university = University.objects.create(university='東北大学')
        faculty = Faculty.objects.create(faculty='工学部', university=university, initial='工')
        Department.objects.create(department='材料科学総合学科', faculty=faculty, initial='材')

        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
            'plus_department': '新学科',
        }

        response = self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().faculty, None)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().department.department, '新学科')
        self.assertRedirects(response, reverse('neighbor_app:sell_list'))  # あくまでサーバーエンドではリダイレクトすることになってるが、実際はajaxなので動作確認は別途必要。

    def post_merchandise_only_new_department_default_faculty(self):
        university = University.objects.create(university='東北大学')
        faculty = Faculty.objects.create(faculty='工学部', university=university, initial='工')
        Department.objects.create(department='材料科学総合学科', faculty=faculty, initial='材')

        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
            'faculty': faculty.faculty,
            'plus_department': '新学科',
        }

        response = self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().faculty, faculty)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().department.department, '新学科')
        self.assertRedirects(response, reverse('neighbor_app:sell_list'))  # あくまでサーバーエンドではリダイレクトすることになってるが、実際はajaxなので動作確認は別途必要。

    def post_merchandise_new_faculty_department(self):
        university = University.objects.create(university='東北大学')
        faculty = Faculty.objects.create(faculty='工学部', university=university, initial='工')
        Department.objects.create(department='材料科学総合学科', faculty=faculty, initial='材')

        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
            'plus_faculty': '新学部',
            'plus_department': '新学科',
        }

        response = self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().faculty.faculty, '新学部')  # データベースに保存されているかを検証
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().department.department, '新学科')  # データベースに保存されているかを検証
        self.assertRedirects(response, reverse('neighbor_app:sell_list'))  # あくまでサーバーエンドではリダイレクトすることになってるが、実際はajaxなので動作確認は別途必要。








    def post_error_confirm(self):  # 商品を出品させない処理を確認
        # 画像が無ければ通さない事を確認
        params = {
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
        }

        response = self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertJSONEqual(response.content, {'message': "商品の画像は必須です。"})

        ################################################################


class NotCardSellFormTest(LoggedInTestCaseDefaultCardFalse):  # カードを登録せずに出品

    def not_card_get_sell_form(self):  # カードを登録してない場合でもアクセスできるかテスト
        response = self.client.get(reverse('neighbor_app:sell_form'))
        self.assertEqual(response.status_code, 200)  # リダイレクトではない
        self.assertTemplateUsed(response, 'sell_form.html')

    def not_card_post_merchandise(self):  # カードを登録せずに出品
        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
        }

        response = self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証
        self.assertRedirects(response, reverse('neighbor_app:sell_list'))  # あくまでサーバーエンドではリダイレクトすることになってるが、実際はajaxなので動作確認は別途必要。


class ReserveMerchandiseTest(LoggedInTestCaseDefaultCardTrue):  # 出品者のカード登録ありで出品、商品を予約する一連の流れ

    def reserve_merchandise(self):
        print('reserve_merchandise')
        print('reserve_merchandise')
        print('reserve_merchandise')
        print('reserve_merchandise')
        print('reserve_merchandise')
        # 出品者が商品を出品
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
        }

        self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証

        # 出品者はログアウト
        self.client.logout()

        # 購入者を作成、ログイン
        self.test_buyer = get_user_model().objects.create_user(
            username='sato_test_buyer',
            email='sato_test_buyer@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )

        # 購入者でDefaultCardオブジェクトを作成
        DefaultCard.objects.create(user=self.test_buyer, default_card_status=True)  # default_card_status=True

        self.client.login(email=self.test_buyer.email, password=self.password)  # 購入者がログイン

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk

        self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存

        response = self.client.post(reverse('neighbor_app:pay'))  # 商品を予約（トークルーム作成）

        self.assertEqual(Talk.objects.filter(talk_buyer=self.test_buyer).count(), 1)  # トークルームがデータベースに保存されているかを検証
        self.assertRedirects(response, reverse('neighbor_app:talk_list'))


class NotCardReserveMerchandiseTest(LoggedInTestCaseDefaultCardFalse):  # 出品者のカード登録なしで出品、商品を予約する一連の流れ

    def not_card_reserve_merchandise(self):
        print('not_card_reserve_merchandise')
        print('not_card_reserve_merchandise')
        print('not_card_reserve_merchandise')
        print('not_card_reserve_merchandise')
        print('not_card_reserve_merchandise')
        # 出品者が商品を出品
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'image': image,
            'merchandise_name': '商品名_test',
            'value': 1000,
            'category': 'other',
            'explanation': '商品の説明_test',
            'region': '受け渡し可能なエリア',
            'merchandise_status': '未使用',
        }

        self.client.post(reverse('neighbor_app:sell_save'), params)
        self.assertEqual(Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').count(), 1)  # データベースに保存されているかを検証

        # 出品者はログアウト
        self.client.logout()

        # 購入者を作成
        self.test_buyer = get_user_model().objects.create_user(
            username='sato_test_buyer',
            email='sato_test_buyer@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )

        # 購入者でDefaultCardオブジェクトを作成
        # DefaultCard.objects.create(user=self.test_buyer, default_card_status=True)  # default_card_status=True

        self.client.login(email=self.test_buyer.email, password=self.password)  # 購入者がログイン

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk

        self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存

        response = self.client.post(reverse('neighbor_app:pay'))  # 商品を予約（トークルーム作成）

        self.assertEqual(Talk.objects.filter(talk_buyer=self.test_buyer).count(), 1)  # トークルームがデータベースに保存されているかを検証
        # print(Talk.objects.filter(talk_buyer=self.test_buyer).first().pay_status)
        self.assertRedirects(response, reverse('neighbor_app:talk_list'))


class AccessMerchandiseDetail(SellFormTest, ReserveMerchandiseTest):

    def access_not_login(self):  # ログインしてなくてもアクセスできるかテスト
        self.post_merchandise()  # 商品を投稿

        self.client.logout()  # ログアウト

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk

        response = self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセス

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'merchandise_detail_test.html')
        self.assertContains(response, 'ログインして質問する')  # 「ログインして質問する」ボタンがあるか確認
        self.assertContains(response, 'ログインして購入する')  # 「ログインして購入する」ボタンがあるか確認

    def access_seller(self):  # 出品者がアクセス
        self.post_merchandise()  # 商品を投稿

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk
        print(merchandise_pk)
        print(self.client)
        response = self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセス

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'merchandise_detail_test.html')
        self.assertNotContains(response, '質問する')  # 「質問する」ボタンがないか確認
        self.assertContains(response, '商品の編集')  # 「商品の編集」ボタンがあるか確認
        self.assertContains(response, '出品停止')  # 「出品停止」ボタンがあるか確認
        self.assertNotContains(response, '購入する')  # 「購入する」ボタンがないか確認

    def access_buyer(self):  # 購入者がアクセス
        self.post_merchandise()  # 商品を投稿

        # 出品者はログアウト
        self.client.logout()

        # 質問者を作成、ログイン
        self.test_buyer = get_user_model().objects.create_user(
            username='sato_test_buyer',
            email='sato_test_buyer@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )

        self.client.login(email=self.test_buyer.email, password=self.password)  # 質問者がログイン

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk

        response = self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセス

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'merchandise_detail_test.html')
        self.assertContains(response, '質問する')  # 「質問する」ボタンがあるか確認
        self.assertNotContains(response, '商品の編集')  # 「商品の編集」ボタンが無いことを確認
        self.assertNotContains(response, '出品停止')  # 「出品停止」ボタンがあるか確認
        self.assertContains(response, '購入する')  # 「購入する」ボタンがあるか確認

    def access_after_sold(self):  # 売り切れた後にアクセス（購入者、出品者、anonymousユーザー）
        self.reserve_merchandise()  # 商品を投稿、購入まで完了

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk

        response = self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # 購入者がアクセス

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'merchandise_detail_test.html')
        self.assertContains(response, '売り切れ')
        self.assertNotContains(response, '質問する')  # 「質問する」ボタンがないか確認
        self.assertNotContains(response, '商品の編集')  # 「商品の編集」ボタンが無いことを確認
        self.assertNotContains(response, '出品停止')  # 「出品停止」ボタンがあるか確認
        self.assertNotContains(response, '購入する')  # 「購入する」ボタンが無いことを確認

        self.client.logout()  # ログアウト

        self.client.login(email=self.test_seller.email, password=self.password)

        response = self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # 出品差がアクセス

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'merchandise_detail_test.html')
        self.assertNotContains(response, '質問する')  # 「質問する」ボタンがないか確認
        self.assertContains(response, '売り切れ')  # 「売り切れ」があるか確認
        self.assertNotContains(response, '商品の編集')  # 「商品の編集」ボタンが無いことを確認
        self.assertNotContains(response, '購入する')  # 「購入する」ボタンが無いことを確認

        self.client.logout()  # ログアウト

        response = self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # anonymousユーザーがアクセス

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'merchandise_detail_test.html')
        self.assertContains(response, '売り切れ')  # 「ログインして質問する」ボタンがあるか確認
        self.assertNotContains(response, '質問する')  # 「質問する」ボタンがないか確認
        self.assertNotContains(response, '商品の編集')  # 「商品の編集」ボタンが無いことを確認
        self.assertNotContains(response, '購入する')  # 「購入する」ボタンが無いことを確認


class TalkTest(ReserveMerchandiseTest):  # 支払いを終えた場合のトークルームでの一連の流れ

    def pay_get_talk(self):  # 支払いを終えていれば出品者もアクセスできる

        self.reserve_merchandise()  # 支払い完了
        talk_room_pk = Talk.objects.filter(talk_buyer=self.test_buyer).first().pk
        response = self.client.get(reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_pk}))  # 支払いを終えて購入者がアクセス
        self.assertEqual(response.status_code, 200)  # アクセスできる
        self.client.logout()  # 購入者がログアウト
        self.client.login(email=self.test_seller.email, password=self.password)  # 出品者がログイン
        response = self.client.get(reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_pk}))  # 支払いを終えて出品者がアクセス
        self.assertEqual(response.status_code, 200)  # アクセスできる
        self.client.logout()  # 出品者がログアウト

    def post_comment(self):  # トークルームでメッセージを投稿
        self.reserve_merchandise()  # reserve_merchandiseを呼出し
        self.assertEqual(Talk.objects.all().count(), 1)  # reserve_merchandiseが引き継がれているか検証
        self.assertEqual(Talk.objects.all().first().last_comment, None)  # last_commentを確認

        talk_room_id = Talk.objects.filter(talk_buyer=self.test_buyer).first().id
        get_response = self.client.get(reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_id}))  # コメント前にページにアクセスしてトークルームのidをsessionに保存
        submit_token = get_response.context['submit_token']  # renderの中から抽出

        # メッセージを投稿
        params = {
            'comment': 'よろしくお願いします。',
            'submit_token': submit_token,
        }

        self.client.post(reverse('neighbor_app:talk_room_post'), params)

        self.assertEqual(Comment.objects.all().count(), 1)  # コメントが投稿されたかを確認
        self.assertEqual(Talk.objects.all().first().last_comment, 'よろしくお願いします。')  # last_commentを確認

    def post_image(self):  # トークルームで画像のみを投稿
        self.reserve_merchandise()  # reserve_merchandiseを呼出し
        self.assertEqual(Talk.objects.all().count(), 1)  # reserve_merchandiseが引き継がれているか検証
        self.assertEqual(Talk.objects.all().first().last_comment, None)  # last_commentを確認

        talk_room_id = Talk.objects.filter(talk_buyer=self.test_buyer).first().id

        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')

        get_response = self.client.get(reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_id}))  # コメント前にページにアクセスしてsubmittokenを格納
        submit_token = get_response.context['submit_token']  # renderの中から抽出

        # メッセージを投稿
        params = {
            'talk_image': image,
            'submit_token': submit_token,
        }

        response = self.client.post(reverse('neighbor_app:talk_room_post'), params)

        self.assertEqual(Comment.objects.all().count(), 1)  # コメントが投稿されたかを確認

        self.assertEqual(Talk.objects.filter(talk_seller=self.test_seller).first().last_comment, '画像を送信しました。')  # 画像の投稿でlast_commentが更新されたか確認。

        self.assertEqual(response.status_code, 200)

    def post_image_and_comment(self):  # トークルームで画像とコメントを投稿
        self.reserve_merchandise()  # reserve_merchandiseを呼出し
        self.assertEqual(Talk.objects.all().count(), 1)  # reserve_merchandiseが引き継がれているか検証
        self.assertEqual(Talk.objects.all().first().last_comment, None)  # last_commentを確認

        talk_room_id = Talk.objects.filter(talk_buyer=self.test_buyer).first().id

        get_response = self.client.get(
            reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_id}))  # コメント前にページにアクセスしてトークルームのidをsessionに保存

        submit_token = get_response.context['submit_token']  # renderの中から抽出

        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')

        # メッセージを投稿
        params = {
            'comment': 'よろしくお願いします。',
            'talk_image': image,
            'submit_token': submit_token,
        }

        response = self.client.post(reverse('neighbor_app:talk_room_post'), params)

        self.assertEqual(Comment.objects.all().count(), 1)  # コメントが投稿されたかを確認

        self.assertEqual(Talk.objects.filter(talk_seller=self.test_seller).first().last_comment, '画像を送信しました。')  # 画像の投稿でlast_commentが更新されたか確認。

        self.assertEqual(response.status_code, 200)


class NotCardTalkTest(NotCardReserveMerchandiseTest):  # 支払いを終えてなければ出品者はアクセスできないことを確認
    
    def not_pay_get_talk(self):  # 支払いを終えてなければ出品者はアクセスできない
        self.not_card_reserve_merchandise()  # 支払い未完了
        talk_room_pk = Talk.objects.filter(talk_buyer=self.test_buyer).first().pk
        response = self.client.get(reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_pk}))  # 支払いを終えずに購入者がアクセス
        self.assertEqual(response.status_code, 200)  # アクセスできる
        self.client.logout()  # 購入者がログアウト
        self.client.login(email=self.test_seller.email, password=self.password)  # 出品者がログイン
        response = self.client.get(reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_pk}))  # 支払いを終えずに出品者がアクセス
        self.assertRedirects(response, reverse('neighbor_app:method_of_payment'))  # 支払いページにリダイレクト
        self.client.logout()  # 出品者がログアウト


class QuestionTest(SellFormTest):

    def post_question(self):
        self.post_merchandise()  # 商品を投稿

        # 出品者はログアウト
        self.client.logout()

        # 質問者を作成、ログイン
        self.test_buyer = get_user_model().objects.create_user(
            username='sato_test_buyer',
            email='sato_test_buyer@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )

        self.client.login(email=self.test_buyer.email, password=self.password)  # 質問者がログイン

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk

        response = self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存

        submit_token = response.context['submit_token']  # renderの中から抽出

        # 質問を投稿
        params = {
            'question': '質問_test',
            'submit_token': submit_token,
        }

        self.client.post(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}), params)

        self.assertEqual(MerchandiseQuestion.objects.all().count(), 1)  # 質問が投稿されたかを確認


class AnswerTest(QuestionTest):

    def post_answer(self):
        self.post_question()

        # 質問者はログアウト
        self.client.logout()

        # 回答者（出品者）がログイン
        self.client.login(email=self.test_seller.email, password=self.password)

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk

        response = self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存
        submit_token = response.context['submit_token']  # renderの中から抽出

        question_pk = MerchandiseQuestion.objects.filter(question='質問_test').first().pk

        # 回答を投稿
        params = {
            'answer': '回答_test',
            'question_pk': question_pk,
            'submit_token': submit_token,
        }

        self.client.post(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}), params)

        self.assertEqual(MerchandiseQuestion.objects.filter(answer='回答_test').count(), 1)  # 回答が投稿されたかを確認


class PayTest(SellFormTest):  # カード登録ありの場合

    def pay(self):  # カード登録有り無しでエラーが起こらないか確認
        self.post_merchandise()  # カード登録ありで出品
        self.client.logout()  # 出品者はログアウト
        # 購入者を作成
        self.test_buyer = get_user_model().objects.create_user(
            username='sato_test_buyer',
            email='sato_test_buyer@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )
        self.client.login(email=self.test_buyer.email, password=self.password)  # 購入者がログイン
        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk
        self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存
        response = self.client.post(reverse('neighbor_app:pay'))  # 商品を予約
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Talk.objects.all().count(), 1)  # トークルームが作成されたか確認
        self.assertEqual(Talk.objects.all().first().pay_status, True)  # pay_status=Trueを確認
        self.client.logout()  # ログアウト

    def card_error_test(self):
        user_id = str(self.test_seller.id)
        payjp.Customer.retrieve(user_id).cards.retrieve(str(self.card_id)).delete()  # setUpで登録したカード情報を削除
        DefaultCard.objects.filter(user=self.test_seller).update(default_card_status=False)  # default_card_statusをFalseに

        # トークンを作成(支払い作成時にexpired_cardを返す)
        payjp_token = payjp.Token.create(
            card={
                'number': '4000000000004012',
                'cvc': '123',
                'exp_month': '2',
                'exp_year': '2024',
            },
            headers={'X-Payjp-Direct-Token-Generate': 'true'}
        )

        error_card = payjp.Customer.retrieve(user_id).cards.create(card=str(payjp_token.id), default=True)  # cardオブジェクトを作成
        DefaultCard.objects.filter(user=self.test_seller).update(default_card_status=True)  # default_card_statusをTrueに

        self.post_merchandise()  # 商品を出品

        # 出品者はログアウト
        self.client.logout()

        # 購入者を作成
        self.test_buyer = get_user_model().objects.create_user(
            username='sato_test_buyer',
            email='sato_test_buyer@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )

        self.client.login(email=self.test_buyer.email, password=self.password)  # 購入者がログイン

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk
        self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存
        response = self.client.post(reverse('neighbor_app:pay'))  # 商品を予約

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))

        ####################################################

        self.client.logout()  # 購入者がログアウト
        self.client.login(email=self.test_seller.email, password=self.password)  # 出品者がログイン

        payjp.Customer.retrieve(user_id).cards.retrieve(str(error_card.id)).delete()  # カード情報を削除
        DefaultCard.objects.filter(user=self.test_seller).update(default_card_status=False)  # default_card_statusをFalseに

        # トークンを作成(支払い作成時にcard_declinedを返す)
        payjp_token = payjp.Token.create(
            card={
                'number': '4000000000080319',
                'cvc': '123',
                'exp_month': '2',
                'exp_year': '2024',
            },
            headers={'X-Payjp-Direct-Token-Generate': 'true'}
        )

        error_card = payjp.Customer.retrieve(user_id).cards.create(card=str(payjp_token.id), default=True)  # 新たにcardオブジェクトを作成
        DefaultCard.objects.filter(user=self.test_seller).update(default_card_status=True)  # default_card_statusをTrueに

        self.client.logout()  # 出品者がログアウト
        self.client.login(email=self.test_buyer.email, password=self.password)  # 購入者がログイン

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk
        self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存
        response = self.client.post(reverse('neighbor_app:pay'))  # 商品を予約

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))

        ################################################

        self.client.logout()  # 購入者がログアウト
        self.client.login(email=self.test_seller.email, password=self.password)  # 出品者がログイン

        payjp.Customer.retrieve(user_id).cards.retrieve(str(error_card.id)).delete()  # カード情報を削除
        DefaultCard.objects.filter(user=self.test_seller).update(default_card_status=False)  # default_card_statusをFalseに

        # トークンを作成(支払い作成時にinvalid_expiration_dateを返す)
        payjp_token = payjp.Token.create(
            card={
                'number': '4000000000000077',
                'cvc': '123',
                'exp_month': '2',
                'exp_year': '2024',
            },
            headers={'X-Payjp-Direct-Token-Generate': 'true'}
        )

        payjp.Customer.retrieve(user_id).cards.create(card=str(payjp_token.id), default=True)  # 新たにcardオブジェクトを作成
        DefaultCard.objects.filter(user=self.test_seller).update(default_card_status=True)  # default_card_statusをTrueに

        self.client.logout()  # 出品者がログアウト
        self.client.login(email=self.test_buyer.email, password=self.password)  # 購入者がログイン

        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk
        self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存
        response = self.client.post(reverse('neighbor_app:pay'))  # 商品を予約

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))


class NotCardPayTest(NotCardSellFormTest):  # カード登録無しの場合

    def not_card_pay(self):  # カード登録有り無しでエラーが起こらないか確認
        self.not_card_post_merchandise()  # カード登録なしで出品
        self.client.logout()  # 出品者はログアウト
        # 購入者を作成
        self.test_buyer = get_user_model().objects.create_user(
            username='sato_test_buyer',
            email='sato_test_buyer@dc.tohoku.ac.jp',
            password=self.password,
            university='東北大学',
            profile='よろしくお願いします！',
        )
        self.client.login(email=self.test_buyer.email, password=self.password)  # 購入者がログイン
        merchandise_pk = Merchandise.objects.filter(merchandise_name='商品名_test', explanation='商品の説明_test').first().pk
        self.client.get(reverse('neighbor_app:merchandise_detail', kwargs={'pk': merchandise_pk}))  # ページにアクセスして商品のidをsessionに保存
        response = self.client.post(reverse('neighbor_app:pay'))  # 商品を予約。この時点では支払いしない。
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Talk.objects.all().count(), 1)  # トークルームが作成されたか確認
        self.assertEqual(Talk.objects.all().first().pay_status, False)  # pay_status=Falseを確認
        self.client.logout()  # ログアウト


class RefundTest(ReserveMerchandiseTest):

    def refund_request(self):
        self.reserve_merchandise()  # カード登録ありで予約済み
        talk_room_pk = Talk.objects.filter(talk_buyer=self.test_buyer).first().pk
        response = self.client.get(reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_pk}))  # 支払いを終えて購入者がアクセス
        self.assertEqual(response.status_code, 200)  # アクセスできる

        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'cases': 'はい',
            'image_for_refund': image,
        }

        response = self.client.post(reverse('neighbor_app:refund_request'), params)  # 商品を予約。この時点では支払いしない。
        self.assertTemplateUsed(response, '403.html')  # 購入者はアクセスできない

        self.client.logout()  # 購入者がログアウト
        self.client.login(email=self.test_seller.email, password=self.password)  # 出品者がログイン
        response = self.client.get(reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_pk}))  # 支払いを終えて購入者がアクセス
        self.assertEqual(response.status_code, 200)  # アクセスできる
        response = self.client.post(reverse('neighbor_app:refund_request'), params)  # 商品を予約。この時点では支払いしない。
        self.assertRedirects(response, reverse('neighbor_app:talk_room', kwargs={'pk': talk_room_pk}))  # 返金が成功し、リダイレクト


class NotGetTalkRoomRefundTest(ReserveMerchandiseTest):

    def not_get_talk_room_refund_request(self):  # トークページにアクセスしないで返金処理できないこと確認
        self.reserve_merchandise()  # カード登録ありで予約済み

        # 出品用の画像を引用
        image_path = 'C:\\Users\\sato4\\Downloads\\女子アイコン.png'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        params = {
            'cases': 'はい',
            'image_for_refund': image,
        }

        response = self.client.post(reverse('neighbor_app:refund_request'), params)  # 購入者が返金リクエスト
        self.assertTemplateUsed(response, '500.html')  # talk_roomのsessionがなければアクセスできない

        self.client.logout()  # 購入者がログアウト
        self.client.login(email=self.test_seller.email, password=self.password)  # 出品者がログイン
        response = self.client.post(reverse('neighbor_app:refund_request'), params)  # 出品者が返金リクエスト
        self.assertTemplateUsed(response, '500.html')  # talk_roomのsessionがなければアクセスできない


class LoginInquiryTest(LoggedInTestCaseDefaultCardTrue):

    def inquiry_test(self):

        # 質問を投稿
        params = {
            'name': 'test_name',
            'email': 'test@outlook.jp',
            'content': 'テスト',
        }

        response = self.client.post(reverse('neighbor_app:inquiry', params))
        self.assertEqual(Inquiry.objects.all().count(), 1)  # 質問が投稿されたかを確認
        self.assertRedirects(response, reverse('neighbor_app:inquiry'))


class NotLoginInquiryTest(LoggedInTestCaseDefaultCardTrue):  #ログアウト状態で確認

    def inquiry_test(self):

        self.client.logout()  # ログアウト

        # 質問を投稿
        params = {
            'name': 'test_name',
            'email': 'test@outlook.jp',
            'content': 'テスト',
        }

        response = self.client.post(reverse('neighbor_app:inquiry'), params)
        self.assertEqual(Inquiry.objects.all().count(), 1)  # 質問が投稿されたかを確認
        self.assertRedirects(response, reverse('neighbor_app:inquiry'))


class GetPaymentMethod(LoggedInTestCaseDefaultCardTrue):

    def get_payment_method(self):
        response = self.client.get(reverse('neighbor_app:method_of_payment'))
        self.assertTemplateUsed(response, 'method_of_payment.html')


class DisplayPaymentMethod(LoggedInTestCaseDefaultCardTrue):  # カード登録有り

    def get_payment_method(self):
        response = self.client.get(reverse('neighbor_app:method_of_payment'))
        self.assertTemplateUsed(response, 'method_of_payment.html')
        self.assertNotContains(response, '登録する')
        self.assertContains(response, '更新する')
        self.assertContains(response, '削除する')


class NotCardDisplayPaymentMethod(LoggedInTestCaseDefaultCardFalse):  # カード登録無し

    def get_payment_method(self):
        response = self.client.get(reverse('neighbor_app:method_of_payment'))
        self.assertTemplateUsed(response, 'method_of_payment.html')
        self.assertContains(response, '登録する')
        self.assertNotContains(response, '更新する')
        self.assertNotContains(response, '削除する')


class GetPaymentMethodAfterMatching(ReserveMerchandiseTest):

    def get_payment_method_after_matching(self):
        self.reserve_merchandise()  # カード登録有りでマッチング済み
        self.client.logout()  # ログアウト
        self.client.login(email=self.test_seller.email, password=self.password)  # 出品者がログイン
        response = self.client.get(reverse('neighbor_app:method_of_payment'))
        self.assertNotContains(response, '登録する')
        self.assertContains(response, '更新する')
        self.assertContains(response, '削除する')
        self.assertNotContains(response, 'お支払い方法を登録すると、購入者とマッチングした商品の手数料の支払いが行われます。')


class NotCardGetPaymentMethodAfterMatching(NotCardReserveMerchandiseTest):

    def not_card_get_payment_method_after_matching(self):
        self.not_card_reserve_merchandise()  # カード登録無しでマッチング済み
        self.client.logout()  # ログアウト
        self.client.login(email=self.test_seller.email, password=self.password)  # 出品者がログイン
        response = self.client.get(reverse('neighbor_app:method_of_payment'))
        self.assertContains(response, '登録する')
        self.assertNotContains(response, '更新する')
        self.assertNotContains(response, '削除する')
        self.assertContains(response, 'お支払い方法を登録すると、購入者とマッチングした商品の手数料の支払いが行われます。')


class NotLoginGetPaymentMethod(LoggedInTestCaseDefaultCardTrue):

    def get_payment_method(self):
        self.client.logout()
        response = self.client.get(reverse('neighbor_app:method_of_payment'))
        self.assertEqual(response.status_code, 302)  # ログイン画面にリダイレクト


class SendEmailView(LoggedInTestCaseDefaultCardTrue):  # スーパーユーザでなければ通さない

    def send_email(self):
        response = self.client.get(reverse('neighbor_app:send_email'))
        self.assertTemplateUsed(response, '404.html')


class SuperUserSendEmailView(LoggedInSuperUser):  # スーパーユーザであれば通す

    def send_email(self):
        response = self.client.get(reverse('neighbor_app:send_email'))
        self.assertTemplateUsed(response, 'send_email.html')
