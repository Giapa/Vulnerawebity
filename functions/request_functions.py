import requests
from bs4 import BeautifulSoup
from .soup_methods import find_links, find_buttons, find_inputs
import json
from .selenium_functions import available_links

#Find available urls
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

#Check for input vulnerabilities
def check_for_vulnerabilities(site,proxy,crawled):
    vulnerable_links = []

    for link in crawled:
        #for each new link
        new_link=site+link

        if proxy is not None:
            response = requests.get(new_link,proxies=proxy)
        else:
            response = requests.get(new_link)        

        soup= BeautifulSoup(response.content,'html.parser')

        if (find_inputs(soup)):
            vulnerable_links.append(link)
            
    return vulnerable_links

#Check if the site needs javascript enabled
def has_ajax(site,proxy):
    
    if proxy is not None:
        page = requests.get(site,proxies=proxy)
    else:
        page = requests.get(site)

    decoded=page.content.decode('utf-8')

    if 'ajax' and 'jquery' in decoded:
        return True
    else:
        return False
