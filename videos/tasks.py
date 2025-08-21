import subprocess
import os
import subprocess
from django.conf import settings
from .models import Video

def convert_480p(source):
    new_file_name = source[:-4] + "_480p.mp4"
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    subprocess.run(cmd,shell=True)
    
    

def generate_thumbnail(video_id):
    video = Video.objects.get(id=video_id)
    input_path = video.file.path

    output_dir = os.path.join(settings.MEDIA_ROOT, "thumbnails") 
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{video.id}.jpg") 

    command = [
        "ffmpeg",                   # Aufruf von ffmpeg (Videoverarbeitungsprogramm)
        "-ss", "00:00:05.000",      # Springe zu 5 Sekunden im Video
        "-i", input_path,           # Eingabevideo (Pfad zur Videodatei)
        "-vframes", "1",            # Erzeuge genau 1 Einzelbild
        "-q:v", "2",                # Bildqualität (2 = sehr gut, kleiner = besser)
        output_path,                # Ausgabepfad für das Thumbnail
        "-update", "1",         # wichtig für Docker: überschreibt existierende Datei
    ]


    subprocess.run(command, check=True)

    # Pfad im Model speichern
    video.thumbnail_url = f"http://127.0.0.1:8000/media/thumbnails/{video.id}.jpg"
    video.save()
