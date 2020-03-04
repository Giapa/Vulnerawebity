from time import sleep
from random import uniform
from soup_methods import find_links, find_buttons, find_inputs
from bs4 import BeautifulSoup
from init import initialize
from difflib import SequenceMatcher

global available
global queue

def available_links(driver,site):
    domain = site.split('.')[0]
    driver.get(site)
    sleep(2)
    home = driver.page_source
    available.add('/')
    while len(queue) != 0 : 
        link = queue[0] 
        driver.get(f'{site}{link}')
        sleep(uniform(1.3,1.7))
        page = driver.page_source
        seq = SequenceMatcher(a=home,b=page)
        ratio = seq.ratio()
        if '404' not in page and page and ratio <= 0.82:
            soup = BeautifulSoup(page,'html.parser')
            for ref in find_buttons(soup,queue,available):
                if ref not in queue and ref not in available:
                    queue.append(ref)
            for ref in find_links(soup,domain,queue,available):
                if ref not in queue and ref not in available:
                    queue.append(ref)
            available.add(queue.pop(0))
        else:
            queue.pop(0)

def check_form_val(driver,site):
    for link in available:
        driver.get(f'{site}{link}')
        sleep(uniform(1.5,1.8))
        page = driver.page_source
        soup = BeautifulSoup(page,'html.parser')
        if find_inputs(soup):
            print(f'{site}{link} has inputs you can exploit')
        else:
            print(f'{site}{link} has no input form to exploit')


if __name__ == '__main__':
    queue = list()
    available = set()
    form_vul = set()
    driver = initialize()
    site = input('Give site full url: ')
    with open('checklist.txt','r') as file:
        lines = file.readlines()
        for line in lines:
            queue.append(line.replace('\n',''))
    available_links(driver,site)
    print('Available Ulrs: ')
    for link in available:
        print(f'---{link}')
    print('----------------- \n')
    check_form_val(driver,site)