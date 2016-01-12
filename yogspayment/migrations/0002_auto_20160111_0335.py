# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yogspayment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='developer',
        ),
        migrations.RemoveField(
            model_name='gamelicense',
            name='game',
        ),
        migrations.RemoveField(
            model_name='gamelicense',
            name='player',
        ),
        migrations.RemoveField(
            model_name='highscore',
            name='game',
        ),
        migrations.RemoveField(
            model_name='highscore',
            name='player',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
        migrations.DeleteModel(
            name='GameLicense',
        ),
        migrations.DeleteModel(
            name='HighScore',
        ),
    ]
