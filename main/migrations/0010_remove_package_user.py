# Generated by Django 5.0.7 on 2024-08-09 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_subscriptionbuy_options_alter_package_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='user',
        ),
    ]
