from elevenlabs import Voice, VoiceSettings, generate, play, voices, save
from dotenv import load_dotenv
import os
import whisper_timestamped as whisper
import datetime
import json
from moviepy.editor import TextClip, concatenate_videoclips, CompositeVideoClip, ColorClip
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

current_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_dir)
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

voiceName = 'Rachel'
num_words = len(voiceover_text.split(' '))

# allVoicesRaw = voices()
# allVoices = {voice.name: voice for voice in allVoicesRaw}

# voice_to_use = Voice(
#     voice_id = '21m00Tcm4TlvDq8ikWAM',
#     settings = VoiceSettings(
#         stability = .25,
#         similarity_boost = 1,
#     )
# )

# tts_audio = generate(api_key=elevenlabs_api_key,
#                      text=voiceover_text, 
#                      voice=voice_to_use
#                      )

# for i in range(len(allVoicesRaw)):
#     if allVoicesRaw[i].labels['gender'] == 'female' and allVoicesRaw[i].labels['accent'] == 'american':
#         print(allVoicesRaw[i].name + ' : ' + allVoicesRaw[i].voice_id + ' : ' + str(allVoicesRaw[i].labels))

model = whisper.load_model('base')
audio = whisper.load_audio("audios-qinhan111\\0000-#wildlife #animals #wildboar #komodo #fyp.mp3")
result = whisper.transcribe(model, audio, language='en')
output = json.loads(json.dumps(result, indent = 2, ensure_ascii = False))
words = output['segments'][0]['words']

video_duration = 10
width = 1920
height = 1080

# Create a black background clip with the specified dimensions and duration
video = ColorClip(size=(width, height), color=(0,255,0), ismask=False).set_duration(video_duration)

all_clips = []

all_clips.append(video)

wIdx = 0

total_duration = []

for pIdx, phrase in enumerate(voiceover_text.split('|')):
    tot_duration = 0
    for idx, word in enumerate(phrase.split(' ')):
        tot_duration += words[wIdx]['end'] - words[wIdx]['start']
        
    total_duration.append(tot_duration)
    wIdx += 1
    
wIdx = 0

for pIdx, phrase in enumerate(voiceover_text.split('|')):
    for idx, word in enumerate(phrase.split(' ')):
        print('ADDING ' + phrase.split(' ')[idx] + ' TO SUBTITLES')
        duration = words[wIdx]['end'] - words[wIdx]['start']
        if pIdx == 0:
            current_text_clip = TextClip(word, stroke_width=subtitle_outline, stroke_color='black', fontsize = subtitle_fontsize*10, color = 'white', bg_color='transparent', font=subtitle_font, method='caption').set_duration(duration).set_start(words[wIdx]['start']).set_end(words[wIdx]['end'])
        else:
            current_text_clip = TextClip(word, stroke_width=subtitle_outline, stroke_color='black', fontsize = subtitle_fontsize*10, color = 'white', bg_color='transparent', font=subtitle_font, method='caption').set_duration(duration).set_start(video_duration - total_duration[pIdx] + words[wIdx]['start'] - 2).set_end(video_duration - total_duration[pIdx] + words[wIdx]['end'] - 2)
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
        txt_moving_resized = current_text_clip.resize(lambda t: resize(t)).set_position(('center',subtitle_y_position*height))
        # txt_moving_resized = txt_moving_resized.resize(lambda t: resize2(t)).set_position(('center','center'))
        all_clips.append(txt_moving_resized)
        
        wIdx += 1



video = CompositeVideoClip(all_clips)
    

# 5. Combine the Clips
# Overlay the resized text on the background to create a composite video
# txt_video = concatenate_videoclips(all_texts)


# 6. Export the Final Video
# Save the composite video to a file with a frame rate of 60 fps
video.write_videofile("scaling_text_1080p.mp4", fps=60)
    
# save_target = 'test.srt'
# with open(save_target, 'w') as f:
#     for idx, word in enumerate(words):
#         f.write(str(idx + 1) + '\n')
#         f.write('00:00:0' + str("{:.3f}".format(float(word['start']))).replace('.',',') + ' --> 00:00:0' + str("{:.3f}".format(float(word['end']))).replace('.',',') + '\n')
#         f.write(word['text'] + '\n')
#         f.write('\n')
        
        
