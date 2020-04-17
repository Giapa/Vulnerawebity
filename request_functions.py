import requests
from bs4 import BeautifulSoup
from soup_methods import find_links, find_buttons, find_inputs
import json

#---Request methods---
def search(site): 
    queue = list() 
    crawled = set() 
    queue.append('/')
    domain = site.split('.')[0]
    while len(queue) != 0 : 
        link = queue[0] 
        page = requests.get(f'{site}{link}')
        soup = BeautifulSoup(page.content,'html.parser')
        queue.extend(find_buttons(soup,queue,crawled))
        queue.extend(find_links(soup,domain,queue,crawled))
        crawled.add(queue.pop(0))
    return crawled

def has_ajax(site):
    page = requests.get(site)
    if 'ajax' in page.content.decode('utf-8'):
        return True
    else:
        return False
<<<<<<< HEAD

def check_urls():
    with open('checklist.txt','r') as file:
        lines = file.readlines()
    for line in lines:
        page = requests.get('https://giapa.github.io/'+line)
        print(page.content.decode('utf-8'))

if __name__ == '__main__':
    queue = list() 
    crawled = set() 
    site = input('Give site full url: ')
    queue.append('/')
    if  not has_ajax(site):
        search(site)
        for page in crawled:
            if page!='/':
                newlink=requests.get(page)
                soup=BeautifulSoup(newlink.content,'html.parser')
                if  find_inputs(soup):
                    print('inputs found at page:',page)
    else:
        ans=input('We found ajax calls so we need a different approach. Would you like to get big guns? [y,n]')    
   
=======
>>>>>>> 43724b80f14baed8595887bace2e7b5b687c40b4
