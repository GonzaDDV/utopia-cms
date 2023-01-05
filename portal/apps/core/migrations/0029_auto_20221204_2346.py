# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-12-04 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20221017_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='ipfs_cid',
            field=models.TextField(blank=True, help_text='CID de la nota en IPFS', null=True, verbose_name='id de IPFS'),
        ),
        migrations.AddField(
            model_name='article',
            name='ipfs_upload',
            field=models.BooleanField(default=False, verbose_name='Publicar en IPFS'),
        ),
        migrations.AddField(
            model_name='article',
            name='solana_signature',
            field=models.TextField(blank=True, help_text='Firma del autor en Solana', null=True, verbose_name='Firma de Solana'),
        ),
        migrations.AddField(
            model_name='article',
            name='solana_signature_address',
            field=models.TextField(blank=True, help_text='Wallet autora de la firma en Solana', null=True, verbose_name='Wallet de Solana'),
        ),
    ]
