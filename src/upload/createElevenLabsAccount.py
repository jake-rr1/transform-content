import time
import os
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from password_generator import PasswordGenerator
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
import names
from selenium.webdriver import Keys

def generate_new_elevenlabs_api_key() -> None:
       print('GENERATING NEW ELEVENLABS API KEY')
       # -----------------CODE-----------------
       options = webdriver.ChromeOptions()
       service = Service(executable_path='C:\\Users\\jacob\\OneDrive\\Desktop\\sidehustles\\transform-content\\src\\upload\\chromedriver.exe')
       options.add_argument("--log-level=3")
       options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"

       current_dir = os.path.dirname(os.path.realpath(__file__))

       # inputs
       load_dotenv(current_dir + '\\inputs.txt')

       # Create a new instance of the Chrome driver
       driver = webdriver.Chrome(options=options)
       driver.maximize_window()
       wait = WebDriverWait(driver, 1e200)
       actions = ActionChains(driver)

       stealth(driver,
              user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.105 Safari/537.36',
              languages=["en-US", "en"],
              vendor="Google Inc.",
              platform="Win32",
              webgl_vendor="Intel Inc.",
              renderer="Intel Iris OpenGL Engine",
              fix_hairline=True,
              )

       emailSite = 'https://internxt.com/temporary-email'

       elevenlabsSite = 'https://elevenlabs.io/sign-up'

       driver.get(emailSite)

       generate_email_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="flex w-full flex-row items-center justify-center space-x-2 whitespace-nowrap rounded-lg border border-gray-10 bg-white px-5 py-2 shadow-sm hover:bg-gray-10"]')))
       generate_email_button.click()

       time.sleep(1)

       username = 'Generating random email...'
       while username == 'Generating random email...':
              username = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="flex h-full w-full cursor-pointer flex-row items-center justify-between rounded-xl bg-gray-1 shadow-sm  px-4 py-3"]'))).text

       pwo = PasswordGenerator() #password object
       password = pwo.generate()

       driver.execute_script(f"window.open('{elevenlabsSite}', 'secondtab')")
       driver.switch_to.window(driver.window_handles[1])

       try:
              elevenlabs_username = username
              username_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[(@data-testid='signup-email-input')]")))
              username_field.click()
              username_field.send_keys(elevenlabs_username)

              time.sleep(0.5)

              password_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[(@data-testid='signup-password-input')]")))
              password_field.click()
              password_field.send_keys(password)
       except:
              captcha_iframe = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Main content of the hCaptcha challenge"]')))
              driver.switch_to.frame(captcha_iframe)
              captcha_window = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@style="position: absolute; top: 0px; cursor: default; z-index: 10; width: 500px; height: 480px;"] | //*[@style="width: 100%; height: 100%; position: fixed; pointer-events: auto; top: 0px; left: 0px; z-index: 0; background-color: rgb(255, 255, 255); opacity: 0.05; cursor: pointer;"]')))

              x_offset = -900
              y_offset = 300
              actions.move_to_element(captcha_window).move_by_offset(x_offset, y_offset).click().perform()

              driver.switch_to.default_content()
              
              elevenlabs_username = username
              username_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[(@data-testid='signup-email-input')]")))
              username_field.click()
              username_field.send_keys(Keys.CONTROL + "a")
              username_field.send_keys(Keys.BACK_SPACE)      
              username_field.send_keys(elevenlabs_username)

              time.sleep(0.5)

              password_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[(@data-testid='signup-password-input')]")))
              password_field.click()
              password_field.send_keys(Keys.CONTROL + "a")
              password_field.send_keys(Keys.BACK_SPACE)
              password_field.send_keys(password)

       wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="block font-serif text-sm font-normal text-white"]')))

       driver.switch_to.window(driver.window_handles[0])

       time.sleep(1)

       refresh_messages = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="cursor-pointer text-gray-50 hover:text-gray-80 "]')))
       refresh_messages.click()

       time.sleep(.5)

       email_messages = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="w-full text-xs line-clamp-2"]')))
       email_messages[-1].click()

       time.sleep(.5)

       email_verify_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Verify Email'))).get_attribute('href')

       driver.execute_script(f"window.open('{email_verify_link}', 'thirdtab')")
       driver.switch_to.window(driver.window_handles[2])

       time.sleep(.5)

       close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="flex items-center  btn btn-primary btn-md btn-normal") and (contains(text(), "Close"))]')))
       close_button.click()

       elevenlabs_email_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="block w-full rounded-md bg-transparent border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm ") and (@type="email")]')))
       elevenlabs_email_input.click()
       elevenlabs_email_input.send_keys(username)

       time.sleep(.5)

       elevenlabs_password_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="block w-full rounded-md bg-transparent border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm ") and (@type="password")]')))
       elevenlabs_password_input.click()
       elevenlabs_password_input.send_keys(password)

       time.sleep(.5)

       continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-circle btn-primary btn-lg disabled:bg-gray-200"]')))
       continue_button.click()

       time.sleep(.5)

       elevenlabs_name = names.get_first_name()
       elevenlabs_name_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="block w-full rounded-md bg-transparent border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm ") and (@type="text")]')))
       elevenlabs_name_input.click()
       elevenlabs_name_input.send_keys(elevenlabs_name)

       time.sleep(.5)

       elevenlabs_reference_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="btn btn-white btn-md btn-normal justify-between flex-grow text-sm w-full border-gray-300")]')))
       elevenlabs_reference_input.click()

       time.sleep(.5)

       elevenlabs_reference_answer = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="flex h-fit items-center flex-wrap") and (@aria-label="Twitter")]')))
       elevenlabs_reference_answer.click()

       time.sleep(.5)

       next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="flex items-center  btn btn-primary btn-md btn-normal mt-6 ml-auto w-24 max-[800px]:w-full")]')))
       next_button.click()

       time.sleep(.5)

       engineer_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="block font-serif text-sm font-light text-gray-700 text-[14px]") and (contains(text(), "Personal projects, Software engineer, Game engineer, CTO"))]')))
       engineer_button.click()

       time.sleep(.5)

       personal_project_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="block font-serif text-lg font-bold text-black text-[16px]") and (contains(text(), "Personal project"))]')))
       personal_project_button.click()

       with open(current_dir + '\\.elevenlabs_credentials', '+a') as f:
              f.write('Username: ' + username + '\n')
              f.write('Password: ' + password + '\n\n')
       
       time.sleep(.5)
       
       my_account_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[(@class="truncate") and (contains(text(), "My Account"))]')))
       my_account_button.click()

       time.sleep(.5)

       profile_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="text-gray-800 hover:bg-gray-50 group flex w-full items-center gap-x-3 rounded-md p-2 text-sm font-semibold leading-6 focus:outline-none focus:ring-2 focus:ring-gray-500"]')))
       profile_button.click()

       time.sleep(.5)

       reveal_key_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="flex items-center  btn btn-white btn-md btn-normal border-l-0 rounded-none"]')))
       reveal_key_button.click()

       time.sleep(.5)

       key = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="block w-full rounded-md bg-transparent border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm  rounded-r-none"]'))).get_attribute('value')

       print('WRITING API KEY TO .api FILE')
       with open(current_dir + '\\.api', 'r') as f:
              lines = f.readlines()

       for idx, line in enumerate(lines):
              if 'ELEVENLABS_API_KEY' in line:
                     lines[idx] = 'ELEVENLABS_API_KEY = ' + key + '\n'
                     
       with open(current_dir + '\\.api', 'w') as f:
              f.writelines(lines)

       print('API KEY GENERATION COMPLETE')