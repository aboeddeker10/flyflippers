# Generated by Django 3.2.3 on 2021-09-18 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fly_flippers_app', '0007_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='gear/'),
        ),
    ]
