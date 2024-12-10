# Generated by Django 5.1.3 on 2024-12-09 04:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('profile1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile1', to='project.userprofile')),
                ('profile2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile2', to='project.userprofile')),
            ],
        ),
    ]
