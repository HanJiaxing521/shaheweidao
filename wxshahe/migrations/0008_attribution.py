# Generated by Django 2.0 on 2019-05-30 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wxshahe', '0007_auto_20190530_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diet_name', models.IntegerField()),
                ('attribution1', models.IntegerField()),
                ('attribution2', models.IntegerField()),
                ('attribution3', models.IntegerField()),
                ('attribution4', models.IntegerField()),
                ('attribution5', models.IntegerField()),
                ('attribution6', models.IntegerField()),
                ('attribution7', models.IntegerField()),
                ('attribution8', models.IntegerField()),
                ('attribution9', models.IntegerField()),
                ('diet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wxshahe.Diet')),
            ],
        ),
    ]