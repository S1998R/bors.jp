from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser, University
import datetime
from django.core.exceptions import ValidationError


def univ_validate_confirm(value):  # 大学のバリデーション

    if value == "":
        raise ValidationError(
            "所属する大学を選択して下さい。",
            params={'value': value},
        )

    return value


class CustomSignupForm(SignupForm):
    class Meta:
        model = CustomUser

    def signup(self, request, user):
        user.university = self.cleaned_data['university']
        user.save()
        return user

    university = forms.ChoiceField(label='大学', choices=[("", "選択してください")] + [(i.university, i.university) for i in University.objects.all().order_by('university')], widget=forms.widgets.Select, required=True, validators=[univ_validate_confirm])
    email = forms.EmailField(label='メールアドレス', required=True, widget=forms.TextInput(attrs={'placeholder': 'メールアドレス'}))

    field_order = ['username', 'email', 'password1', 'password2', 'university']

    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()
        university = cleaned_data.get("university")
        email = cleaned_data.get("email")

        if not university:  # 上のvalidatorsの関数でバリデーションにかかると、ここがNoneになるので以下でエラーを防ぐためにreturnする
            return cleaned_data

        if not email:  # 上のvalidatorsの関数でバリデーションにかかると、ここがNoneになるので以下でエラーを防ぐためにreturnする
            return cleaned_data

        university_domain = University.objects.filter(university=university).first().email_domain

        if not university_domain in email:  # 選択した大学とドメインが一致しなければバリデーションエラー

            raise forms.ValidationError("大学とドメインが一致しません。" + university_domain + "のドメインで登録してください。")

        return cleaned_data
