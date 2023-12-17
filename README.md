# transform-content
Automate Transormative Content

Automation Steps:

- 1 download videos + convert .mp4 to .mov + adobe premier edits (one click) 
  - 1.1 download videos + convert .mp4 to .mov :white_check_mark:
  - 1.2 adobe premier edits
    - 1.2.1 use llama to analyze video and describe it
      - 1.2.1.1 run llama demo
        - 1.2.1.1.1 follow instructions at https://github.com/DAMO-NLP-SG/Video-LLaMA
        - 1.2.1.1.2 install requirements.txt using ```pip install -r requirements.txt```
        - 1.2.1.1.2 if error pops up talking about cuda do the below
          - ```conda install pytorch torchvision cudatoolkit=10.2 -c pytorch```
          - ```$ sudo add-apt-repository ppa:graphics-drivers/ppa
               $ sudo apt install nvidia-driver-450```
    - 1.2.2 use gpt to convert llama analysis into 'intro' for short form content vid
    - 1.2.3 use text-to-speech (TTS) to convert 'intro' into .mp4 file
    - 1.2.4 combine video with .mp4 file
    - 1.2.5 export to .MP4 video
- upload videos (one click)
- profit $$$$$
