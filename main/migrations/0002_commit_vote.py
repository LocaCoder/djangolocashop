# Generated by Django 5.0.7 on 2024-07-27 08:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_reply', models.BooleanField(default=False)),
                ('body', models.TextField(max_length=400)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p_commits', to='main.package')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_commits', to='main.commit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u_commits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p_vote', to='main.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u_vote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
