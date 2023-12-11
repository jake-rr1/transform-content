import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests

def main(user, link_ids) -> None:
    print("STEP 1: Get urls to download")

    urlsToDownload = ["https://www.tiktok.com/@{user}/video/" + item for item in link_ids]

    print(urlsToDownload)

    print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
    for index, url in enumerate(urlsToDownload):
        print(f"Downloading video: {index}")
        downloadVideo(url, index)
        time.sleep(10)

def downloadVideo(link, id):
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
    with open(f"videos/{id}-{videoTitle}.mp4", "wb") as output:
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

if __name__ == "__main__":
    # URL of the webpage you want to read (this should be an html webpage obtained from right click > inspect element > network > Fetch/XHR > find 'item_list/?WebId' thing)
    # url = 'https://www.tiktok.com/api/post/item_list/?WebIdLastTime=1689543710&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F120.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=35&coverFormat=2&cursor=0&device_id=7256534963528451626&device_platform=web_pc&focus_state=true&from_page=user&history_len=4&is_fullscreen=false&is_page_visible=true&language=en&os=windows&priority_region=US&referer=&region=US&screen_height=1080&screen_width=1920&secUid=MS4wLjABAAAA-Dx2ekKupqNLDLOBDD2v8wLOKhCzMwZwtn8orYP07J38ufn76Uo0rD4NtEQNKNOp&tz_name=America%2FPhoenix&webcast_language=en&msToken=Mz0PSykhT8hWz6CmS_oHgOrXBr2h0dorOYXqBnvywaJ1wCXBU03qh6cGDvSPdGvgTmlxTLVSDEknGubK0aayd79EPxaJgucFm2XBOtG7vbj0raLAmoiAc1YFIngIeHmkaGN0X6AEtasPFw==&X-Bogus=DFSzswVO/RxANy5ntuQ/2t9WcBnh&_signature=_02B4Z6wo00001-yryDgAAIDD7KvIOMGPEUfsq8yAAJ5m24' #'https://www.tiktok.com/api/post/item_list/?WebIdLastTime=1689543710&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F120.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=35&coverFormat=2&cursor=0&device_id=7256534963528451626&device_platform=web_pc&focus_state=true&from_page=user&history_len=3&is_fullscreen=false&is_page_visible=true&language=en&os=windows&priority_region=US&referer=&region=US&screen_height=1080&screen_width=1920&secUid=MS4wLjABAAAA-Dx2ekKupqNLDLOBDD2v8wLOKhCzMwZwtn8orYP07J38ufn76Uo0rD4NtEQNKNOp&tz_name=America%2FPhoenix&webcast_language=en&msToken=XtuC-R_wGAlpVamkzYkPI05D8dS8N8piuFQBwLCGMx8XWxNfrmeCS8dA1wVxYc_tuWuGby-2KbfPfnQZfOO1JS8xUx01ZaXPW4mL8XgNxp4Pb9VDCp6HuWAJKZOjnSScNtgP&X-Bogus=DFSzswVOG/UANy5ntuBJXt9WcBJt&_signature=_02B4Z6wo00001yp6F-wAAIDDKnoX7Bsw3H8qehNAAK.ze3'
    # user = "qinhan111"
    # file_path = 'data.txt'

    # link_ids, stats = get_vid_properties(file_path)

    # main(user, link_ids)

    from haralyzer import HarParser

    # Load the HAR file as a dictionary
    with open('C:\\Users\\jacob\\Desktop\\github\\jake-rr1\\github\\transform-content\\src\\python\\qinhan111.har', 'r') as har_file:
        har_parser = HarParser(json.loads(har_file.read()))

    # # Create a HarParser instance with the dictionary representation
    # har_parser = HarParser(har_data)

    # Extract data from XHR entries
    item_lists = []

    for entry in har_parser.har_data['entries']:
        if 'item_list' in entry['request']['url']:
            # Adjust the condition based on the actual pattern of your XHR entries
            response_text = entry['response']['content']['text']
            item_lists.append(response_text)

    # Now, item_lists contains the data from all XHR entries with URLs containing 'item_list'
    print(item_lists)
