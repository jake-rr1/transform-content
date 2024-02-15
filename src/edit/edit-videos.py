from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
from dotenv import load_dotenv

load_dotenv('..\\upload\\inputs.txt')

current_dir = os.path.dirname(os.path.realpath(__file__))
user = os.getenv('USER')
path_to_videos = current_dir + f'\\videos-{user}'

for vid in os.listdir(path_to_videos):
    # Get the desired video title
    title = vid.split('-')[1].split('.')[0]

    # Open the video and audio
    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("audio.mp3")

    # Concatenate the video clip with the audio clip
    final_clip = video_clip.set_audio(audio_clip)

    # Export the final video with audio
    final_clip.write_videofile(title + ".mp4")	