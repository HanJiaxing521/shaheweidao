# Generated by Django 2.0 on 2019-05-30 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxshahe', '0011_auto_20190530_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]