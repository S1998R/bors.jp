from django import forms
from .models import Merchandise, Talk, Inquiry, OpenComment, Report, MerchandiseQuestion, Announce
from accounts.models import CustomUser, Faculty, Department


class SellForm(forms.ModelForm):
    image = forms.ImageField(label='商品の画像', required=False)
    image_2 = forms.ImageField(label='商品の画像2', required=False)
    image_3 = forms.ImageField(label='商品の画像3', required=False)
    image_4 = forms.ImageField(label='商品の画像4', required=False)
    image_5 = forms.ImageField(label='商品の画像5', required=False)
    image_6 = forms.ImageField(label='商品の画像6', required=False)
    image_7 = forms.ImageField(label='商品の画像7', required=False)
    image_8 = forms.ImageField(label='商品の画像8', required=False)
    image_9 = forms.ImageField(label='商品の画像9', required=False)
    image_10 = forms.ImageField(label='商品の画像10', required=False)
    merchandise_name = forms.CharField(label='商品名', widget=forms.TextInput())
    value = forms.IntegerField(label='商品の価格')  # 最大値、最小値を制限
    explanation = forms.CharField(label='詳細', widget=forms.Textarea(attrs={'style':'resize:none'}))
    region = forms.CharField(label='商品の受け渡し可能なエリア', widget=forms.TextInput(attrs={'placeholder': '○〇キャンパス、○○大学周辺など'}))

    class Meta:
        model = Merchandise
        fields = ('image', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'image_7', 'image_8', 'image_9', 'image_10', 'merchandise_name', 'value', 'explanation', 'class_name', 'category', 'region', 'merchandise_status')


class SearchForm(forms.Form):

    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "検索"}))

    class Meta:
        fields = ('search',)


class TalkRoomForm(forms.ModelForm):

    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': '商品を受け取る・渡す日時、場所等を決めましょう！', 'style': 'resize:none', 'rows': 4}), required=False)

    class Meta:
        model = Talk
        fields = ('comment',)


class AccountEditForm(forms.ModelForm):

    profile = forms.CharField(label='プロフィール', widget=forms.Textarea(attrs={'style': 'resize:none', 'rows': 4}))

    class Meta:
        model = CustomUser
        fields = ('profile',)


class TenantForm(forms.Form):
    SELECTION1 = (
        ('普通', '普通'),
        ('当座', '当座'),
        ('貯蓄', '貯蓄'),
    )

    bank_code = forms.IntegerField(label="銀行コード", widget=forms.NumberInput(attrs={'placeholder': "例) 1234(数字4ケタ)"}))
    bank_branch_code = forms.IntegerField(label="支店コード", widget=forms.NumberInput(attrs={'placeholder': "例) 123(数字3ケタ)"}))
    bank_account_type = forms.ChoiceField(label='預金種別', choices=SELECTION1)
    bank_account_number = forms.IntegerField(label="口座番号", widget=forms.NumberInput(attrs={'placeholder': "例) 1234567(数字7ケタ)"}))
    bank_account_holder_name = forms.CharField(label="口座名義", widget=forms.TextInput(attrs={'placeholder': "例) ヤマダ タロウ"}))

    class Meta:
        fields = ('bank_code', 'bank_branch_code', 'bank_account_type', 'bank_account_number', 'bank_account_holder_name')


class InquiryForm(forms.ModelForm):

    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'できる限り具体的に入力して下さい。', 'style': 'resize:none'}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={'placeholder': '正確に入力して下さい。'}))
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '例）ヤマダ タロウ'}))

    class Meta:
        model = Inquiry
        fields = ('name', 'email', 'content',)


class OpenCommentForm(forms.ModelForm):

    comment = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'コメントで商品について質問、回答できます。', 'style': 'resize:none', 'rows': 4}))

    class Meta:
        model = OpenComment
        fields = ('comment',)


class ReportForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': '通報内容をできる限り具体的にご入力下さい。', 'style': 'resize:none', 'rows': 4}))

    class Meta:
        model = Report
        fields = ('content',)


class MerchandiseQuestionForm(forms.ModelForm):
    question = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': '商品について質問できます。質問はこの商品ページで全ユーザーに公開されます。', 'style': 'resize:none', 'rows': 4}), required=True)

    class Meta:
        model = MerchandiseQuestion
        fields = ('question',)


class MerchandiseAnswerForm(forms.ModelForm):
    answer = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': '質問に回答しましょう', 'style': 'resize:none', 'rows': 4}), required=True)

    class Meta:
        model = MerchandiseQuestion
        fields = ('answer',)


class EmailRequestForm(forms.ModelForm):

    SELECTION1 = (
        ('True', 'はい'),
        ('False', 'いいえ'),
    )

    email_permission = forms.ChoiceField(label='', choices=SELECTION1)

    class Meta:
        model = CustomUser
        fields = ('email_permission',)


class AnnounceForm(forms.ModelForm):

    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 10}), required=True)

    class Meta:
        model = Announce
        fields = ('title', 'content')


