# Generated by Django 2.2.7 on 2019-11-21 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='parent',
            field=models.IntegerField(default=-1),
        ),
    ]