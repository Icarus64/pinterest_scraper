import os
import asyncio
import json
from datetime import datetime
from pyppeteer import launch
from bs4 import BeautifulSoup

async def main():
    user_input = input("Enter your search query: ")
    scroll_input = int(input("How many times do you want the page to scroll down? "))
    browser = await launch()
    page = await browser.newPage()
    
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    )
    q = user_input.replace(" ", "%20")
    url = f"https://www.pinterest.com/search/pins/?q={q}&rs=typed"
    await page.goto(url)

    try:
        for x in range(1, scroll_input+1):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            print(f"scroll no. {x} finished \nGoing to sleep for 5 secs")
            await asyncio.sleep(5)

        # await asyncio.sleep(20)
            
    except Exception as e:
        print("Error occured while scrolling")
        print(e)
        print('------------------------------------')
    
    
    try:
        await page.waitForSelector('div[data-test-id="masonry-container"]')
        div_content = await page.querySelectorEval('div[data-test-id="masonry-container"]', 'el => el.outerHTML')

        extracts = extractor(div_content)
        print(f'{len(extracts)} number of pins found in this scraping...')
        results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            'payload': extracts,
            'count': len(extracts)
        }

        os.makedirs('output', exist_ok=True)

        with open(f'output/{user_input.replace(" ", "_")}_data.json', 'w') as json_file:
            json.dump(results, json_file, indent=4)

        print(f"Data saved to {user_input}_data.json")

        
    except Exception as e:
        print("div couldn't be found")
        print(e)
        print('--------------------')
    
    await browser.close()

def extractor(content: str) -> dict:
    soup = BeautifulSoup(content, 'html.parser')

    try:
        # Find div elements with attribute 'data-test-id' and value 'deeplink-wrapper'
        deeplink_wrappers = soup.select('div[data-test-id="deeplink-wrapper"]')
        
        extracted_data = []
        for wrapper in deeplink_wrappers:
            a_tag = wrapper.find('a')
            img_tag = wrapper.find('img')
            
            item_link = 'https://www.pinterest.com' + a_tag['href'] if a_tag and 'href' in a_tag.attrs else ''
            item_label = a_tag['aria-label'] if a_tag and 'aria-label' in a_tag.attrs else ''
            img_link = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''
            
            extracted_data.append({
                'pin_link': item_link,
                'pin_label': item_label,
                'img_link': img_link
            })

        return extracted_data

    except Exception as e:
        print("Content found but couldn't count")
        print(e)
        print('--------------------')

asyncio.get_event_loop().run_until_complete(main())