class FacultyForm(forms.ModelForm):

    faculty = forms.ChoiceField(label='学部',)

    class Meta:
        model = Faculty
        fields = ('faculty',)

    def __init__(self, selection=None, *args, **kwargs):
        self.base_fields["faculty"].choices = selection
        super().__init__(*args, **kwargs)


class DepartmentForm(forms.ModelForm):

    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 10}), required=True)

    class Meta:
        model = Announce
        fields = ('title', 'content')


class TestSellForm(forms.Form):

    SELECTION1 = (
        ('', '選択して下さい'),
        ('textbook', '教科書'),
        ('other', 'その他'),
    )

    SELECTION2 = (
        ('', '選択して下さい'),
        ('未使用', '未使用'),
        ('新品に近い', '新品に近い'),
        ('良い', '良い'),
        ('可', '可'),
    )

    SELECTION3 = (
        ('', '選択して下さい'),
        ('', '追加する'),
    )

    image = forms.ImageField(label='商品の画像', required=False)
    image_2 = forms.ImageField(label='商品の画像2', required=False)
    image_3 = forms.ImageField(label='商品の画像3', required=False)
    image_4 = forms.ImageField(label='商品の画像4', required=False)
    image_5 = forms.ImageField(label='商品の画像5', required=False)
    image_6 = forms.ImageField(label='商品の画像6', required=False)
    image_7 = forms.ImageField(label='商品の画像7', required=False)
    image_8 = forms.ImageField(label='商品の画像8', required=False)
    image_9 = forms.ImageField(label='商品の画像9', required=False)
    image_10 = forms.ImageField(label='商品の画像10', required=False)
    merchandise_name = forms.CharField(label='商品名', widget=forms.TextInput())
    value = forms.IntegerField(label='商品の価格', min_value=0)  # 最大値、最小値を制限
    explanation = forms.CharField(label='詳細', widget=forms.Textarea(attrs={'style':'resize:none', 'placeholder': '定価や汚れ具合の詳細など'}))
    region = forms.CharField(label='商品の受け渡し可能なエリア', widget=forms.TextInput(attrs={'placeholder': '○〇キャンパス周辺、配送可・不可など'}))
    category = forms.ChoiceField(label='カテゴリ', choices=SELECTION1)
    merchandise_status = forms.ChoiceField(label='商品の状態', choices=SELECTION2)
    faculty = forms.ChoiceField(label='学部',)
    department = forms.ChoiceField(label='学科', choices=SELECTION3)

    def __init__(self, selection=None, *args, **kwargs):
        self.base_fields["faculty"].choices = selection
        super().__init__(*args, **kwargs)


class TestSellFormEdit(forms.Form):

    SELECTION1 = (
        ('', '選択して下さい'),
        ('textbook', '教科書'),
        ('other', 'その他'),
    )

    SELECTION2 = (
        ('', '選択して下さい'),
        ('未使用', '未使用'),
        ('新品に近い', '新品に近い'),
        ('良い', '良い'),
        ('可', '可'),
    )

    image = forms.ImageField(label='商品の画像', required=False)
    image_2 = forms.ImageField(label='商品の画像2', required=False)
    image_3 = forms.ImageField(label='商品の画像3', required=False)
    image_4 = forms.ImageField(label='商品の画像4', required=False)
    image_5 = forms.ImageField(label='商品の画像5', required=False)
    image_6 = forms.ImageField(label='商品の画像6', required=False)
    image_7 = forms.ImageField(label='商品の画像7', required=False)
    image_8 = forms.ImageField(label='商品の画像8', required=False)
    image_9 = forms.ImageField(label='商品の画像9', required=False)
    image_10 = forms.ImageField(label='商品の画像10', required=False)
    merchandise_name = forms.CharField(label='商品名', widget=forms.TextInput())
    value = forms.IntegerField(label='商品の価格', min_value=0)  # 最大値、最小値を制限
    explanation = forms.CharField(label='詳細', widget=forms.Textarea(attrs={'style':'resize:none', 'placeholder': '定価や汚れ具合の詳細など'}))
    region = forms.CharField(label='商品の受け渡し可能なエリア', widget=forms.TextInput(attrs={'placeholder': '○〇キャンパス周辺、配送可・不可など'}))
    category = forms.ChoiceField(label='カテゴリ', choices=SELECTION1)
    merchandise_status = forms.ChoiceField(label='商品の状態', choices=SELECTION2)
    faculty = forms.ChoiceField(label='学部',)
    department = forms.ChoiceField(label='学科',)

    def __init__(self, faculty_selection=None, department_selection=None, merchandise_name=None, value=None, category=None, explanation=None, merchandise_status=None, region=None, faculty=None, department=None, *args, **kwargs):
        self.base_fields["faculty"].choices = faculty_selection
        self.base_fields["department"].choices = department_selection
        self.base_fields["merchandise_name"].initial = merchandise_name
        self.base_fields["value"].initial = value
        self.base_fields["category"].initial = category
        self.base_fields["explanation"].initial = explanation
        self.base_fields["merchandise_status"].initial = merchandise_status
        self.base_fields["region"].initial = region
        self.base_fields["faculty"].initial = faculty
        self.base_fields["department"].initial = department

        super().__init__(*args, **kwargs)