import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from termcolor import colored
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

def wait_to_click(selector_arg, attempts=10):
    count = 0
    while count < attempts:
        try:
            upload_button = bot.find_element(By.XPATH, selector_arg)
            time.sleep(1)
            upload_button.click()
            count += 1
        except Exception as e:
            if ('is not clickable at point' in str(e) or "stale element not found" in str(e)):
                print('Retrying clicking on button.')
                count += 1
            else:
                raise e

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

        bot.get('https://www.tiktok.com/foryou')

        time.sleep(3)

        login_button = bot.find_elements(By.XPATH, "//*[(contains(text(), 'Use phone / email / username'))]")
        
        if login_button != []:
            login_button.click()
            
            use_email_button = bot.find_element(By.XPATH, "//*[(contains(text(), 'Log in with email or username'))]")
            use_email_button[0].click()

            username_input = bot.find_elements(By.CSS_SELECTOR, "input[name='username']")
            password_input = bot.find_elements(By.CSS_SELECTOR, "input[type='password']")
            
            username_input[0].send_keys(os.getenv('IG_TT_YT_USERNAME'))
            password_input[0].send_keys(os.getenv('IG_TT_YT_PASSWORD'))
            
            time.sleep(2)
            
            login_button = bot.find_element(By.XPATH, "//button[(@type='submit') and (@data-e2e='login-button')]")
            login_button.click()

        selector_arg =  "//*[@class='css-1qup28j-DivUpload e18d3d944']"
        # wait_to_click(selector_arg, 30)
        
        upload_button = EC.presence_of_element_located((By.XPATH, selector_arg))
        WebDriverWait(bot, 20).until(upload_button).click()
        
        time.sleep(3)
                
        frame = bot.find_element(By.XPATH, '//*[@data-tt="Upload_index_iframe"]')
        bot.switch_to.frame(frame)
                
        file_input = bot.find_element(By.XPATH, "//*[(@role='button') and (@class='jsx-3397029100')]/input")
        simp_path = current_dir + f"\\videos\\{vid}"
        abs_path = os.path.abspath(simp_path)
                
        file_input.send_keys(abs_path)
        
        time.sleep(10)
        
        text_box = bot.find_element(By.XPATH, "//*[(@class='notranslate public-DraftEditor-content') and (@role='combobox')]")
        text_box.click()
        
        text_box.send_keys(Keys.CONTROL + "a")
        text_box.send_keys(Keys.BACK_SPACE)  
        
        title = vid.split('-')[1].split('.')[0]
        if title == "":
            title = "#fyp #foryou #foryoupage #viral #tiktok"
            
        for elem in title.split(' '):   
            text_box.send_keys(elem)
            time.sleep(2)
            text_box.send_keys(Keys.ENTER)
        
        time.sleep(5)
        
        post_button = bot.find_element(By.XPATH, "//*[(@class='css-1z070dx') and (contains(text(), 'Post'))]")
        post_button.click()
        
        time.sleep(60)
        bot.quit()
        time.sleep(3600)
        




