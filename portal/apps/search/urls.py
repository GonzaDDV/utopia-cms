# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import *
from search.views import search

urlpatterns = [
    url(r'^$', search, name='search'),
    url(r'^(?P<token>.+)/$', search, name='search_terms'),
]
