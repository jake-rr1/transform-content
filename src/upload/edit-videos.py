from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip, concatenate_audioclips
import os
from dotenv import load_dotenv
import subprocess
from elevenlabs import Voice, VoiceSettings, save, generate
import elevenlabs
from termcolor import colored
import json
import whisper_timestamped as whisper
import re
from createElevenLabsAccount import generate_new_elevenlabs_api_key
import time

# self-made imports
import gpt
from imagecaptions import predict_caption

# image saving imports
from datetime import timedelta
import cv2
import numpy as np
import os

# CONVERT .mov TO .mov
def mp4_to_mov(movie_path, fn) -> None:
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

def get_video_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def save_frames(video_file, SAVING_FRAMES_PER_SECOND, title_with_id):
    filename, _ = os.path.splitext(video_file)
    # define save directory
    save_dir = filename.replace(f'videos', f'images')
    # read the video file    
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # get the list of duration spots to save
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    # start the loop
    count = 0
    
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration, 
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            print("SAVING VIDEO FRAME: ", f"frame{frame_duration_formatted}.png (VIDEO: {title_with_id})")
            cv2.imwrite(os.path.join(save_dir, f"frame{frame_duration_formatted}.png"), frame) 
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1
            
def get_voiceover_text(path_to_videos, file) -> str:
    print("GENERATING TEXTS FOR VOICEOVERS")
    title_with_id = file.split('.')[0]
    
    if not os.path.exists(path_to_images + title_with_id):
        os.mkdir(path_to_images + title_with_id) 
    
    video_file = path_to_videos + title_with_id + '.mp4'
    
    video_duration = get_video_duration(video_file)
    
    SAVING_FRAMES_PER_SECOND = num_frames_to_save/video_duration
    
    save_frames(video_file=video_file, SAVING_FRAMES_PER_SECOND=SAVING_FRAMES_PER_SECOND, title_with_id=title_with_id)   
                
    images = []
    for image in os.listdir(path_to_images + title_with_id + '\\'):
        images.append(path_to_images + title_with_id + '\\' + image)
    
    frame_by_frame = predict_caption(images)

    voiceover_text = ''
    while '|' not in voiceover_text: 
        voiceover_text = gpt.gpt_response(frame_by_frame)
        
    return voiceover_text
                    
# GET VOICEOVER
def get_voiceover(voiceID, stability, similarity_boost, file) -> dict:
    print("GENERATING VOICEOVERS")
    voice_to_use = Voice(
        voice_id = voiceID,
        settings = VoiceSettings(
            stability = stability,
            similarity_boost = similarity_boost,
            style = 0,
            use_speaker_boost=True
        )
    )
     
    voiceover_text = get_voiceover_text(path_to_videos=path_to_videos, file=file)
    
    if ' | ' in voiceover_text:
        voiceover_text = voiceover_text.replace(' | ', '|')
    elif ' |' in voiceover_text:
        voiceover_text = voiceover_text.replace(' |', '|')
    elif '| ' in voiceover_text:
        voiceover_text = voiceover_text.replace('| ', '|')
    elif '|' in voiceover_text:
        voiceover_text = voiceover_text
    else:
        print(colored('STRANGE | SCENARIO: '  + voiceover_text, 'red'))
    
    if '\"' in voiceover_text:
        voiceover_text = voiceover_text.replace('\"', '')
    elif "\'" in voiceover_text:
        voiceover_text = voiceover_text.replace("\'", "")
        
    # if words are connected by '...' split words. (e.g. "hello...goobye -> hello... goodbye")
    re.sub(r'\.\.\.(?![\|\s])', '... ', voiceover_text)
    
    if not voiceover_split:
        voiceover_text = voiceover_text.replace('|', ' ')
    
    return voice_to_use, voiceover_text

# GET WORD BY WORD TIMESTAMPS
def get_word_breakdown(mp3File) -> list:
    model = whisper.load_model('medium.en')
    audio = whisper.load_audio(mp3File)
    result = whisper.transcribe(model, audio, language='en')
    output = json.loads(json.dumps(result, indent = 2, ensure_ascii = False))
    all_words = []

    for segment in output["segments"]:
        all_words.extend(segment["words"])
    
    return all_words

