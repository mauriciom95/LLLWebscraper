# import requests
import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup

URL = 'https://shop.lululemon.com/c/sale/_/'
driver = webdriver.Chrome(executable_path=r"/Applications/Google Chrome.app")
driver.get(URL)
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

response = driver.page_source;
# print(response.text)


## Extract the Items under WMTM

soup = BeautifulSoup(response.content, 'html.parser')

results = soup.find(id='product-list')
# print(results.prettify())

product_elems = results.find_all('div', class_='product-tile')

count = 0;

for product_elem in product_elems:
    inner_elem = product_elem.find('a',{'link product-tile__image-link'})
    # print (product_elem.prettify())
    json_details = json.loads(inner_elem['data-lulu-attributes'])
    # Seems that the json parser takes care of inner json fields.
    itemName = json_details['product']['name']

    cleanedName = itemName.replace('%20', ' ')
    print(cleanedName)
    # print(product_elem.find(])
    print('\n\n\n')
    count += 1;
    # print()

print(count);
# TODO: Need to step through and load the rest of the site to get the full list.
# TODO: Need to figure out how to retrieve the correct URL for men's WMTM,
# which may change over the weeks?
