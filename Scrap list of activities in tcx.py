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
import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import filedialog
import csv
import numpy as np
import random



def strava_login_selen():
    
    #Initialisation of variables
    url_co = "https://www.strava.com/login"
    email = ""
    password = ""

    # Set-up of Selenium
    driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_extension('./eigiefcapdcdmncdghkeahgfmnobigha.crx')
    prefs = {"download.default_directory" : r""} #insert download directory
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options) 
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

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select a CSV file using the file dialog
file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
actID = pd.read_csv(file_path, skiprows=1)
actID = np.array(actID.values.flatten())

n=0
N=len(actID)
for act in actID:
    driver.set_page_load_timeout(45)
    driver.get(act)
    T=random.randint(30, 45)
    time.sleep(T)

    try:
        button = driver.find_element(By.CSS_SELECTOR, ".slide-menu.drop-down-menu.enabled.align-bottom")
        # Click the button
        button.click()
        Export_tcx = driver.find_element(By.CSS_SELECTOR, "a.tcx")
        # Click the link
        Export_tcx.click()
    except Exception:
        # Handle the case when the button element is not present
        print("Button not found. Skipping the subsequent lines of code.")



    T=random.randint(15, 25)
    time.sleep(T)
    n=n+1
    print(f"{n} out of {N}")






