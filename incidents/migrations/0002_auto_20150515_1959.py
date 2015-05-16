# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='stage',
            field=models.IntegerField(default=1, choices=[(1, b'During the performance'), (2, b'During the scoring')]),
        ),
        migrations.AlterField(
            model_name='incident',
            name='amount',
            field=models.IntegerField(default=1, choices=[(1, b'One finger'), (2, b'Two fingers'), (3, b'Down your drink')]),
        ),
    ]
