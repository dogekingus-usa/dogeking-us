"""
Undetected Chrome - Cloudflare DNS fix
"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import json
import sys

GITHUB_IPS = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']
CF_EMAIL = 'dogeking.us@gmail.com'
CF_PASS = 'domvic-1tIdko-wijdaz'

print('[1/5] Starting undetected Chrome...')
driver = uc.Chrome(headless=True, use_subprocess=True)
driver.set_window_size(1280, 900)

print('[2/5] Navigating to Cloudflare login...')
driver.get('https://dash.cloudflare.com/login')
time.sleep(5)
print('  Title:', driver.title)
print('  URL:', driver.current_url)
driver.save_screenshot('C:\\Users\\SAMPC\\workspace-dogeking-us\\uc_login.png')

# Check if we're on login page
if 'login' in driver.current_url.lower():
    print('[3/5] Logging in...')
    try:
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        email_input.send_keys(CF_EMAIL)
        pass_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        pass_input.send_keys(CF_PASS)
        submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit.click()
        print('  Login submitted')
        time.sleep(8)
        print('  After login URL:', driver.current_url)
        driver.save_screenshot('C:\\Users\\SAMPC\\workspace-dogeking-us\\uc_after_login.png')
    except Exception as e:
        print(f'  Login error: {e}')
        driver.save_screenshot('C:\\Users\\SAMPC\\workspace-dogeking-us\\uc_login_error.png')
        driver.quit()
        sys.exit(1)

# Check for 2FA
if any(x in driver.current_url.lower() for x in ['2fa', 'totp', 'verification', 'challenge']):
    print('[!] 2FA/Verification required')
    driver.save_screenshot('C:\\Users\\SAMPC\\workspace-dogeking-us\\uc_2fa.png')
    print('  Screenshot saved for user review')
    driver.quit()
    sys.exit(2)

print('[4/5] Navigating to DNS...')
try:
    # Go to dogeking.us zone DNS
    driver.get('https://dash.cloudflare.com/?to=/:zone/dns')
    time.sleep(5)
    print('  DNS page URL:', driver.current_url)
    driver.save_screenshot('C:\\Users\\SAMPC\\workspace-dogeking-us\\uc_dns.png')
    
    # Look for the zone
    try:
        zone_link = driver.find_element(By.XPATH, '//a[contains(text(), "dogeking.us")]')
        zone_link.click()
        time.sleep(3)
        print('  Clicked dogeking.us zone')
    except:
        print('  Could not find zone link, may already be on zone page')
    
    # Look for DNS Records tab
    try:
        dns_tab = driver.find_element(By.XPATH, '//a[contains(text(), "DNS")] | //span[contains(text(), "DNS")]')
        dns_tab.click()
        time.sleep(3)
        print('  Clicked DNS tab')
    except:
        print('  May already be on DNS page')
    
    driver.save_screenshot('C:\\Users\\SAMPC\\workspace-dogeking-us\\uc_dns_records.png')
except Exception as e:
    print(f'  DNS navigation error: {e}')
    driver.save_screenshot('C:\\Users\\SAMPC\\workspace-dogeking-us\\uc_dns_error.png')

print('[5/5] Removing old records and adding new ones...')
try:
    # Find all A records and delete them
    rows = driver.find_elements(By.XPATH, '//tr[.//td[contains(text(), "A")]]')
    print(f'  Found {len(rows)} A records')
    
    # Also find all AAAA records
    rows_aaaa = driver.find_elements(By.XPATH, '//tr[.//td[contains(text(), "AAAA")]]')
    print(f'  Found {len(rows_aaaa)} AAAA records')
    
    for row in rows + rows_aaaa:
        try:
            delete_btn = row.find_element(By.XPATH, './/button[contains(@aria-label, "Delete")] | .//button[contains(text(), "Delete")]')
            delete_btn.click()
            time.sleep(1)
            # Confirm
            confirm = driver.find_element(By.XPATH, '//button[contains(text(), "Delete")] | //button[contains(text(), "Confirm")]')
            confirm.click()
            time.sleep(2)
            print('  Deleted one record')
        except:
            print('  Could not delete a record')
    
    # Add new A records
    for ip in GITHUB_IPS:
        try:
            add_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Add Record")] | //a[contains(text(), "Add Record")]')
            add_btn.click()
            time.sleep(1)
            
            # Select type
            type_select = driver.find_element(By.XPATH, '//select[contains(@name, "type") or contains(@id, "type")]')
            type_select.send_keys('A')
            time.sleep(0.5)
            
            # Fill value
            value_input = driver.find_element(By.XPATH, '//input[contains(@name, "content") or contains(@name, "value") or contains(@placeholder, "IPv4")]')
            value_input.clear()
            value_input.send_keys(ip)
            time.sleep(0.5)
            
            # Toggle proxy OFF
            try:
                proxy_check = driver.find_element(By.XPATH, '//input[@type="checkbox" and contains(@name, "proxied")]')
                if proxy_check.is_selected():
                    proxy_check.click()
                    time.sleep(0.5)
            except:
                pass
            
            # Save
            save_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Save")] | //button[contains(text(), "Add")]')
            save_btn.click()
            time.sleep(2)
            print(f'  Added A record: {ip}')
        except Exception as e:
            print(f'  Error adding record {ip}: {e}')
except Exception as e:
    print(f'  Error in DNS modification: {e}')

driver.save_screenshot('C:\\Users\\SAMPC\\workspace-dogeking-us\\uc_final.png')
print('[DONE] Screenshots saved. Check results.')
time.sleep(3)
driver.quit()
