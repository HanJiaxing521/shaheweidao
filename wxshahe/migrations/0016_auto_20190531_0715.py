# Generated by Django 2.0 on 2019-05-30 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxshahe', '0015_cluster'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField()),
                ('group', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Cluster',
        ),
    ]
