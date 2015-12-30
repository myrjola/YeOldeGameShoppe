# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yogsauth', '0001_yogsauth_create_player_and_developer'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False,
                                        verbose_name='ID', primary_key=True)),
                ('activation_key', models.CharField(max_length=40)),
                ('key_expires', models.DateTimeField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
