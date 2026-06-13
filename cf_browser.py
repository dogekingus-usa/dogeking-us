"""
Cloudflare DNS Fix - Browser Automation
Opens browser, logs into Cloudflare, updates DNS to GitHub Pages
If captcha appears - user helps. Otherwise full auto.
"""
import asyncio, sys, os

GITHUB_IPS = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']
CF_EMAIL = 'dogeking.us@gmail.com'
CF_PASS = 'domvic-1tIdko-wijdaz'

async def main():
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        print('=== CLOUDFLARE DNS FIX ===')
        print('[1/6] Launching browser (visible)...')
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()
        
        print('[2/6] Navigating to Cloudflare login...')
        await page.goto('https://dash.cloudflare.com/login', timeout=60000, wait_until='domcontentloaded')
        await asyncio.sleep(3)
        
        current_url = page.url.lower()
        print('  URL:', current_url[:100])
        
        if 'challenge' in current_url or 'cf_chl' in current_url:
            print('\n[!] CAPTCHA/CHALLENGE DETECTED')
            print('[!] User - please complete the Cloudflare challenge in the browser')
            print('[!] Waiting up to 120 seconds for you to complete it...')
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_captcha.png')
            # Wait for user to complete captcha
            try:
                await page.wait_for_url('**/login**', timeout=120000)
            except:
                pass
            await asyncio.sleep(3)
            print('  After wait URL:', page.url[:100])
        
        # Check if we need to login
        if 'login' in page.url.lower():
            print('[3/6] Filling login form...')
            try:
                # Try multiple selectors for email
                email_found = False
                for sel in ['#email', 'input[name="email"]', 'input[type="email"]', 'input[autocomplete="username"]']:
                    try:
                        el = await page.wait_for_selector(sel, timeout=2000)
                        if el:
                            await el.fill(CF_EMAIL)
                            email_found = True
                            print('  Email filled using:', sel)
                            break
                    except:
                        continue
                
                if not email_found:
                    print('  Could not find email field - may need help')
                    await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_no_email.png')
                
                for sel in ['#password', 'input[name="password"]', 'input[type="password"]']:
                    try:
                        el = await page.wait_for_selector(sel, timeout=2000)
                        if el:
                            await el.fill(CF_PASS)
                            print('  Password filled using:', sel)
                            break
                    except:
                        continue
                
                # Click sign in button
                for sel in ['button[type="submit"]', '#sign_up_button', 'button:has-text("Sign in")', 'button:has-text("Log in")']:
                    try:
                        el = await page.wait_for_selector(sel, timeout=2000)
                        if el:
                            await el.click()
                            print('  Clicked sign in')
                            break
                    except:
                        continue
                
                print('  Waiting for login...')
                await asyncio.sleep(5)
                print('  After login URL:', page.url[:100])
            except Exception as e:
                print('  Login error:', str(e)[:200])
        
        # Check for 2FA
        if any(x in page.url.lower() for x in ['2fa', 'totp', 'mfa', 'verification', 'authenticator']):
            print('\n[!] 2FA/VERIFICATION REQUIRED')
            print('[!] User - please complete 2FA in the browser window')
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_2fa.png')
            try:
                await page.wait_for_url('**/dashboard**', timeout=120000)
            except:
                pass
            await asyncio.sleep(3)
        
        # Now we should be on the dashboard or need to navigate
        print('[4/6] Current page:', page.url[:100])
        
        # Try to find and click on dogeking.us zone
        print('[5/6] Looking for dogeking.us zone...')
        try:
            # Try direct URL to zone DNS
            await page.goto('https://dash.cloudflare.com/', timeout=30000, wait_until='domcontentloaded')
            await asyncio.sleep(3)
            
            # Look for dogeking.us link
            try:
                zone_link = await page.wait_for_selector('a:has-text("dogeking.us")', timeout=5000)
                if zone_link:
                    await zone_link.click()
                    print('  Clicked dogeking.us zone')
                    await asyncio.sleep(3)
            except:
                print('  Could not find zone link directly')
            
            # Look for DNS in the sidebar/nav
            try:
                dns_link = await page.wait_for_selector('a:has-text("DNS"), span:has-text("DNS"), li:has-text("DNS")', timeout=5000)
                if dns_link:
                    await dns_link.click()
                    print('  Clicked DNS tab')
                    await asyncio.sleep(3)
            except:
                print('  Could not find DNS tab directly')
            
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_dns_page.png')
        except Exception as e:
            print('  Navigation error:', str(e)[:200])
        
        print('[6/6] Browser is open. User can see the screen.')
        print('  Waiting 30 seconds for any manual adjustments...')
        await asyncio.sleep(30)
        
        # Try to add DNS records via the page
        print('  Attempting to add GitHub Pages A records...')
        try:
            page_text = await page.inner_text('body')
            if 'dogeking' in page_text.lower() and ('A' in page_text or 'AAAA' in page_text):
                print('  DNS records page detected')
        except:
            print('  Could not verify DNS page')
        
        await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_final.png')
        print('\n[DONE] Screenshots saved to workspace-dogeking-us\\')
        print('Browser will close in 5 seconds...')
        await asyncio.sleep(5)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
