# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('yogsauth', '0005_gamertag_not_unique'), ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='gamertag',
            field=models.CharField(
                blank=True,
                null=True,
                help_text='Optional name to show in high-scores.',
                max_length=32), ),
    ]
