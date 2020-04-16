from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

class Actions():

    def scroll_end(self, driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.END)

    def scroll_up(self, driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)

    def scroll_down(self, driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

    def refresh(self, driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.F5)

def initialize():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--ignore-certificate-error")
    opts.add_argument("--incognito")
    opts.add_argument("--start-maximized")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

    driver = webdriver.Firefox(firefox_options=opts)

    return driver