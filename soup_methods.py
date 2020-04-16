#Find all links 
def find_links(soup,domain,queue,crawled):
    new_list = list()
    #Find all links
    links = soup.find_all('a',{'href':True})
    #Loop through links
    for a in links:
        href = a['href'] 
        #Check if links are valid
        if domain in href or '#/' in href or '.html' in href: 
            if href not in crawled and href not in queue and href not in new_list: 
                new_list.append(href)
    return new_list

#Find available buttons
def find_buttons(soup,queue,crawled):
    new_list = list()
    #Find all links connected to buttons
    buttons = soup.find_all('button',{'routerlink':True})
    #Loop through buttons
    for button in buttons:
        href = button['routerlink']
        #Check if link is alreaded referenced
        if href not in crawled and href not in queue and href not in new_list: 
                new_list.append(href)
    #Return results
    return new_list

#Find available inputs
def find_inputs(soup):
    #Get all inputs
    inputs = soup.find_all('input')
    #If inputs are available
    if inputs is not None:
        return True
    else:
        return False