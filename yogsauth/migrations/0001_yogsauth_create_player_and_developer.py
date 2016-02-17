# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        primary_key=True,
                                        serialize=False,
                                        auto_created=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ], ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        primary_key=True,
                                        serialize=False,
                                        auto_created=True)),
                ('gamertag', models.CharField(max_length=32,
                                              unique=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ], ),
    ]
