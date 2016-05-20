# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_pagepos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippetpos',
            name='snippet',
        ),
        migrations.DeleteModel(
            name='Snippet',
        ),
        migrations.DeleteModel(
            name='SnippetPos',
        ),
    ]
