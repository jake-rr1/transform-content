import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from termcolor import colored
from dotenv import load_dotenv

options = webdriver.ChromeOptions()
service = Service(executable_path='chromedriver.exe')
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
options.add_argument("user-data-dir=C:\\Users\\jacob\\AppData\\Local\\Google\\Chrome Beta\\User Data\\Profile 2")
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
print("\033[1;31;40m IMPORTANT: Put one or more videos in the *videos* folder in this directory")
answer = 2 #input("\033[1;32;40m Press 1 if you want to spam same video or Press 2 if you want to upload multiple videos: ")

txt = colored('-----', 'white')
print(txt)

current_dir = os.path.dirname(os.path.realpath(__file__))

load_dotenv(current_dir + '\\.env')

if(int(answer) == 1):
    nameofvid = input("\033[1;33;40m Put the name of the video you want to upload (Ex: vid.mp4 or myshort.mp4 etc..) ---> ")
    howmany = input("\033[1;33;40m How many times you want to upload this video ---> ")
    
    print(txt)

    for i in range(int(howmany)):
        print("UPDATE CODE TO WORK WITH THIS SETTING")


elif(int(answer) == 2):
    dir_path = current_dir + '\\videos'
    count = 0

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    print("   ", count, " Videos found in the videos folder, ready to upload...")

    for vid in os.listdir(dir_path):
        bot = webdriver.Chrome(options=options)

        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(1)

        file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
        simp_path = current_dir + f"\\videos\\{vid}"
        abs_path = os.path.abspath(simp_path)
        
        file_input.send_keys(abs_path)
        
        time.sleep(7)
        
        text_box = bot.find_element(By.XPATH, '//*[@id="textbox"]')
        text_box.click()
        text_box.send_keys(Keys.CONTROL + "a")
        text_box.send_keys(Keys.BACK_SPACE)       
        title = vid.split('-')[1].split('.')[0]
        if title == "":
            title = "#shortschallenge #shortsart #shortsbeauty #shortsfashion #shortsfitness #shortstravel #shortsanimal #shortseducation #shortsentertainment #shortslife #shortslove #shortsstory #shortsdiy #shortshacks"
        text_box.send_keys(title)

        next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
        for i in range(3):
            next_button.click()
            time.sleep(1)

        done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
        done_button.click()
        time.sleep(5)
        bot.quit()
        time.sleep(3600)
        




