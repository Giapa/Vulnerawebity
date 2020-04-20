from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

class Actions():

    def scroll_end(self, driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.END)

    def scroll_up(self, driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)

    def scroll_down(self, driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

    def refresh(self, driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.F5)

def initialize(proxy):
    opts = Options()
    #opts.add_argument("--headless")
    opts.add_argument("--ignore-certificate-error")
    opts.add_argument("--incognito")
    opts.add_argument("--start-maximized")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

    if(proxy is not None):
        #if proxy exists initialiaze it manually
        prox=Proxy()
        prox.proxy_type=ProxyType.MANUAL
        if('https' in proxy):
            #secure protocol
            prox.ssl_proxy=proxy
        else:
            #simple http
            prox.http_proxy=proxy
        capabilities= webdriver.DesiredCapabilities.FIREFOX
        driver=webdriver.Firefox(firefox_options=opts,desired_capabilities=capabilities)
    else:
        driver = webdriver.Firefox(firefox_options=opts)

    return driver