# Generated by Django 5.1.1 on 2024-09-13 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_video_subtitles_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='subtitles_file',
        ),
    ]
