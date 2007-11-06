#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Default Django settings for an iki app (web or else :?). You'll have to
import anything from here to construct your settings.py for web deployment.

.. sourcecode:: python

   from iki.conf.settings import *

   ROOT_URLCONF = 'iki.urls'

   TIME_ZONE = "Europe/Oslo"

   INSTALLED_APPS += { #...
   }

"""
import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Example coco', 'coco@example.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Paris'

DEFAULT_CHARSET = 'utf-8'
DEFAULT_CONTENT_TYPE = 'text/html'

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True

ADMIN_MEDIA_PREFIX = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',)

#To define in your settings.py
#ROOT_URLCONF = 'iki.urls'

IKI_ROOT = os.path.abspath(os.path.split(__file__)[0])

MEDIA_ROOT = '/var/media/iki'
STATIC_ROOT = MEDIA_ROOT
MEDIA_URL = '/'

TEMPLATE_DIRS = (
    os.path.join(IKI_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'tagging',
    'iki.core.metadata',
)

# Django built-in system for users, ok ?
# FIXME: openid too
BUILTIN_AUTH = True
LOGIN_URL = '/account/login'
AUTH_PROFILE_MODULE = 'accounts.Profile'

# Cache backend options
CACHE_EXPIRATION_TIME = 60 * 60 * 24 * 30 # 1 month

# Custom test runner, using nose to find tests and execute them. Why not ?!
# I'll try it, stolen from reviewboard :D
# Or should we use the django test built-in.. well.. 
#TEST_RUNNER = 'iki.test.runner'

# Default settings for iki
#TODO: move them somewhere else (in the media module..)
MEDIA_BY_PAGE = 10
MAX_MEDIA_BY_PAGE = 150
PHOTO_THUMB = {
   'PHOTO_LARGE_THUMB' : (700, 700),
   'PHOTO_AVG_THUMB' : (300,300),
   'PHOTO_MIN_THUMB' : (60, 60),
}
# Default Licence for media
DEFAULT_LICENCE = 'copyright'
# User profile choices
USER_GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('B', 'Both'),
    )
USER_SINGLENESS_CHOICES = (
    ('S', 'Single'),
    ('T', 'Taken'),
    ('O', 'Open'),
    ('R', 'Rather not say'),
    )
USER_ORDER_CHOICES = (
    ('D', 'Date'),
    ('A', 'Alphabetical'),
    ('R', 'Rated'),
    )
USER_MAJORITY = 18
