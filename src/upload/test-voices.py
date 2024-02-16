from elevenlabs import Voice, VoiceSettings, generate, play, voices
from dotenv import load_dotenv
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
load_dotenv(current_dir + '\\.api')
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')

voiceName = 'Rachel'
voiceover_text = 'Komodo dragons are insane... do you think you could take one?'

allVoicesRaw = voices()
allVoices = {voice.name: voice for voice in allVoicesRaw}

voice_to_use = Voice(
    voice_id = '21m00Tcm4TlvDq8ikWAM',
    settings = VoiceSettings(
        stability = .25,
        similarity_boost = 1,
    )
)

tts_audio = generate(api_key=elevenlabs_api_key,
                     text=voiceover_text, 
                     voice=voice_to_use
                     )

for i in range(len(allVoicesRaw)):
    if allVoicesRaw[i].labels['gender'] == 'female' and allVoicesRaw[i].labels['accent'] == 'american':
        print(allVoicesRaw[i].name + ' : ' + allVoicesRaw[i].voice_id + ' : ' + str(allVoicesRaw[i].labels))

play(tts_audio)