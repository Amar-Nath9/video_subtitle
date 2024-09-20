from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='subtitles')
    text = models.TextField()
    start_time = models.DurationField()  # HH:MM:SS,MS format
    end_time = models.DurationField(null=True)  # Temporarily allow nulls
   # Add end_time for subtitles
    language = models.CharField(max_length=10, default='en')

    def __str__(self):
        return f'{self.start_time} --> {self.end_time}: {self.text}'
