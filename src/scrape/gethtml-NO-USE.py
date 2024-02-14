from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.service import Service
import time
import httpx
import os
import json

# INPUTS
user = "qinhan111"
numScrolls = 2

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

            with open(current_dir + '\\headers.txt', 'w') as f:
                f.write(str(headersTXT))
                
            headers = {}
            with open(current_dir + '\\headers.txt') as f:
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

itemList = []
itemListIDs = []

print(dataList)

for i in range(len(dataList)):
    for j in range(len(dataList[i]['itemList'])):
        if dataList[i]['itemList'][j]['id'] not in itemListIDs:
            itemList.append(dataList[i]['itemList'][j])
            itemListIDs.append(dataList[i]['itemList'][j]['id'])

dataList[0]['itemList'] = itemList

print(dataList[0]['itemList'][0])
print(len(dataList[0]['itemList']))