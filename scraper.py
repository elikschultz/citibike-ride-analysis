# Imports and setup
from selenium import webdriver
from dateutil.parser import parse
import random
import time
from datetime import timedelta
import pandas as pd
from selenium.webdriver.common.keys import Keys
import os
import sys

# Ensure driver is in path (TO BE MODIFIED)
sys.path.insert(0, os.getcwd() + 'chromedriver.exe')


login_url = 'https://account.citibikenyc.com/ride-history'
phone_number = input('Please enter the phone number associated with your Citi Bike account (just numbers, starting with area code): ')


# Navigate to webpage
browser = webdriver.Chrome()
browser.get((login_url))



### Perform login ###

# Enter and submit phone number
phone_number_web_element = browser.find_element_by_id('phone')
phone_number_web_element.send_keys(phone_number)

next_button_web_element = browser.find_element_by_xpath("//button[@data-testid='formSubmit']")
next_button_web_element.click()

# Enter and submit verification code
verification_code = input('Please enter the six-digit verification code that was sent to your phone: ')

verification_code_web_element = browser.find_element_by_xpath("//input[@data-testid='verification-code-field']")
verification_code_web_element.send_keys(verification_code)

time.sleep(5)

confirmation_button_web_element = browser.find_element_by_xpath("//button[@data-aid='challenge']")
confirmation_button_web_element.click()

# Enter and submit email associated with account
email = input('Please enter the email address associated with your account: ')

email_web_element = browser.find_element_by_xpath("//input[@name='email']")
email_web_element.send_keys(email)

submit_email_button_web_element = browser.find_element_by_xpath("//button[@data-testid='form-submit']")
submit_email_button_web_element.click()

time.sleep(10)

# If banner pops up, close it
try:
    cookie_banner_close_web_element = browser.find_element_by_xpath("//button[@class='optanon-alert-box-close banner-close-button']")
    cookie_banner_close_web_element.click()
    
except:
    pass

### Show all rides and ride details ###
# Show all rides
while True:
    try:
        show_more_button_web_element = browser.find_element_by_xpath("//button[@data-testid='DATA_TESTID_SHOW_MORE']")
        try:
            show_more_button_web_element.click()
            time.sleep(0.25 + random.random())
        except:
            time.sleep(5)
            show_more_button_web_element.click()
    except:
        break

time.sleep(5)

# Show all ride details
browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME) # Scroll to top of page to avoid overlay interfering with button
ride_details_web_elements = browser.find_elements_by_xpath("//div[@data-testid ='DATA_TESTID_RIDE_OVERVIEW_CARD']")

for ride_detail in ride_details_web_elements:
    try:
        try:
            ride_detail.click()
            time.sleep(random.random())
        except:
            time.sleep(5)
            ride_detail.click()
    except:
        print('Error while expanding ride details.')
        raise
        
    
### Scrape and output ride information ###
ride_details_full = browser.find_elements_by_xpath("//div[@data-testid = 'DATA_TESTID_RIDE_OVERVIEW_CARD']")
all_rides_df = pd.DataFrame(columns = ['ride_start_datetime', 'ride_end_datetime', 'ride_start_location',
                                       'ride_end_location'])

for ride_detail_full in ride_details_full:
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    try:
        ride_data_raw = ride_detail_full.text.split('\n') + \
            ride_detail_full.find_element_by_xpath("..//div[@data-testid = 'DATA_TESTID_RIDE_DETAILS_INFO']").text.split('\n')
    except:
        ride_detail_full.click()
        time.sleep(2)
        ride_data_raw = ride_detail_full.text.split('\n') + \
            ride_detail_full.find_element_by_xpath("..//div[@data-testid = 'DATA_TESTID_RIDE_DETAILS_INFO']").text.split('\n')
        
    ride_data = dict()
    ride_data['ride_start_datetime'] = [parse(ride_data_raw[0] + ' ' + ride_data_raw[2].split(maxsplit = 2)[2])]
    try:
        ride_data['ride_end_datetime'] = [ride_data['ride_start_datetime'][0] + \
                  timedelta(minutes = int(ride_data_raw[3].split()[1]), seconds = int(ride_data_raw[3].split()[3]))]
    except IndexError:
        ride_data['ride_end_datetime'] = [ride_data['ride_start_datetime'][0] + \
                  timedelta(minutes = int(ride_data_raw[3].split()[1]))]
        
    ride_data['ride_start_location'] = [ride_data_raw[6]]
    ride_data['ride_end_location'] = [ride_data_raw[8]]
    
    all_rides_df = all_rides_df.append(pd.DataFrame.from_dict(ride_data))
    
all_rides_df.to_csv('all_rides.csv', index = False)

browser.quit()
    