from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip, concatenate_audioclips
import os
from dotenv import load_dotenv
import subprocess
from elevenlabs import Voice, VoiceSettings, save, generate
from termcolor import colored
import json
import whisper_timestamped as whisper

# CONVERT .mov TO .mov
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
    voice_to_use = Voice(
        voice_id = voiceID,
        settings = VoiceSettings(
            stability = stability,
            similarity_boost = similarity_boost,
            style = 0,
            use_speaker_boost=True
        )
    )
    
    return voice_to_use

# GET WORD BY WORD TIMESTAMPS
def get_word_breakdown(mp3File):
    model = whisper.load_model('base')
    audio = whisper.load_audio(mp3File)
    result = whisper.transcribe(model, audio, language='en')
    output = json.loads(json.dumps(result, indent = 2, ensure_ascii = False))
    all_words = []

    for segment in output["segments"]:
        all_words.extend(segment["words"])
    
    return all_words

# ADD THE CAPTIONS TO THE FINAL CLIP
def add_captions(video, title, audio_clip_end):   
    if '|' in voiceover_text: 
        print('GETTING START WORDS')
        start_words = get_word_breakdown((path_to_audios + title + '-start.mp3'))
        print('GETTING END WORDS')
        end_words = get_word_breakdown((path_to_audios + title + '-end.mp3'))
    else:
        start_words = get_word_breakdown((path_to_audios + title + '.mp3'))
        
    video_width, video_height = video.size
    video_duration = video.duration
        
    all_clips = []
    
    all_clips.append(video)

    if '|' in voiceover_text:
        end_words_final = end_words[-1]['end']
        for pIdx, phrase in enumerate(voiceover_text.split('|')):
            for idx, word in enumerate(phrase.split(' ')):
                print('ADDING ' + phrase.split(' ')[idx] + ' TO SUBTITLES')
                if pIdx == 0:
                    duration = start_words[idx]['end'] - start_words[idx]['start']
                    current_text_clip = TextClip(word, stroke_width=subtitle_outline, stroke_color='black', fontsize = subtitle_fontsize*10, color = 'white', bg_color='transparent', font=subtitle_font, method='caption').set_start(start_words[idx]['start']).set_end(start_words[idx]['end'])
                else:
                    duration = end_words[idx]['end'] - end_words[idx]['start']
                    start_time = video_duration - audio_clip_end.duration + end_words[idx]['start'] - 2
                    end_time = video_duration - audio_clip_end.duration + end_words[idx]['end'] - 2
                    current_text_clip = TextClip(word, stroke_width=subtitle_outline, stroke_color='black', fontsize = subtitle_fontsize*10, color = 'white', bg_color='transparent', font=subtitle_font, method='caption').set_start(start_time).set_end(end_time)
                    
                    if idx == len(phrase.split(' '))-1:
                        print('OUTRO TEXT ENDING POINT: ' + str(video_duration - audio_clip_end.duration + end_words[idx]['start'] - 2))
                
                # 3. Define the Resize (Scaling) Function
                def resize(t):
                    # Starting scale factor
                    start_scale = 1/10
                    # End scale factor (the size to which the text should grow)
                    end_scale = 1.5/10
                    # Calculate the scaling factor based on elapsed time and total duration
                    scale_factor = start_scale + t/duration * (end_scale - start_scale)
                    return scale_factor
                
                # 4. Apply the Resize Effect to the Text
                # Resize the text over time using the scaling function
                txt_moving_resized = current_text_clip.resize(lambda t: resize(t)).set_position(('center',subtitle_y_position*video_height))
                # txt_moving_resized = txt_moving_resized.resize(lambda t: resize2(t)).set_position(('center','center'))
                all_clips.append(txt_moving_resized)
    else:
        for idx, word in enumerate(start_words):
            print('ADDING ' + voiceover_text.split(' ')[idx] + ' TO SUBTITLES')
            
            duration = start_words[idx]['end'] - start_words[idx]['start']
            current_text_clip = TextClip(voiceover_text.split(' ')[idx], stroke_width=subtitle_outline, stroke_color='black', fontsize = subtitle_fontsize*10, color = 'white', bg_color='transparent', font=subtitle_font, method='caption').set_start(start_words[idx]['start']).set_end(start_words[idx]['end'])

            # 3. Define the Resize (Scaling) Function
            def resize(t):
                # Starting scale factor
                start_scale = 1/10
                # End scale factor (the size to which the text should grow)
                end_scale = 1.5/10
                # Calculate the scaling factor based on elapsed time and total duration
                scale_factor = start_scale + t/duration * (end_scale - start_scale)
                return scale_factor
            
            # 4. Apply the Resize Effect to the Text
            # Resize the text over time using the scaling function
            txt_moving_resized = current_text_clip.resize(lambda t: resize(t)).set_position(('center',subtitle_y_position*video_height))
            # txt_moving_resized = txt_moving_resized.resize(lambda t: resize2(t)).set_position(('center','center'))
            all_clips.append(txt_moving_resized)
                    
    video = CompositeVideoClip(all_clips)
    
    print('WRITING VIDEO FILE WITH CAPTIONS')
    video.write_videofile(path_to_complete + title + '.mp4', fps=60)
    print('DONE WRITING')
    
    raise 'test'

