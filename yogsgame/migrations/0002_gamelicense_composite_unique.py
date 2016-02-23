# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yogsgame', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highscore',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterUniqueTogether(
            name='gamelicense',
            unique_together=set([('game', 'player')]),
        ),
    ]
