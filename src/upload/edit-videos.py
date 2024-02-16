from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os
from dotenv import load_dotenv
import subprocess
from elevenlabs import Voice, VoiceSettings, voices, save, generate
from termcolor import colored


def mp4_to_mov(movie_path) -> None:
    for fn in os.listdir(movie_path):
        print("Converting " + movie_path + fn + " to .mov file")
        print(fn[:-4])
        if os.path.isfile(movie_path + fn):
            if fn.endswith(".mp4"):
                cmd = ["ffmpeg",
                    "-i", movie_path + fn,
                    "-n",
                    "-acodec", "copy",
                    "-vcodec", "copy",
                    "-f", "mov", movie_path + fn[:-4] + ".mov"]
                print("mp4 file found: "  + fn)
                p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=False)
                if p.returncode == 0:
                    os.remove(movie_path + fn)
                    print("Converted " + fn)
                else:
                    print("Skipped   " + fn)
                    
# GET VOICEOVER
def get_voiceover(voiceID, stability, similarity_boost):
    
    voiceover_text = 'Komodo dragons are insane... do you think you could take one?'
    voice_to_use = Voice(
        voice_id = voiceID,
        settings = VoiceSettings(
            stability = stability,
            similarity_boost = similarity_boost,
            style = 0,
            use_speaker_boost=True
        )
    )
    
    return voiceover_text, voice_to_use

# CREATE VIDEOS WITH VOICEOVER AND CAPTION
def edit_videos(voiceover_text, voice_to_use):
    for file in os.listdir(path_to_videos):
        # Get the desired video title
        title_with_id = file.split('.')[0]
        video_file = path_to_videos + title_with_id + '.mp4'
        audio_file = path_to_audios + title_with_id + '.mp3'
        
        print(colored('---------------', 'white'))
        print(colored('', 'white'))
        print(colored('EDITING VIDEO: ' + video_file.split('\\')[-1], 'red'))
        print(colored('', 'white'))
        
        tts_audio = generate(api_key=elevenlabs_api_key,
                            text=voiceover_text, 
                            voice=voice_to_use
                            )
        save(tts_audio, audio_file)
        
        # Open the video and audio
        video_clip = VideoFileClip(video_file)
        original_audio_clip = video_clip.audio
        audio_clip = AudioFileClip(audio_file)
        
        final_audio_clip = CompositeAudioClip([audio_clip, original_audio_clip])

        # Concatenate the video clip with the audio clip
        final_clip = video_clip.set_audio(final_audio_clip) 

        # Export the final video with audio
        if os.path.exists(path_to_complete + title_with_id + ".mov"):
            print(colored('.mov ALREADY EXISTS... REMOVING: ' + title_with_id, 'yellow'))
            print(colored('', 'white'))
            os.remove(path_to_complete + title_with_id + ".mov")
            
        final_clip.write_videofile(path_to_complete + title_with_id + ".mp4")	
        
        # Convert to .mov
        mp4_to_mov(path_to_complete)
        
        print(colored('VIDEO SUCCESSFULLY EDITED AND SAVED: ' + video_file.split('\\')[-1], 'green'))
        print(colored('', 'white'))

if __name__ == '__main__':
    # LOAD VARIABLES
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    if not os.path.exists(current_dir + '\\.api'):
        apiKeyTemplate = 'ELEVENLABS_API_KEY = '
        with open(current_dir + '\\.api', 'w') as f:
            f.write(str(apiKeyTemplate))
        print(colored("ERROR: No .api file found. Creating .api file... Please go into the .api file and fill out the information.", 'red'))
        exit()
    
    load_dotenv(current_dir + '\\.api')
    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    load_dotenv(current_dir + '\\inputs.txt')
    user = os.getenv('USER')
    voice_id = os.getenv('VOICE_ID')
    voice_stability = float(os.getenv('VOICE_STABILITY'))
    voice_similarity_boost = float(os.getenv('VOICE_SIMILARITY_BOOST'))

    # DEFINE PATHS
    path_to_videos = current_dir + f'\\videos-{user}\\'
    path_to_audios = current_dir + f'\\audios-{user}\\'
    path_to_complete = current_dir + f'\\complete-{user}\\'

    # CREATE DIRECTORIES
    if not os.path.exists(path_to_audios):
        os.mkdir(path_to_audios)
        
    if not os.path.exists(path_to_complete):
        os.mkdir(path_to_complete)
    
    voiceover_text, voice_to_use = get_voiceover(voice_id, voice_stability, voice_similarity_boost)
    
    edit_videos(voiceover_text, voice_to_use)