# ADD THE CAPTIONS TO THE FINAL CLIP
def add_captions(video, title, audio_clip_end):   
    print("GENERATING VIDEO CAPTIONS")
    if '|' in voiceover_text: 
        start_words = get_word_breakdown((path_to_audios + title + '\\start.mp3'))
        end_words = get_word_breakdown((path_to_audios + title + '\\end.mp3'))
    else:
        start_words = get_word_breakdown((path_to_audios + title + '\\full.mp3'))
    
    start_words = [start_word for start_word in start_words if start_word['text'] != '[*]']
        
    if len(start_words) != len(voiceover_text.split(' ')):
        raise print('ERROR: LENGTH OF LIST "start_words" NOT EQUAL TO LENGTH OF LIST "voiceover_text.split(\' \')"... CONSIDER USING A HIGHER FIDELITY VOICE RECOGNITION MODEL... \n\nstart_words: ', [start_word['text'] for start_word in start_words], '\n\nvoiceover_text.split(' '): ', voiceover_text.split(' '))
        
    video_width, video_height = video.size
    video_duration = video.duration
        
    all_clips = []
    
    all_clips.append(video)

    print('ADDING START_WORDS TO CAPTIONS: ', [start_word['text'] for start_word in start_words])

    if '|' in voiceover_text:
        # end_words_final = end_words[-1]['end']
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

# CREATE VIDEOS WITH VOICEOVER AND CAPTION
def edit_videos(voiceover_text, voice_to_use, file):
    # Get the desired video title
    title_with_id = file.split('.')[0]
    video_file = path_to_videos + title_with_id + '.mp4'
    audio_file_folder = path_to_audios + title_with_id
    if not os.path.exists(audio_file_folder):
        os.mkdir(audio_file_folder)
    audio_file_full = path_to_audios + title_with_id + '\\full.mp3'
    audio_file_start = path_to_audios + title_with_id + '\\start.mp3'
    audio_file_end = path_to_audios + title_with_id + '\\end.mp3'
    
    print(colored('---------------', 'white'))
    print(colored('', 'white'))
    print(colored('EDITING VIDEO: ' + video_file.split('\\')[-1], 'red'))
    print(colored('', 'white'))
    
    iter = 0
    if '|' in voiceover_text:
        while True:
            try:
                print('GENERATING AI VOICE FROM TEXT')
                if iter > 0:
                    old_elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
                    while old_elevenlabs_api_key == elevenlabs_api_key:
                        load_dotenv(current_dir + '\\.api')
                        elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
                else:
                    load_dotenv(current_dir + '\\.api')
                    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
                tts_audio_start = generate(api_key=elevenlabs_api_key,
                                    text=voiceover_text.split('|')[0], 
                                    voice=voice_to_use,
                                    )
                
                tts_audio_end = generate(api_key=elevenlabs_api_key,
                                    text=voiceover_text.split('|')[1], 
                                    voice=voice_to_use,
                                    )
                break
            except Exception as err:
                iter += 1
                if 'This request exceeds your quota.' in str(err):
                    print('API KEY EXPIRED')
                    generate_new_elevenlabs_api_key()
                else:
                    print(err)
                
        save(tts_audio_start, audio_file_start)
        save(tts_audio_end, audio_file_end)
        
        tts_audio_clip_start = AudioFileClip(audio_file_start)
        tts_audio_clip_end = AudioFileClip(audio_file_end)
        
        tts_audio_full = concatenate_audioclips([tts_audio_clip_start, tts_audio_clip_end])
        tts_audio_full.write_audiofile(audio_file_full)

        # words_end = get_word_breakdown(path_to_audios + title_with_id + '-end.mp3')
                
        # Open the video and audio
        video_clip = VideoFileClip(video_file)
        video_duration = video_clip.duration
        # end_words_final = words_end[-1]['end']
        audio_clip_end = AudioFileClip(audio_file_end)
        audio_start_time = video_duration - audio_clip_end.duration - 2
        
        original_audio_clip = video_clip.audio
        audio_clip_start = AudioFileClip(audio_file_start)
        audio_clip_end = AudioFileClip(audio_file_end)
        audio_clip_end = audio_clip_end.set_start(audio_start_time)
        audio_clip = audio_clip_end
        final_audio_clip = CompositeAudioClip([audio_clip_start, audio_clip_end, original_audio_clip])
    else:
        while True:
            try:
                print('GENERATING AI VOICE FROM TEXT')
                if iter > 0:
                    old_elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
                    while old_elevenlabs_api_key == elevenlabs_api_key:
                        load_dotenv(current_dir + '\\.api')
                        elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
                else:
                    load_dotenv(current_dir + '\\.api')
                    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
                tts_audio = generate(api_key=elevenlabs_api_key,
                                    text=voiceover_text.split('|')[0], 
                                    voice=voice_to_use,
                                    )  
                break
            except Exception as err:
                iter += 1
                if 'This request exceeds your quota.' in str(err):
                    print('API KEY EXPIRED')
                    generate_new_elevenlabs_api_key()
                else:
                    print(err)
                    
        save(tts_audio, audio_file_full)
                    
        # Open the video and audio
        video_clip = VideoFileClip(video_file)
        original_audio_clip = video_clip.audio
        audio_clip = AudioFileClip(audio_file_full)
        final_audio_clip = CompositeAudioClip([audio_clip, original_audio_clip]) 
    # Concatenate the video clip with the audio clip
    print('SETTING AUDIO FOR FINAL VIDEO')
    final_clip = video_clip.set_audio(final_audio_clip) 

    # Export the final video with audio
    print('EXPORTING FINAL VIDEO')
    if os.path.exists(path_to_complete + title_with_id + ".mov"):
        print(colored('.mov ALREADY EXISTS... REMOVING: ' + title_with_id, 'yellow'))
        print(colored('', 'white'))
        os.remove(path_to_complete + title_with_id + ".mov")
                
    # Add captions
    add_captions(final_clip, title_with_id, audio_clip)
    
    # Convert to .mov
    mp4_to_mov(path_to_complete, file)
    
    print(colored('VIDEO SUCCESSFULLY EDITED AND SAVED: ' + video_file.split('\\')[-1], 'green'))
    print(colored('', 'white'))
    
    raise 'test'

