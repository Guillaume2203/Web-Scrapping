from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import telepot
import requests
import re
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
import time
import scrapfly

token = "token" #insert the token of your telegram bot
chat_id = "ID" #insert the chat id of you telegram channel
bot = telepot.Bot(token)

import subprocess
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

# Replace with the path to your web driver executable
driver_path = "path/to/web/driver"
# Create a new instance of the web driver
chrome_options = Options()
chrome_options.add_argument('--headless')


# Create the WebDriver instance with the options
driver = webdriver.Chrome(options=chrome_options)

#go to Twitter's Homepage
driver.get("https://twitter.com/login")
time.sleep(30)

username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys("username") #Insert the twitter username or email
next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
next_button.click()

### If unusual connection is asked
time.sleep(30)
try:
    # Check if an element with the specified selector exists
    element = driver.find_element(By.XPATH,"//input[@name='text']")
    element.send_keys("phone_number") #insert your phone number
    next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
    next_button.click()
except NoSuchElementException:
    print("Element not found!")

time.sleep(30)
password = driver.find_element(By.XPATH,"//input[@name='password']")
password.send_keys('password') #Insert your password
log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
log_in.click()

time.sleep(30)
Cookies = driver.find_element(By.XPATH,"//span[contains(text(),'Accept')]")
Cookies.click()

#Notif = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[3]")
#Notif.click()
#time.sleep(10)
#Notif2 = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[1]/div/div/article")
#Notif2.click()
#time.sleep(3)



## Loop without end

from datetime import date
import datetime
today = date.today()
twitter_ids_filename = 'all_ids.json'
id_selector = '.time a.tweet-timestamp'
tweet_selector = 'li.js-stream-item'
ids = []
def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])
def form_url(since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  user + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
    return p1 + p2
def increment_day(date, i):
    return date + datetime.timedelta(days=i)

#list of all users - loop for
file_path = ""  # Replace with the correct file path where the csv file containing all usernames is located
import pandas as pd
# Read a CSV file into a DataFrame
users = pd.read_csv(file_path)
users = np.array(users)


d1 = format_day(increment_day(today, +1))
d2 = format_day(increment_day(today, -3))

for user in users:
    time.sleep(30)
    url = form_url(d2, d1)
    url = ''.join(url)
    print(user)
    print(d2, "|", d1)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    driver.get(url)
    time.sleep(25)

    Recent = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a")
    Recent.click()
    time.sleep(30)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # Alternatively, you can scroll down by a specific amount
    driver.execute_script("window.scrollBy(0, 500)")
    # Wait for the page to load
    time.sleep(25)

    response=driver.page_source

    soup = BeautifulSoup(response, 'html.parser')
    # Find all the anchor tags with href attributes
    anchor_tags = soup.find_all('a', href=True)

    # Extract the href values
    href_values = [tag['href'] for tag in anchor_tags]

    # Print the extracted href values
    filtered_values = [href for href in href_values if "status/" in href and "analytics" not in href]
    filtered_values = [line for line in filtered_values if line.count('/') <= 3]
    filtered_values = list(set(filtered_values))
    u = str(user)
    u = u.strip("[]'")
    filtered_values = [item for item in filtered_values if u in item]



    # Read a CSV file into a DataFrame
    Tweets = pd.read_csv("dir/Tweets_viewed.csv") #Insert the path where the csv file of already scrapped tweet is located
    
    for tweet_url in filtered_values:
            # extract all url in temp
        base_url = "https://twitter.com"
        merged_url = base_url + tweet_url
        while True:
            if merged_url in Tweets.values:
                print("Next") 
                break
            else:
                driver.get(merged_url)
                time.sleep(20)
                driver.save_screenshot("dir/1.png")
                time.sleep(20)

                image_path="dir/1.png"
                    
                image = Image.open(image_path)
                # Convert image to a file-like object
                image = image.convert("RGB")
                temp_file_path = "temp_image.jpg"
                image.save(temp_file_path, format="JPEG")
                
                
                
                while True:
                        time.sleep(15)
                        try:
                            bot.sendPhoto(chat_id=chat_id, photo=open(temp_file_path, "rb"))
                            break  # If no error occurs, exit the loop
                        except Exception as e:
                            time.sleep(20)
                            print(f"An error occurred: {e}")
                        
                print(merged_url)
                while True:
                        time.sleep(18)
                        try:
                            url1 = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={merged_url}&disable_web_page_preview=True"
                            requests.get(url1)
                            print(url1)
                            break  # If no error occurs, exit the loop
                        except Exception as e:
                            time.sleep(20)
                            print(f"An error occurred: {e}")

                time.sleep(15)
                break

        Tweets = Tweets.append({'1': merged_url}, ignore_index=True)
    Tweets.to_csv('dir/Tweets_viewed.csv', index=False)
    # Print the merged URL