import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os

def main(user, link_ids, mov_path) -> None:
    print("STEP 1: Get urls to download")

    urlsToDownload = [f"https://www.tiktok.com/@{user}/video/" + item for item in link_ids]

    print(urlsToDownload)

    print(f"STEP 3: T   ime to download {len(urlsToDownload)} videos")
    for index, url in enumerate(urlsToDownload):
        print(f"Downloading video: {index}")
        downloadVideo(url, index, mov_path)
        time.sleep(10)

def downloadVideo(link, id, movie_path):
    print(f"Downloading video {id} from: {link}")
    
    cookies = {
        '_ga': 'GA1.1.1568192361.1702255294',
        '__gads': 'ID=0a294eb2b7e4166e:T=1702255293:RT=1702255293:S=ALNI_MbvX6xCO4qF9gH_6tNLzt4lj8V7Rw',
        '__gpi': 'UID=00000d16d0568f6c:T=1702255293:RT=1702255293:S=ALNI_Ma1NpgmPZQNw_-zR7ZYSROoXQZi6w',
        '_ga_ZSF3D6YSLC': 'GS1.1.1702255293.1.1.1702255374.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.1.1568192361.1702255294; __gads=ID=0a294eb2b7e4166e:T=1702255293:RT=1702255293:S=ALNI_MbvX6xCO4qF9gH_6tNLzt4lj8V7Rw; __gpi=UID=00000d16d0568f6c:T=1702255293:RT=1702255293:S=ALNI_Ma1NpgmPZQNw_-zR7ZYSROoXQZi6w; _ga_ZSF3D6YSLC=GS1.1.1702255293.1.1.1702255374.0.0.0',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'RjU5bWlk',
    }

    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    # Feel free to change the download directory
    with open(f"{movie_path}{id}-{videoTitle}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

def get_vid_properties(file_path) -> list:
    # Open the file and load its content as a JSON string
    with open(file_path, 'r') as file:
        json_str = file.read()

    # Parse the JSON string to create a Python dictionary
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    
    link_ids = [item['id'] for item in data['itemList']]
    stats = [item['stats'] for item in data['itemList']]

    return link_ids, stats

def mp4_to_mov(movie_path) -> None:
    import os
    import subprocess

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

if __name__ == "__main__":
    user = "qinhan111"
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = current_dir + '\\data.txt'
    mov_path = current_dir + '\\videos\\'

    link_ids, stats = get_vid_properties(file_path)

    main(user, link_ids, mov_path)
    
    mp4_to_mov(mov_path)
        
