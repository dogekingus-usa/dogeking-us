"""
DNS Fix - Real Edge Browser
"""
import time, sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By

GITHUB_IPS = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']
CF_EMAIL = 'dogeking.us@gmail.com'
CF_PASS = 'domvic-1tIdko-wijdaz'

print('[1/5] Launching Edge browser...')
options = webdriver.EdgeOptions()
options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
options.add_argument('--start-maximized')
driver = webdriver.Edge(options=options)

print('[2/5] Navigating to Cloudflare login...')
driver.get('https://dash.cloudflare.com/login')
time.sleep(5)
print('  Title:', driver.title)
print('  URL:', driver.current_url[:100])

if 'login' in driver.current_url.lower():
    print('[3/5] Logging in...')
    try:
        email_inp = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        email_inp.send_keys(CF_EMAIL)
        pass_inp = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        pass_inp.send_keys(CF_PASS)
        sub_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        sub_btn.click()
        print('  Login submitted')
        time.sleep(8)
        print('  After login:', driver.current_url[:100])
    except Exception as e:
        print('  Login error:', str(e)[:200])

if any(x in driver.current_url.lower() for x in ['2fa', 'totp', 'mfa', 'verification']):
    print('\n[!] 2FA required - complete in browser window')
    input('  Press Enter after completing 2FA...')

print('[4/5] Navigating to DNS...')
driver.get('https://dash.cloudflare.com/')
time.sleep(5)
print('  Dashboard:', driver.current_url[:100])

# Find dogeking.us zone
try:
    link = driver.find_element(By.XPATH, '//a[contains(text(), "dogeking.us")]')
    link.click()
    time.sleep(3)
    print('  Clicked dogeking.us')
except:
    print('  No zone link found')

# Find DNS tab
try:
    dns = driver.find_element(By.XPATH, '//a[contains(text(), "DNS")]')
    dns.click()
    time.sleep(3)
    print('  DNS tab clicked')
except:
    print('  No DNS tab found')

print('\n[5/5] BROWSER OPEN. Add these DNS records:')
for ip in GITHUB_IPS:
    print(f'  A record: @ -> {ip} (gray cloud)')
print('\n  Or tell me when DNS is updated and I verify.')

input('\n  Press Enter when done...')
driver.quit()
print('Done')
