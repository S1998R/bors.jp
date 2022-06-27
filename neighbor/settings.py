"""
Django settings for neighbor project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import payjp

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ADMIN_PATH = os.environ.get('ADMIN_PATH')
ALLOWED_ADMIN = os.environ.get('IP_ADDRESS')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
    # os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'neighbor_app.apps.NeighborAppConfig',
    'accounts.apps.AccountsConfig',

    'django.contrib.sites',
    'allauth',
    'allauth.account',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'neighbor_app.middleware.AdminProtect',  # 自作、Adminのセキュリティー設定
]

ROOT_URLCONF = 'neighbor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'neighbor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'neighbor',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# ロギング設定
LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # neighbor_appアプリケーションが利用するロガー
        'neighbor_app': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },

    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

#ユーザーモデルをカスタムユーザーとして定義
AUTH_USER_MODEL = 'accounts.CustomUser'

#メールをコンソールに出力する設定
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-allauthで利用するdjango.contrib.sitesを使うためにサイト識別用IDを設定
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',  # 一般ユーザー用(メールアドレス認証)
    'django.contrib.auth.backends.ModelBackend',  # 管理サイト用(ユーザー名認証)
)

# メールアドレス認証に変更する設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = True

# サインアップにメールアドレス確認を挟むよう設定
# これにより、emailから確認を押さないとログインできなくなる。
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

# ログイン/ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = 'neighbor_app:top'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'


# メール認証の確認ボタンを押したら自動でログインした扱いになる設定（確定ボタン押したときに、もう一度ログイン画面を経由しない。）
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 画像保存パスの指定
MEDIA_URL = '/media/'

# signupformを指定(新規登録で年齢フォームを作成するのに必要)
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}

# signupformからの情報をcustomusermodelに保存するのに必要(新規登録で年齢フォームを作成するのに必要)
ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

# PAY.JP設定
payjp.api_key = os.environ['API_KEY']  # テスト用秘密鍵

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# SESSION_COOKIE_AGE = 1  # 1秒
SESSION_COOKIE_AGE = 1209600  # 2週間

SESSION_SAVE_EVERY_REQUEST = True

# python-memcachedをインストール
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# allauthからのメールの送信元アドレスの設定（これが無いとwebmaster@localhostとなる）
DEFAULT_FROM_EMAIL = os.environ.get('INFO_EMAIL')

BACKUP_PATH = 'backup/'

SESSION_COOKIE_NAME = 'bors'

# パスワードを連続で10回失敗した時、30分ログインできない
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60 * 30
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60 * 60 * 24 * 7

# セキュリティー対策
SESSION_COOKIE_HTTPONLY = True  # sessionがjavascriptで取得できない設定

ACCOUNT_SESSION_REMEMBER = True # 自動でアカウントのセッションを保持(いちいちユーザーネームとパスワードを要求しない)