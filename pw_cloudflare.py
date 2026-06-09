"""
Playwright - Cloudflare DNS update for GitHub Pages
Simplified approach
"""
import asyncio
import sys

GITHUB_IPS = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']
CF_EMAIL = 'dogeking.us@gmail.com'
CF_PASS = 'domvic-1tIdko-wijdaz'

async def main():
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        print('[1/4] Launching Playwright Chromium...')
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        page = await context.new_page()
        
        print('[2/4] Navigating to Cloudflare login...')
        try:
            await page.goto('https://dash.cloudflare.com/login', timeout=60000, wait_until='domcontentloaded')
            print(f'  Page loaded: {page.url[:80]}')
        except Exception as e:
            print(f'  Load error: {e}')
        
        await asyncio.sleep(3)
        await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw_step1.png')
        print('  Screenshot saved')
        
        # Try to fill login form
        current_url = page.url.lower()
        print(f'  URL: {current_url[:100]}')
        
        if 'login' in current_url:
            print('[3/4] Filling login form...')
            try:
                # Try various selectors for email field
                selectors = [
                    'input[type="email"]',
                    'input[name="email"]',
                    'input[autocomplete="email"]',
                    'input[autocomplete="username"]',
                    '#email',
                ]
                email_el = None
                for sel in selectors:
                    try:
                        email_el = await page.wait_for_selector(sel, timeout=2000)
                        if email_el:
                            print(f'  Found email field with selector: {sel}')
                            break
                    except:
                        continue
                
                if email_el:
                    await email_el.fill(CF_EMAIL)
                    # Find password field
                    pass_el = await page.wait_for_selector('input[type="password"]', timeout=3000)
                    await pass_el.fill(CF_PASS)
                    # Find submit button
                    submit_el = await page.wait_for_selector('button[type="submit"]', timeout=3000)
                    await submit_el.click()
                    print('  Login submitted, waiting...')
                    await asyncio.sleep(5)
                    print(f'  After login URL: {page.url[:100]}')
                    await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw_step2.png')
                else:
                    print('  Could not find email field')
                    await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw_no_field.png')
            except Exception as e:
                print(f'  Login error: {e}')
                await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw_error.png')
        
        # Check for 2FA
        url_after = page.url.lower()
        if any(x in url_after for x in ['2fa', 'totp', 'verification', 'challenge', 'mfa']):
            print('[!] 2FA/Verification required')
            print(f'  URL: {url_after[:100]}')
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw_2fa.png')
            await browser.close()
            return False
        
        print('[4/4] Trying to navigate to DNS...')
        try:
            await page.goto('https://dash.cloudflare.com/', timeout=30000, wait_until='domcontentloaded')
            await asyncio.sleep(3)
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw_dashboard.png')
            print(f'  Dashboard URL: {page.url[:100]}')
        except Exception as e:
            print(f'  Dashboard navigation error: {e}')
        
        await asyncio.sleep(2)
        await browser.close()
        return True

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
