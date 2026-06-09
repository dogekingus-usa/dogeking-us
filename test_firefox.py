"""Test Firefox with Selenium"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.add_argument('--headless')
print('Testing Firefox...')
driver = webdriver.Firefox(options=options)
driver.get('https://example.com')
print('Title:', driver.title)
ua = driver.execute_script('return navigator.userAgent')
print('User Agent:', ua)
driver.quit()
print('Firefox works!')
