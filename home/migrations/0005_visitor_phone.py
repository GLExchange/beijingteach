# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20160109_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='phone',
            field=models.CharField(default=b'', max_length=16),
        ),
    ]
