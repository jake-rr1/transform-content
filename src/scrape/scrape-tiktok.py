import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.service import Service
import httpx
from dotenv import load_dotenv
import subprocess

def main(mov_path) -> None:
    # get html data and put into data.txt
    htmlResponse = get_html(user, numScrolls=numScrolls) 
    
    # get link ids and statistics from videos
    link_ids, stats = get_vid_properties(htmlResponse)
    
    # get urls from link ids
    urlsToDownload = [f"https://www.tiktok.com/@{user}/video/" + item for item in link_ids]
    
    # download mp4 files
    print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
    for index, url in enumerate(urlsToDownload):
        downloadVideo(url, index, mov_path)
        time.sleep(10)
        
    # convert mp4 to mov
    mp4_to_mov(mov_path)

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
        'cookie': '_ga=GA1.1.1568192361.1702255294; __gads=ID=0a294eb2b7e4166e:T=1702255293:RT=1702255293:S=ALNI_MbvX6xCO4qF9gH_6tNLzt4lj8V7Rw; __gpi=UID=00000d16d0568f6c:T=1702255293:RT=1702255293:S=ALNI_Ma1NpgmPZQNw_-zR7ZYSROoXQZi6w; _ga_ZSF3D6YSLC=GS1.1.1702255293.1.1.1702255374.0.0.0',
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

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")
    downloadLink = downloadSoup.a["href"]
    
    if 'tikcdn.io' not in downloadLink:
        print('SOMETHING WENT WRONG WITH SSSTIK.IO AND DOWNLOAD LINK! SKIPPING FILE!')
        ssstikProblemVideos.append(link)
        return
    
    videoTitle = downloadSoup.p.getText().strip()
    vidName = f"{movie_path}{str(id).zfill(4)}-{videoTitle}.mp4"

    print(f"Saving the video using download link: {videoTitle}")
    mp4File = urlopen(downloadLink)
    # Feel free to change the download directory
    with open(vidName, "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

def get_vid_properties(data) -> list:
    print('STEP 2: Grabbing video properties from hmtl (link/stats)')  
    
    link_ids = [item['id'] for item in data['itemList']]
    stats = [item['stats'] for item in data['itemList']]

    return link_ids, stats

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

def get_html(user, numScrolls) -> dict:
    print(f'STEP 1: Grabbing html to parse videos from tiktok channel: {user}')
    # -----------------CODE-----------------
    options = webdriver.ChromeOptions()
    service = Service(executable_path='C:\\Users\\jacob\\OneDrive\\Desktop\\sidehustles\\transform-content\\src\\upload\\chromedriver.exe')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")
    options.add_argument("user-data-dir=C:\\Users\\jacob\\AppData\\Local\\Google\\Chrome Beta\\User Data\\Profile 2")
    options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"

    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=options)

    accountLink = f'https://www.tiktok.com/@{user}'

    # Go to the Google home page
    driver.get(accountLink)

    time.sleep(10)

    for i in range(numScrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    # Access requests via the `requests` attribute
    dataList = []
    for request in driver.requests:
        if request.response:
            if '/post/item_list/?WebIdLastTim' in request.url:
                requestURL = request.url
                headersTXT = request.headers
                headersFile = current_dir + '\\headers.txt'

                with open(headersFile, 'w') as f:
                    f.write(str(headersTXT))
                    
                headers = {}
                with open(headersFile) as f:
                    for line in f.read().splitlines():
                        if ': ' in line:
                            headers[str(line.split(': ',1)[0])] = str(line.split(': ',1)[1])
                
                client = httpx.Client(http2=True)

                try:
                    # Perform the request
                    response = client.get(requestURL, headers=headers)

                    # Check if the response was received via HTTP/2
                    protocol = response.http_version
                    print(f'Response received via: {protocol}')

                    dataList.append(json.loads(response.text))

                finally:
                    # Close the client
                    client.close()

    os.remove(headersFile)

    itemList = []
    itemListIDs = []

    for i in range(len(dataList)):
        for j in range(len(dataList[i]['itemList'])):
            if dataList[i]['itemList'][j]['id'] not in itemListIDs:
                itemList.append(dataList[i]['itemList'][j])
                itemListIDs.append(dataList[i]['itemList'][j]['id'])

    dataList[0]['itemList'] = itemList

    return dataList[0]

if __name__ == "__main__":
    # add inputs to os environment
    current_dir = os.path.dirname(os.path.realpath(__file__))
    load_dotenv(current_dir + '\\inputs.txt')
    
    # get inputs
    user = os.getenv("USER")
    numScrolls = int(os.getenv("NUMBER_OF_SCROLLS"))
    mov_path = os.getenv("TIKTOK_DOWNLOAD_PATH")
    
    # create unique videos-{user} folder
    mov_path_split = mov_path.split('\\')
    mov_path_split[-2] = f'videos-{user}'
    mov_path = '\\'.join(mov_path_split)
    
    # videos that had problems downloading from ssstik.io
    ssstikProblemVideos = []
    
    # download vidoes as mp4
    main(mov_path)
    
    print('PROBLEMATIC VIDEOS: ')
    print('-------------------------------------------------')  
    print(ssstikProblemVideos)