"""
Playwright v2 - Cloudflare DNS fix for GitHub Pages
"""
import asyncio, sys

GITHUB_IPS = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']
CF_EMAIL = 'dogeking.us@gmail.com'
CF_PASS = 'domvic-1tIdko-wijdaz'

async def main():
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        print('[1/5] Launching browser...')
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()
        
        print('[2/5] Going to Cloudflare dashboard...')
        await page.goto('https://dash.cloudflare.com', timeout=30000, wait_until='domcontentloaded')
        await asyncio.sleep(5)
        print('  URL:', page.url[:120])
        await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw2_step1.png')
        
        if 'login' in page.url.lower() or 'challenge' in page.url.lower():
            print('[3/5] On login/challenge page')
            try:
                email_el = await page.wait_for_selector('#email, input[name="email"], input[type="email"]', timeout=5000)
                if email_el:
                    await email_el.fill(CF_EMAIL)
                    pass_el = await page.wait_for_selector('#password, input[name="password"], input[type="password"]', timeout=3000)
                    await pass_el.fill(CF_PASS)
                    submit = await page.wait_for_selector('#sign_up_button, button[type="submit"], button:has-text("Sign in")', timeout=3000)
                    await submit.click()
                    print('  Login submitted')
                    await asyncio.sleep(8)
                    print('  After login:', page.url[:120])
                    await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw2_login.png')
                else:
                    print('  No email field found - challenge page')
            except Exception as e:
                print('  Login error:', str(e)[:100])
        else:
            print('[3/5] Already on dashboard')
        
        if any(x in page.url.lower() for x in ['2fa', 'totp', 'mfa', 'verification']):
            print('[!] 2FA required')
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw2_2fa.png')
            await browser.close()
            return '2FA'
        
        print('[4/5] Attempting DNS update...')
        try:
            # Try direct zone DNS page
            await page.goto('https://dash.cloudflare.com/?to=/:zone/dns', timeout=30000, wait_until='domcontentloaded')
            await asyncio.sleep(3)
            print('  DNS page:', page.url[:120])
            await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\pw2_dns.png')
            
            page_text = await page.inner_text('body')
            if 'dogeking' in page_text.lower():
                print('  dogeking.us found on page')
            else:
                print('  No dogeking.us on this page')
        except Exception as e:
            print('  DNS navigation error:', str(e)[:100])
        
        cookies = await context.cookies()
        cf_count = len([c for c in cookies if 'cloudflare' in c.get('domain', '')])
        print('  CF cookies found:', cf_count)
        
        await browser.close()
        return 'done'

if __name__ == '__main__':
    result = asyncio.run(main())
    print('Result:', result)
    sys.exit(0 if result == 'done' else 2)
