# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('yogsauth', '0002_emailvalidation'), ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='iban',
            field=models.CharField(
                max_length=34,
                verbose_name='IBAN',
                default='default_iban',
                help_text='Your sales proceedings will be paid here.'),
            preserve_default=False, ),
        migrations.AddField(
            model_name='developer',
            name='swift',
            field=models.CharField(max_length=11,
                                   verbose_name='SWIFT or BIC code',
                                   default='default_bic'),
            preserve_default=False, ),
    ]
