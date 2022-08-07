from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-v1c_aza%(hsh^dfbwefuihg42fh4**&Joiddducq#(a7h!90#e%v1!8o'

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tgbot_ew',
        'USER': 'romancvc',
        'PASSWORD': '21761815',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}