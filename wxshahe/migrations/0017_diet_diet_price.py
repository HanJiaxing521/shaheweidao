# Generated by Django 2.2.1 on 2019-08-06 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxshahe', '0016_auto_20190531_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='diet',
            name='diet_price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]