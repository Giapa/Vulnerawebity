import requests
from bs4 import BeautifulSoup
from soup_methods import find_links, find_buttons, find_inputs
import json
from selenium_functions import available_links

#---Request methods---
def search(site,proxy): 
    queue = list() 
    crawled = set() 
    queue.append('/')
    domain = site.split('.')[0]
    #if proxy exists use it
    if proxy is not None:
        while len(queue) != 0: 
            link = queue[0] 
            page = requests.get(f'{site}{link}',proxies=proxy)
            soup = BeautifulSoup(page.content,'html.parser')
            queue.extend(find_buttons(soup,queue,crawled))
            queue.extend(find_links(soup,domain,queue,crawled))
            crawled.add(queue.pop(0))
    else:
        #otherwise get site with default method
        while len(queue) != 0: 
                link = queue[0] 
                page = requests.get(f'{site}{link}')
                soup = BeautifulSoup(page.content,'html.parser')
                queue.extend(find_buttons(soup,queue,crawled))
                queue.extend(find_links(soup,domain,queue,crawled))
                crawled.add(queue.pop(0))
        
    return crawled

def has_ajax(site,proxy):
    if proxy is not None:
        page = requests.get(site,proxies=proxy)
        decoded=page.content.decode('utf-8')
    else:
        page = requests.get(site)
        decoded=page.content.decode('utf-8')
    if 'ajax' or 'jquery' in decoded:
        return True
    else:
        return False