# CREATE VIDEOS WITH VOICEOVER AND CAPTION
def edit_videos(voiceover_text, voice_to_use):
    for file in os.listdir(path_to_videos):
        # Get the desired video title
        title_with_id = file.split('.')[0]
        video_file = path_to_videos + title_with_id + '.mp4'
        audio_file_full = path_to_audios + title_with_id + '.mp3'
        audio_file_start = path_to_audios + title_with_id + '-start.mp3'
        audio_file_end = path_to_audios + title_with_id + '-end.mp3'
        
        print(colored('---------------', 'white'))
        print(colored('', 'white'))
        print(colored('EDITING VIDEO: ' + video_file.split('\\')[-1], 'red'))
        print(colored('', 'white'))
        
        if '|' in voiceover_text:
            tts_audio_start = generate(api_key=elevenlabs_api_key,
                                text=voiceover_text.split('|')[0], 
                                voice=voice_to_use,
                                )
            
            tts_audio_end = generate(api_key=elevenlabs_api_key,
                                text=voiceover_text.split('|')[1], 
                                voice=voice_to_use,
                                )
            
            save(tts_audio_start, audio_file_start)
            save(tts_audio_end, audio_file_end)
            
            tts_audio_clip_start = AudioFileClip(audio_file_start)
            tts_audio_clip_end = AudioFileClip(audio_file_end)
            
            tts_audio_full = concatenate_audioclips([tts_audio_clip_start, tts_audio_clip_end])
            tts_audio_full.write_audiofile(audio_file_full)

            words_end = get_word_breakdown(path_to_audios + title_with_id + '-end.mp3')
                    
            # Open the video and audio
            video_clip = VideoFileClip(video_file)
            video_duration = video_clip.duration
            end_words_final = words_end[-1]['end']
            audio_clip_end = AudioFileClip(audio_file_end)
            audio_start_time = video_duration - audio_clip_end.duration - 2
            
            original_audio_clip = video_clip.audio
            audio_clip_start = AudioFileClip(audio_file_start)
            audio_clip_end = AudioFileClip(audio_file_end)
            audio_clip_end = audio_clip_end.set_start(audio_start_time)
            print('OUTRO AUDIO ENDING POINT: ' + str(audio_start_time))
            audio_clip = audio_clip_end
            final_audio_clip = CompositeAudioClip([audio_clip_start, audio_clip_end, original_audio_clip])
        else:
            tts_audio = generate(api_key=elevenlabs_api_key,
                                text=voiceover_text.split('|')[0], 
                                voice=voice_to_use,
                                )
            
            save(tts_audio, audio_file_full)
                    
            # Open the video and audio
            video_clip = VideoFileClip(video_file)
            original_audio_clip = video_clip.audio
            audio_clip = AudioFileClip(audio_file_full)
            final_audio_clip = CompositeAudioClip([audio_clip, original_audio_clip])   

        # Concatenate the video clip with the audio clip
        final_clip = video_clip.set_audio(final_audio_clip) 

        # Export the final video with audio
        if os.path.exists(path_to_complete + title_with_id + ".mov"):
            print(colored('.mov ALREADY EXISTS... REMOVING: ' + title_with_id, 'yellow'))
            print(colored('', 'white'))
            os.remove(path_to_complete + title_with_id + ".mov")
                    
        # Add captions
        add_captions(final_clip, title_with_id, audio_clip)
        
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
    subtitle_font = os.getenv('SUBTITLE_FONT')
    subtitle_outline = float(os.getenv('SUBTITLE_OUTLINE'))
    voiceover_text = os.getenv('VOICEOVER_TEXT').upper()
    subtitle_fontsize = float(os.getenv('SUBTITLE_FONTSIZE'))
    subtitle_y_position = float(os.getenv('SUBTITLE_Y_POSITION'))
    
    # DEFINE PATHS
    path_to_videos = current_dir + f'\\videos-{user}\\'
    path_to_audios = current_dir + f'\\audios-{user}\\'
    path_to_subtitles = current_dir + f'\\subtitles-{user}\\'
    path_to_complete = current_dir + f'\\complete-{user}\\'

    # CREATE DIRECTORIES
    if not os.path.exists(path_to_audios):
        os.mkdir(path_to_audios)
        
    if not os.path.exists(path_to_complete):
        os.mkdir(path_to_complete)
    
    if not os.path.exists(path_to_subtitles):
        os.mkdir(path_to_subtitles)
    
    voice_to_use = get_voiceover(voice_id, voice_stability, voice_similarity_boost)
    
    edit_videos(voiceover_text, voice_to_use)