def construct_dict_of_voices():
    voices = elevenlabs.voices()
    voices_dict = {}
    
    for voice in voices:
        voices_dict[voice.name] = voice.voice_id

    return voices_dict

if __name__ == '__main__':
    # CONSTRUCT DICTIONARY MAPPING NAMES TO VOICES
    voices_dict = construct_dict_of_voices()
    
    # LOAD VARIABLES
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    if not os.path.exists(current_dir + '\\.api'):
        apiKeyTemplate = ['ELEVENLABS_API_KEY = ', 'OPENAI_API_KEY = ', 'CLOUDMERSIVE_API_KEY = ']
        with open(current_dir + '\\.api', 'w') as f:
            f.write(str(apiKeyTemplate[0]) + '\n')
            f.write(str(apiKeyTemplate[1]) + '\n')
            f.write(str(apiKeyTemplate[2]))
            
        print(colored("ERROR: No .api file found. Creating .api file... Please go into the .api file and fill out the information.", 'red'))
        exit()
    
    load_dotenv(current_dir + '\\inputs.txt')
    load_dotenv(current_dir + '\\.api')
    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    user = os.getenv('USER')
    voice_name = os.getenv('VOICE_NAME')
    voice_id = voices_dict[voice_name]
    voice_stability = float(os.getenv('VOICE_STABILITY'))
    voice_similarity_boost = float(os.getenv('VOICE_SIMILARITY_BOOST'))
    subtitle_font = os.getenv('SUBTITLE_FONT')
    subtitle_outline = float(os.getenv('SUBTITLE_OUTLINE'))
    subtitle_fontsize = float(os.getenv('SUBTITLE_FONTSIZE'))
    subtitle_y_position = float(os.getenv('SUBTITLE_Y_POSITION'))
    voiceover_split = bool(int(os.getenv('VOICEOVER_SPLIT')))
    num_frames_to_save = float(os.getenv('SAVE_FRAMES'))
    verification_email = os.getenv('VERIFICATION_EMAIL')
    
    # DEFINE PATHS
    path_to_videos = current_dir + f'\\{user}\\videos\\'
    path_to_audios = current_dir + f'\\{user}\\audios\\'
    path_to_complete = current_dir + f'\\{user}\\complete\\'
    path_to_images = current_dir + f'\\{user}\\images\\'

    # CREATE DIRECTORIES
    if not os.path.exists(path_to_audios):
        os.mkdir(path_to_audios)
        
    if not os.path.exists(path_to_complete):
        os.mkdir(path_to_complete)
        
    if not os.path.exists(path_to_images):
        os.mkdir(path_to_images)
    
    for file in os.listdir(path_to_videos):
        if not os.path.exists(path_to_complete + file.replace('.mp4','.mov')):
            voice_to_use, voiceover_text = get_voiceover(voice_id, voice_stability, voice_similarity_boost, file=file)
                        
            voiceover_text = 'These animals have mastered the art of relaxation... but can you guess where they call home? Are you more of a beach bum or a forest dweller?'
                        
            print('GENERATED VOICEOVER TEXT: ' + voiceover_text)
                                        
            edit_videos(voiceover_text, voice_to_use, file)
        else:
            print(colored(f'{file} ALREADY EDITED... SKIPPING!', 'green'))