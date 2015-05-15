# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=140)),
                ('button', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=256)),
                ('amount', models.IntegerField(choices=[(1, b'One finger'), (2, b'Two fingers'), (3, b'Down your drink')])),
            ],
        ),
    ]
