# Generated by Django 2.0 on 2019-05-30 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxshahe', '0008_attribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribution',
            name='diet_name',
            field=models.TextField(),
        ),
    ]
