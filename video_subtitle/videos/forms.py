from django import forms
from .models import Video

# Form for uploading a video
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']

# Form for searching subtitles
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Search for subtitles')
