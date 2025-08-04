import subprocess

def convert_480p(source):
    new_file_name = source[:-4] + "_480p.mp4"
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    # cmd = [
    # "ffmpeg",
    # "-i", "/app/media/uploads/video1_AtvN1IP.mp4",
    # "-s", "hd480",
    # "-c:v", "libx264",
    # "-crf", "23",
    # "-c:a", "aac",
    # "-strict", "-2",
    # "/app/media/uploads/video1_AtvN1IP_480p.mp4"
    # ]
    print("lääuufftt")
    subprocess.run(cmd,shell=True)