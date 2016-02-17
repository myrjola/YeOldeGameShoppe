# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('yogsauth', '0004_optional_gamertag'), ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='gamertag',
            field=models.CharField(help_text=
                                   'Optional name to show in high-scores.',
                                   max_length=32,
                                   blank=True,
                                   null=True), ),
    ]
