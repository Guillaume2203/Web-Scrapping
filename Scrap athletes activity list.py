import requests
import json
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import functions_strava as fs
import pandas as pd
from selenium.common.exceptions import TimeoutException

def strava_login_selen():
    
    #Initialisation of variables
    url_co = "https://www.strava.com/login"
    password = ""
    email = ""

    # Set-up of Selenium
    driver = webdriver.Chrome()
    url = driver.command_executor._url
    session_id = driver.session_id
    driver.maximize_window()
    driver.get(url_co)

    # Find the email and password fields and fill them in
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    print(email_field)
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)

    # Wait for the login process to complete and the dashboard to load
    WebDriverWait(driver, 10).until(EC.url_contains("dashboard"));
    
    # Return the driver object
    return driver

driver = strava_login_selen()

#Insert the date range
start_date = "2014-01-01"
end_date = "2023-07-01"

interval = pd.date_range(start=start_date, end=end_date, freq='M').strftime("%Y%m").tolist()

#Insert the athlete ID
athleteID=

listactID=pd.DataFrame({1:[0]})
listathID=pd.DataFrame({1:[0]})
listID=pd.DataFrame({1:[0]})

for w in interval:
    driver.set_page_load_timeout(90)
    driver.get(f"https://www.strava.com/athletes/{athleteID}#interval?interval={w}&interval_type=month&chart_type=miles&year_offset=0")
    time.sleep(90)


    import re
    # The provided HTML
    response=driver.page_source
    soup = BeautifulSoup(response, 'html.parser')

    target_divs = soup.find_all('div', attrs={'class': '------packages-feed-ui-src-components-media-Card-Card__feed-entry--WKvAQ ------packages-feed-ui-src-components-media-Card-Card__card--dkL_L', 'data-testid': 'web-feed-entry'})

    # Print the extracted elements (you can process them as needed)
    for target_div in target_divs:
       # Regular expressions patterns to extract href values
        activity_id_pattern = r'/activities/(\d+)'
        athlete_id_pattern = r'/athletes/(\d+)'

        # Extract the activity ID
        anchor_tag = target_div.find('a', href=re.compile(activity_id_pattern))
        if anchor_tag:
        # Extract the activity ID using the regular expression search
            activity_id_match = re.search(activity_id_pattern, anchor_tag['href'])
        if activity_id_match:
                activity_id = activity_id_match.group(1)
                print(f"Activity ID: {activity_id}")
        
        # Find the anchor tag for athlete ID within the div element
        athlete_anchor_tag = target_div.find('a', href=re.compile(athlete_id_pattern))
        if athlete_anchor_tag:
            # Extract the athlete ID using the regular expression search
            athlete_id_match = re.search(athlete_id_pattern, athlete_anchor_tag['href'])
            if athlete_id_match:
                athlete_id = athlete_id_match.group(1)
                print(f"Athlete ID: {athlete_id}")
        listactID=listactID.append({1: activity_id}, ignore_index=True)
        listathID=listathID.append({1: athlete_id}, ignore_index=True)

listID=listID.append(pd.concat([listactID, listathID], axis=1))
listID = listID.loc[(listID != 0).all(axis=1)]


# Text you want to add
text_to_add = "https://www.strava.com/activities/"
listID['1'] = text_to_add + listID['1'].astype(str)
listID = listID.iloc[:, 0]


listID.to_csv(f'dir/activitiesID_{athleteID}_{start_date}-{end_date}.csv', index=False)