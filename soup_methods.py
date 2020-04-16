
def find_links(soup,domain,queue,crawled):
    new_list = list()
    links = soup.find_all('a',{'href':True})
    for a in links:
        href = a['href'] 
        if domain in href or '#/' in href: 
            if href not in crawled and href not in queue and href not in new_list: 
                new_list.append(href)
    return new_list

def find_buttons(soup,queue,crawled):
    new_list = list()
    buttons = soup.find_all('button',{'routerlink':True})
    for button in buttons:
        href = button['routerlink']
        if href not in crawled and href not in queue and href not in new_list: 
                new_list.append(href)
    return new_list

def find_inputs(soup):
    inputs = soup.find_all('input')
    if inputs is not None:
        return True
    else:
        return False