# Generated by Django 2.0 on 2019-05-29 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxshahe', '0003_auto_20190529_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diet',
            name='diet_brief_content',
        ),
    ]
