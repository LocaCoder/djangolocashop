# Generated by Django 5.0.7 on 2024-08-05 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_created_comment_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='package',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='p_commits', to='main.package'),
            preserve_default=False,
        ),
    ]
