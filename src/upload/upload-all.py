import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from termcolor import colored
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

options = webdriver.ChromeOptions()
service = Service(executable_path='chromedriver.exe')
options.add_argument("--log-level=3")
options.add_argument("user-data-dir=C:\\Users\\jacob\\AppData\\Local\\Google\\Chrome Beta\\User Data\\Profile 2")
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
answer = 2 # 1 if you want to spam same video or 2 if you want to upload multiple videos

current_dir = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(current_dir + '\\.env'):
    accountInfoTemplate = 'INSTAGRAM_USERNAME=\'\'\nTIKTOK_USERNAME=\'\'\nYOUTUBE_USERNAME=\'\'\nINSTAGRAM_PASSWORD=\'\'\nTIKTOK_PASSWORD=\'\'\nYOUTUBE_PASSWORD=\'\''
    with open(current_dir + '\\.env', 'w') as f:
        f.write(str(accountInfoTemplate))
    print(colored("ERROR: No .env file found. Creating .env file. Please go into the .env file and fill out the information.", 'red'))
    exit()

load_dotenv(current_dir + '\\.env')
load_dotenv(current_dir + '\\inputs.txt')
user = os.getenv('USER')

if(int(answer) == 1):
    # TODO UPDATE CODE TO WORK WITH THIS SETTING
    
    nameofvid = input("\033[1;33;40m Put the name of the video you want to upload (Ex: vid.mp4 or myshort.mp4 etc..) ---> ")
    howmany = input("\033[1;33;40m How many times you want to upload this video ---> ")
    
    for i in range(int(howmany)):
        print("UPDATE CODE TO WORK WITH THIS SETTING")

elif(int(answer) == 2):
    dir_path = current_dir + f'\\videos-{user}'
    count = 0

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    print("   ", count, " Videos found in the videos folder, ready to upload...")

    for vid in os.listdir(dir_path):
        bot = webdriver.Chrome(options=options)

        # UPLOAD ON INSTAGRAM REELS
        
        bot.get('https://www.instagram.com/')

        time.sleep(3)

        username_input = bot.find_elements(By.CSS_SELECTOR, "input[name='username']")
        password_input = bot.find_elements(By.CSS_SELECTOR, "input[name='password']")

        if username_input != []:
            username_input[0].send_keys(os.getenv('INSTAGRAM_USERNAME'))
            password_input[0].send_keys(os.getenv('INSTAGRAM_PASSWORD'))
            
            login_button = bot.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

        time.sleep(3)

        upload_button = bot.find_element(By.CSS_SELECTOR, "svg[aria-label='New post']")
        upload_button.click()
        time.sleep(5)
        
        file_input = bot.find_element(By.XPATH, "//*[@class='x6s0dn4 x78zum5 x5yr21d xl56j7k x1n2onr6 xh8yej3']/form/input")
        simp_path = current_dir + f"\\videos\\{vid}"
        abs_path = os.path.abspath(simp_path)
                        
        file_input.send_keys(abs_path)
        
        time.sleep(7)
        
        next_button = bot.find_element(By.XPATH, "//*[(@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37') and (contains(text(), 'Next'))]")
        next_button.click()
        
        time.sleep(3)
        
        next_button = bot.find_element(By.XPATH, "//*[(@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37') and (contains(text(), 'Next'))]")
        next_button.click()
        
        time.sleep(3)
        
        text_box = bot.find_element(By.XPATH, "//*[(@class='xw2csxc x1odjw0f x1n2onr6 x1hnll1o xpqswwc xl565be x5dp1im xdj266r x11i5rnm xat24cr x1mh8g0r x1w2wdq1 xen30ot x1swvt13 x1pi30zi xh8yej3 x5n08af notranslate') and (@aria-label='Write a caption...')]")
        text_box.click()
        
        title = vid.split('-')[1].split('.')[0]
        if title == "":
            title = "#reels #viral #funny #memes #art #photography #travel #fitness #food #pets #quotes #inspiration #motivation #goals #lifestyle #beauty #skincare #makeup #hair #nails #ootd #blogger #influencer #entrepreneur #business #marketing #education #health #wellness #music"
        text_box.send_keys(title)

        time.sleep(3)
        
        share_button = bot.find_element(By.XPATH, "//*[(@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37') and (contains(text(), 'Share'))]")
        share_button.click() 
        
        time.sleep(60)
       
        # UPLOAD ON YOUTUBE
        
        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(3)

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
            time.sleep(3)

        done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
        done_button.click()
        
        time.sleep(60)
        
        # UPLOAD ON TIKTOK
        
        bot.get('https://www.tiktok.com/foryou')

        time.sleep(3)

        login_button = bot.find_elements(By.XPATH, "//*[(contains(text(), 'Use phone / email / username'))]")
        
        if login_button != []:
            login_button.click()
            
            use_email_button = bot.find_element(By.XPATH, "//*[(contains(text(), 'Log in with email or username'))]")
            use_email_button[0].click()

            username_input = bot.find_elements(By.CSS_SELECTOR, "input[name='username']")
            password_input = bot.find_elements(By.CSS_SELECTOR, "input[type='password']")
            
            username_input[0].send_keys(os.getenv('TIKTOK_USERNAME'))
            password_input[0].send_keys(os.getenv('TIKTOK_PASSWORD'))
            
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
        
        print(vid + ' UPLOADED SUCCESSFULLY TO ALL PLATFORMS! REMOVING VIDEO FROM STORAGE...')
        os.remove(abs_path)
        
        time.sleep(3600)




