# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yogsgame', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='developer',
        ),
        migrations.AlterField(
            model_name='highscore',
            name='id',
            field=models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True),
        ),
    ]
