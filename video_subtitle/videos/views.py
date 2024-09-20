import os
import logging
import ffmpeg
import re
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Video, Subtitle
from .forms import VideoUploadForm

def list_videos(request):
    """List view for uploaded videos."""
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def upload_video(request):
    """Upload a new video."""
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            error_message = extract_subtitles(video)
            if error_message:
                return HttpResponse(f"Failed to extract subtitles: {error_message}")
            return redirect('list_videos')
    else:
        form = VideoUploadForm()
    
    return render(request, 'video_upload.html', {'form': form})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    selected_language = request.GET.get('language', 'en')# check if eng 
    search_query = request.GET.get('q', '')

    subtitles = Subtitle.objects.filter(video=video, language=selected_language)

    if search_query:
        subtitles = subtitles.filter(text__icontains=search_query)
        message = f'Found "{search_query}" in the subtitles.'
    else:
        message = 'No search query provided. Or select the Subtitle first'

    # Fetch available languages
    languages = Subtitle.objects.filter(video=video).values_list('language', flat=True).distinct()

    context = {
        'video': video,
        'subtitles': subtitles,
        'selected_language': selected_language,
        'search_query': search_query,
        'message': message,
        'languages': languages,
    }

    return render(request, 'search_results.html', context)

def search_subtitles(request, video_id):
    """Search within the subtitles of a specific video."""
    video = get_object_or_404(Video, pk=video_id)
    query = request.GET.get('q', '')
    logging.debug(f"Search query: {query}")

    subtitles = Subtitle.objects.filter(video=video, text__icontains=query) if query else []

    context = {
        'video': video,
        'subtitles': subtitles,
        'search_query': query,
        'message': f'Found "{query}" in the following subtitles:' if subtitles else f'No match found for "{query}".',
        'languages': Subtitle.objects.filter(video=video).values_list('language', flat=True).distinct(),
        'selected_language': 'en'  # Defaulting to 'en', but could be dynamic
    }

    return render(request, 'search_results.html', context)


def extract_subtitles(video):
    video_path = video.video_file.path
    output_dir = os.path.join('media', 'subtitles')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Probe the video file for subtitle streams
        probe = ffmpeg.probe(video_path)
        subtitle_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle']
        
        if not subtitle_streams:
            return "This file has no subtitles to process."
        
        # Extract subtitles for each subtitle stream
        for index, stream in enumerate(subtitle_streams):
            language = stream.get('tags', {}).get('language', f'lang_{index}')
            output_path = os.path.join(output_dir, f"{video.title}_{language}.srt")

            # Extract subtitles
            process = (
                ffmpeg
                .input(video_path)
                .output(output_path, **{'c:s': 'copy', 'map': f'0:s:{index}'})
                .run(capture_stdout=True, capture_stderr=True)
            )
            save_subtitles_to_db(video, output_path, language)
        
        return None

    except ffmpeg.Error as e:
        error_message = e.stderr.decode('utf8')
        logging.error(f"ffmpeg error: {error_message}")
        return f"ffmpeg error: {error_message}"

def save_subtitles_to_db(video, subtitle_path, language='en'):
    try:
        with open(subtitle_path, 'r', encoding='utf-8') as subtitle_file:
            subtitle_content = subtitle_file.read()
        
        subtitles = parse_srt(subtitle_content, video, language)
        Subtitle.objects.bulk_create(subtitles)
        logging.info(f"Subtitles saved for video {video.title}")
    except Exception as e:
        logging.error(f"Failed to save subtitles to the database: {str(e)}")
        raise

def convert_srt_time_to_seconds(srt_time):
    """Convert SRT time format to seconds."""
    try:
        if ',' in srt_time:
            h, m, s_ms = srt_time.split(':')
            s, ms = s_ms.split(',')
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
        else:
            parts = srt_time.split(':')
            if len(parts) == 2:  # MM:SS format
                m, s = parts
                return int(m) * 60 + float(s)
            elif len(parts) == 1:  # SS,MS format
                return float(parts[0])
    except ValueError as e:
        logging.error(f"Error parsing time '{srt_time}': {e}")
        return 0

def parse_srt(content, video, language='en'):
    """Parse the SRT file content and save the subtitles with correct timestamps."""
    subtitles = []
    pattern = re.compile(r'(\d+)\n(\d{1,2}:\d{2}:\d{2},\d{3}|\d{1,2}:\d{2}.\d+|\d{1,2},\d+|\d+)\s-->\s(\d{1,2}:\d{2}:\d{2},\d{3}|\d{1,2}:\d{2}.\d+|\d{1,2},\d+|\d+)\n(.*?)\n', re.DOTALL)
    matches = pattern.findall(content)
    
    for match in matches:
        start_time_str = match[1]
        text = match[3].replace('\n', ' ')
        start_time = convert_srt_time_to_seconds(start_time_str)

        subtitles.append(Subtitle(
            video=video,
            text=text,
            start_time=str(start_time),  # Store as string for compatibility
            language=language
        ))

    return subtitles
