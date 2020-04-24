from functions.request_functions import search,has_ajax,check_for_vulnerabilities
from functions.selenium_functions import available_links,check_form_val,loginsqlinjection,xssattack
from functions.init import initialize
from bs4 import BeautifulSoup
from functions.soup_methods import find_inputs
from time import sleep

#Run it with different ip address
def get_proxy():
    ansP=input('\nDo you want to use proxies? ')

    if ansP in yes:
        #Open the file
        with open(input('\nGive the full path: '),'r') as file:
            line = file.readline()
            proxy=line.split('\n')[0]

            return proxy
    else:
        return None

#For static sites
def run_static(site,proxy):
    is_vulnerable = False
    print('\nFinding available urls of the given site')

    crawled = search(site,proxy)

    for link in crawled:
        print(f'---: {link}')

    vulnerable_links = check_for_vulnerabilities(site,proxy,crawled)
    
    if len(vulnerable_links) > 0:

        for link in vulnerable_links:

            if any('login' in url for url in vulnerable_links) or any('signup' in url for url in vulnerable_links):
                print(f'{link}: is probably vulnerable to Sql Injection')
                is_vulnerable = True
            else:
                print(f'{link}: is probably vurnerable to XSS attack')
                is_vulnerable = True
    else:
        print('\nNo available inputs for XSS and SQL injections')
    
    if is_vulnerable:

        ans = input('\nThere is a probability for vulnerabilities.Do you want to test them?[y,n] ')
        if ans in yes:
            driver = initialize(proxy)
            #check if link has login for sql injection
            if any('login' in url for url in vulnerable_links):
                loginsqlinjection(site,'/login',driver)
            elif any('signin' in url for url in vulnerable_links):
                loginsqlinjection(site,'/signin',driver)
            else:
                print('No login or signin page for SQL injection testing')

            #Get results of xss
            response = xssattack(driver,site,vulnerable_links)
            #Print results of xss
            if response is None:
                print('Xss attacks failed')
            else:
                print('Your page is vulnerable to Xss attacks')

            driver.quit()
            
             

#For sites with javascript enabled
def run_dynamic(site,proxy):
    #Basic queue for crawling
    queue = list()
    #Set of available links
    available = set()

    #Init webdriver
    driver = initialize(proxy)
    driver.get(site)
    site = driver.current_url

    #Init list an set
    queue.append('/')
    available.add('/')
    
    print('\nFinding available urls of the given site')

    #Find available links
    available_links(driver,site,queue,available)
    #Print available links
    print('Available Urls:')
    for link in available:
        print(f'---: {link}')
    print('')

    #Check for inputs
    vulnerable_links = check_form_val(driver,available,site)
    #Print threat level of links
    for vul_link in vulnerable_links:

        if 'login' in vul_link or 'signup' in vul_link:
            print(f'{vul_link} : is probably vulnerable to Sql Injection')
        else:
            print(f'{vul_link} : is probably vurnerable to XSS attack')

    ans = input('\nThere is a probability for vulnerabilities.Do you want to test them?[y,n] ')

    if ans in yes:

        #check if link has login for sql injection
        if any('login' in url for url in vulnerable_links):
            loginsqlinjection(site,'/login',driver)
        elif any('signin' in url for url in vulnerable_links):
            loginsqlinjection(site,'/signin',driver)
        else:
            print('No login or signin page for SQL injection testing')

        #Get results of xss
        response = xssattack(driver,site,vulnerable_links)
        #Print results of xss
        if response is None:
            print('Xss attacks failed')
        else:
            print('Your page is vulnerable to Xss attacks')

    driver.quit()


if __name__ == "__main__":
    yes = ['Yes','yes','Y','y']

    site = input('Give site url: ')

    proxy=get_proxy()
    
    if not has_ajax(site,proxy):
        run_static(site,proxy)
        
    else:
        ans = input('\nWe found ajax calls so we need a different approach. Would you like to get the big guns? [y,n]: ')

        if ans in yes:
            run_dynamic(site,proxy)
            print('\nVulnerability testing is finished.\nGoodbye!')
        else:
            print('Thank you for using our tool.\nGoodbye!')
