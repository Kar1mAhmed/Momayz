from django.contrib import admin
from .models import QA


admin.site.register(QA) 

# Register your models here.
########## UN REGISTER SOME USELESS MODELS FOR ADMIN ######################
from django.contrib.sites.models import Site
admin.site.unregister(Site)

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)



from django.contrib import admin

# Unregister all apps except your own apps
apps_to_exclude = ['daphne', 'channels', 'celery', 'django_celery_results', 'django_celery_beat',
                   'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                   'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                   'django.contrib.sites', 'rest_framework', 'rest_framework.authtoken',
                   'dj_rest_auth', 'dj_rest_auth.registration', 'allauth', 'allauth.account',
                   'allauth.socialaccount']

for app in apps_to_exclude:
    try:
        app_module = __import__(app)
        admin.site.unregister(app_module)
    except Exception:
        pass