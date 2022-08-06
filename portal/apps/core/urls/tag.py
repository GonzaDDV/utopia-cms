# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from core.views.tag import tag_detail


urlpatterns = [
    url(r'^(?P<tag_slug>[\w-]+)/$', tag_detail, name='tag_detail'),
]
