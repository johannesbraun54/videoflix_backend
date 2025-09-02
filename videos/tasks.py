import subprocess
import os
import subprocess
from django.conf import settings
from .models import Video
import subprocess

def generate_thumbnail(video_id):
    video = Video.objects.get(id=video_id)
    input_path = video.file.path

    output_dir = os.path.join(settings.MEDIA_ROOT, "thumbnails") 
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{video.id}.jpg") 

    cmd = [
        "ffmpeg",                  
        "-ss", "00:00:05.000",    
        "-i", input_path,
        "-vframes", "1",            
        "-q:v", "2",                
        output_path,               
        "-update", "1",       
    ]

    subprocess.run(cmd, check=True)

    video.thumbnail_url = f"https://videoflix-backend.jb-webdevelopment.com/media/thumbnails/{video.id}.jpg"
    video.save()
    
def convert_video_into_specific_resolution(resolution, scale, input_file, video_id):
    output_dir = os.path.join(settings.MEDIA_ROOT, "videos", str(video_id), resolution)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "index.m3u8")

    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"scale={scale}",
        "-c:v", "h264",       # Video-Codec
        "-c:a", "aac",        # Audio-Codec
        "-f", "hls",          # Ausgabeformat
        "-hls_time", "10",    # Segmentlänge 10 Sekunden
        "-hls_playlist_type", "vod",  # VoD-Playlist
        output_file
    ]
    
    subprocess.run(cmd, check=True)
    
    
def convert_video_into_hls(input_file, video_id):
    
    RESOLUTION_MAP = {
        "480p": "854:480",
        "720p": "1280:720",
        "1080p": "1920:1080",
    }    

    for resolution, scale in RESOLUTION_MAP.items():
        convert_video_into_specific_resolution(resolution, scale, input_file, video_id)
        
    return True
