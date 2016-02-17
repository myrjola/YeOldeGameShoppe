# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('yogsauth', '0003_developerfields'), ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='gamertag',
            field=
            models.CharField(blank=True,
                             null=True,
                             unique=True,
                             help_text='Optional name to show in highscores',
                             max_length=32), ),
    ]
