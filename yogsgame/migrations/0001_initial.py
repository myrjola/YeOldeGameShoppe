# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yogsauth', '0003_developerfields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True,
                                        verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=256, unique=True)),
                ('price', models.DecimalField(decimal_places=2,
                                              max_digits=10)),
                ('url', models.URLField()),
                ('developer', models.ForeignKey(to='yogsauth.Developer')),
            ],
        ),
        migrations.CreateModel(
            name='GameLicense',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True,
                                        verbose_name='ID', serialize=False)),
                ('purchase_price', models.DecimalField(decimal_places=2,
                                                       max_digits=10)),
                ('bought_at', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(to='yogsgame.Game')),
                ('player', models.ForeignKey(to='yogsauth.Player')),
            ],
        ),
        migrations.CreateModel(
            name='HighScore',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True,
                                        verbose_name='id', serialize=False)),
                ('score', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(to='yogsgame.Game')),
                ('player', models.ForeignKey(to='yogsauth.Player')),
            ],
        ),
    ]
