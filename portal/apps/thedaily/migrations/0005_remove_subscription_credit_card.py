# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-02 02:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thedaily', '0004_auto_20210615_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='credit_card',
        ),
    ]