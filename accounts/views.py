from allauth.account.utils import complete_signup
from allauth.account.views import SignupView
from allauth.exceptions import ImmediateHttpResponse
from allauth.account import app_settings
from .models import CustomUser
import datetime
from dateutil.relativedelta import relativedelta


class OriginalSignupView(SignupView):
    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        email = self.user.email
        user = CustomUser.objects.get(email=email)
        birthday = self.user.birthday
        d0 = birthday  # 生年月日
        d1 = datetime.date.today()  # 現在の日付
        dy = relativedelta(d1, d0)  # 経過時間
        user.age = dy.years  # 年齢をモデルに保存
        if dy.years < 20:
            user.abstract_age = '10代'
        elif dy.years < 30:
            user.abstract_age = '20代'
        elif dy.years < 40:
            user.abstract_age = '30代'
        elif dy.years < 50:
            user.abstract_age = '40代'
        elif dy.years < 60:
            user.abstract_age = '50代'
        elif dy.years < 70:
            user.abstract_age = '60代'
        elif dy.years < 80:
            user.abstract_age = '70代'
        elif dy.years < 90:
            user.abstract_age = '80代'
        elif dy.years < 100:
            user.abstract_age = '90代'
        else:
            user.abstract_age = '100歳以上'
        user.save()


        try:
            return complete_signup(
                self.request, self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url())
        except ImmediateHttpResponse as e:
            return e.response