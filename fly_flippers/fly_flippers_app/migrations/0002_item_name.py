# Generated by Django 3.2.3 on 2021-09-08 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fly_flippers_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(default='null', max_length=100),
        ),
    ]