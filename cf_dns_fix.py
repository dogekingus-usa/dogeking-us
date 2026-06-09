"""
Cloudflare DNS Fix — Point dogeking.us to GitHub Pages
Using Playwright to automate Cloudflare dashboard
"""
import asyncio
import json
import sys

GITHUB_PAGES_IPS = [
    '185.199.108.153',
    '185.199.109.153',
    '185.199.110.153',
    '185.199.111.153',
]

CF_EMAIL = 'dogeking.us@gmail.com'
CF_PASS = 'domvic-1tIdko-wijdaz'

async def main():
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        # Launch browser
        print("[1/6] Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        print("[2/6] Navigating to Cloudflare login...")
        await page.goto('https://dash.cloudflare.com/login', wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Take screenshot to see what we got
        await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_step1_login.png')
        print("  Screenshot saved: cf_step1_login.png")
        
        # Check if we're already logged in (redirected)
        if 'login' not in page.url.lower():
            print("  Already logged in! URL:", page.url)
        else:
            # Fill login form
            print("[3/6] Filling login credentials...")
            try:
                # Try email field
                email_input = await page.wait_for_selector('input[type="email"], input[name="email"], input[placeholder*="email" i]', timeout=5000)
                await email_input.fill(CF_EMAIL)
                
                # Try password field
                pass_input = await page.wait_for_selector('input[type="password"], input[name="password"]', timeout=3000)
                await pass_input.fill(CF_PASS)
                
                # Click submit
                submit_btn = await page.wait_for_selector('button[type="submit"]', timeout=3000)
                await submit_btn.click()
                
                print("  Login form submitted. Waiting for redirect...")
                await asyncio.sleep(5)
                await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_step2_after_login.png')
                print("  Screenshot saved: cf_step2_after_login.png")
            except Exception as e:
                print(f"  Login form error: {e}")
                await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_step2_error.png')
                await browser.close()
                return False
        
        # Check if 2FA or verification needed
        current_url = page.url.lower()
        print(f"  Current URL after login: {current_url}")
        
        if '2fa' in current_url or 'totp' in current_url or 'verification' in current_url:
            print("[!] 2FA/Verification required! Need user to complete.")
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_step3_2fa.png')
            await browser.close()
            return False
        
        # Navigate to DNS settings for dogeking.us
        print("[4/6] Navigating to DNS settings...")
        try:
            await page.goto('https://dash.cloudflare.com/?to=/:zone/dns', wait_until='networkidle')
            await asyncio.sleep(3)
            
            # Try to find and click on dogeking.us zone
            zone_link = await page.query_selector('a:has-text("dogeking.us")')
            if zone_link:
                await zone_link.click()
                await asyncio.sleep(3)
            
            # Look for DNS tab/link
            dns_tab = await page.query_selector('a:has-text("DNS"), a:has-text("dns"), span:has-text("DNS"), li:has-text("DNS")')
            if dns_tab:
                await dns_tab.click()
                await asyncio.sleep(3)
            
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_step4_dns.png')
            print("  Screenshot saved: cf_step4_dns.png")
        except Exception as e:
            print(f"  Navigation error: {e}")
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_step4_error.png')
            await browser.close()
            return False
        
        # Delete existing A/AAAA records
        print("[5/6] Removing old A/AAAA records...")
        try:
            # Find and delete A records
            records = await page.query_selector_all('tr:has(td:has-text("A"))')
            print(f"  Found {len(records)} A records")
            for rec in records:
                delete_btn = await rec.query_selector('button:has-text("Delete"), button[aria-label*="Delete"], a:has-text("Delete")')
                if delete_btn:
                    await delete_btn.click()
                    await asyncio.sleep(1)
                    confirm_btn = await page.query_selector('button:has-text("Confirm"), button:has-text("Delete")')
                    if confirm_btn:
                        await confirm_btn.click()
                        await asyncio.sleep(1)
            
            # Find and delete AAAA records
            records_aaaa = await page.query_selector_all('tr:has(td:has-text("AAAA"))')
            print(f"  Found {len(records_aaaa)} AAAA records")
            for rec in records_aaaa:
                delete_btn = await rec.query_selector('button:has-text("Delete"), button[aria-label*="Delete"], a:has-text("Delete")')
                if delete_btn:
                    await delete_btn.click()
                    await asyncio.sleep(1)
                    confirm_btn = await page.query_selector('button:has-text("Confirm"), button:has-text("Delete")')
                    if confirm_btn:
                        await confirm_btn.click()
                        await asyncio.sleep(1)
        except Exception as e:
            print(f"  Delete records error: {e}")
        
        # Add GitHub Pages A records
        print("[6/6] Adding GitHub Pages A records...")
        try:
            for ip in GITHUB_PAGES_IPS:
                # Click Add Record button
                add_btn = await page.query_selector('button:has-text("Add Record"), button:has-text("Add"), a:has-text("Add Record")')
                if add_btn:
                    await add_btn.click()
                    await asyncio.sleep(1)
                
                # Select type A
                type_select = await page.query_selector('select[name="type"], select[id*="type"]')
                if type_select:
                    await type_select.select_option('A')
                    await asyncio.sleep(0.5)
                
                # Fill name
                name_input = await page.query_selector('input[name="name"], input[id*="name"], input[placeholder*="name" i]')
                if name_input:
                    await name_input.fill('@')
                    await asyncio.sleep(0.5)
                
                # Fill IPv4 address
                value_input = await page.query_selector('input[name="content"], input[name="value"], input[placeholder*="IPv4" i], input[placeholder*="address" i]')
                if value_input:
                    await value_input.fill(ip)
                    await asyncio.sleep(0.5)
                
                # Toggle proxy OFF (gray cloud)
                proxy_toggle = await page.query_selector('input[type="checkbox"][name="proxied"], span:has-text("Proxied")')
                if proxy_toggle:
                    # Check if it's checked (orange cloud = proxied)
                    is_checked = await proxy_toggle.is_checked()
                    if is_checked:
                        await proxy_toggle.click()  # Toggle off
                        await asyncio.sleep(0.5)
                
                # Save
                save_btn = await page.query_selector('button:has-text("Save"), button:has-text("Add")')
                if save_btn:
                    await save_btn.click()
                    await asyncio.sleep(1)
                    print(f"  Added A record: {ip}")
        except Exception as e:
            print(f"  Add records error: {e}")
        
        await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_step5_done.png')
        print("  Screenshot saved: cf_step5_done.png")
        
        print("\n[DONE] Cloudflare DNS update attempted. Check screenshots for results.")
        await asyncio.sleep(5)
        await browser.close()
        return True

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
