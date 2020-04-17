from request_functions import search,has_ajax
from selenium_functions import available_links,check_form_val,loginsqlinjection,xssattack
from init import initialize

#For static sites
def run_static(site):
    crawled = search(site)
    for link in crawled:
        print(f'Found available link: {link}')

#For sites with javascript enabled
def run_dynamic(site):
    #Basic queue for crawling
    queue = list()
    #Set of available links
    available = set()
    #Init webdriver
    driver = initialize()
    #Init list an set
    queue.append('/')
    available.add('/')
    print('\nFinding available urls of the given site')
    #Find available links
    available_links(driver,site,queue,available)
    #Print available links
    print('Available Urls:')
    for link in available:
        print(f'---{link}')
    print('\n')
    #Check for inputs
    vulnerable_links = check_form_val(driver,available,site)
    #Print threat level of links
    for vul_link in vulnerable_links:
        if 'login' in vul_link or 'signup' in vul_link:
            print(f'{vul_link} is probably vulnerable to Sql Injection')
        else:
            print(f'{vul_link} is probably vurnerable to XSS attack')

   # if '/login/' in  vulnerable_links: #check if link has login 
   #     loginsqlinjection(site,'/login/',driver)

    #Get results of xss
    response = xssattack(driver,site,available)
    #Print results of xss
    if response is None:
       print('\nXss attacks failed')
    else:
       print('\nThere are available xss attacks')


if __name__ == "__main__":
    site = input('Give site url: ')
    if not has_ajax(site):
        run_static(site)
    else:
        ans = input('\nWe found ajax calls so we need a different approach. Would you like to get the big guns? [y,n]: ')
        yes = ['Yes','yes','Y','y']
        if ans in yes:
            run_dynamic(site)
        else:
            print('Thank you for using our too\n Goodbye!')