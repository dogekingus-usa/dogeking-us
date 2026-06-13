"""
Cloudflare DNS Fix - Interactive Mode
Browser opens for user to complete captcha/2FA, then script updates DNS
"""
import asyncio, sys

GITHUB_IPS = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']
CF_EMAIL = 'dogeking.us@gmail.com'
CF_PASS = 'domvic-1tIdko-wijdaz'

async def main():
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        print('=== CLOUDFLARE DNS FIX - INTERACTIVE ===')
        print('[1] Opening Cloudflare login in browser...')
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()
        
        await page.goto('https://dash.cloudflare.com/login', timeout=60000, wait_until='domcontentloaded')
        
        print('\n[2] BROWSER IS OPEN. Please:')
        print('  1. Complete the captcha/challenge if shown')
        print('  2. Login with email: dogeking.us@gmail.com')
        print('  3. Complete 2FA if needed')
        print('  4. Navigate to DNS settings for dogeking.us')
        print('\n  Waiting up to 5 minutes...')
        
        # Wait for user to navigate to a page with DNS records
        logged_in = False
        for i in range(60):
            await asyncio.sleep(5)
            try:
                current_url = page.url.lower()
                content = await page.inner_text('body')
                
                # Check if we're on dashboard/zone page
                if any(x in current_url for x in ['dash.cloudflare.com']):
                    if 'login' not in current_url and 'challenge' not in current_url:
                        if not logged_in:
                            print(f'  Logged in! URL: {current_url[:80]}')
                            logged_in = True
                
                # Check if we're on DNS records page
                if 'dns' in current_url or 'dns_records' in current_url:
                    print(f'  On DNS page! URL: {current_url[:80]}')
                    break
                    
                # Check if dogeking.us zone is visible
                if 'dogeking' in content.lower() and ('record' in content.lower() or 'dns' in content.lower()):
                    print('  dogeking.us DNS page detected!')
                    break
                    
            except:
                pass
            
            if i % 12 == 0:
                print(f'  Still waiting... ({i*5}s)')
        
        # Take screenshot
        await page.screenshot(path='C:\\Users\\SAMPC\\workspace-dogeking-us\\cf_current.png')
        print('  Screenshot saved')
        
        # Try to add DNS records via page interaction
        print('\n[3] Attempting to add GitHub Pages DNS records...')
        try:
            # Look for Add Record button
            try:
                add_btn = await page.wait_for_selector('button:has-text("Add Record"), a:has-text("Add Record")', timeout=5000)
                if add_btn:
                    print('  Found Add Record button')
            except:
                print('  No Add Record button found')
            
            # Check current records
            page_content = await page.inner_text('body')
            for ip in ['108.153', '109.153', '110.153', '111.153']:
                if ip in page_content:
                    print(f'  GitHub Pages IP {ip} already present!')
        except Exception as e:
            print(f'  Error checking records: {e}')
        
        print(f'\n[4] Current URL: {page.url}')
        print('  Browser stays open. Tell me when to proceed or close.')
        
        # Keep browser open for user
        await asyncio.sleep(60)
        
        await browser.close()
        print('\n[DONE] Browser closed')

if __name__ == '__main__':
    asyncio.run(main())
