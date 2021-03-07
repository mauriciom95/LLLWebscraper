import requests
import json
import time
import csv
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from urllib.parse import unquote

URL = 'https://shop.lululemon.com/c/sale/_/'

## Scroll through to the bottom of the page.
DRIVER_PATH = '/Users/i868119/Personal/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(URL)
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

# while True:

while True:

    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    python_button = driver.find_elements_by_xpath('//*[@id="main-content"]/div/section/div/div[2]/div/button')
    #scroll height is total height of the page, growing by the screen height each time.
    #Screen height is height of the screen.

    if python_button:
        thisElement = python_button[0]
        # print(thisElement)

        actions = ActionChains(driver)
        actions.move_to_element(thisElement).click().perform()
        # thisElement.click()
        time.sleep(scroll_pause_time)
        ##Looks like the button has to be on screen before we can actually "CLICK" on it.
        # driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height+200, i=i-1))

        continue


    if (screen_height) * i > scroll_height: # We've iterated past the end of the page.
        break



## Extract the Items under WMTM

soup = BeautifulSoup(driver.page_source, 'html.parser')

results = soup.find(id='product-list')
# print(results.prettify())

product_elems = results.find_all('div', class_='product-tile')

count = 0

items = []

## Retrieve the names
for product_elem in product_elems:
    inner_elem = product_elem.find('a',{'link product-tile__image-link'})
    # print (product_elem.prettify())
    json_details = json.loads(inner_elem['data-lulu-attributes'])
    # Seems that the json parser takes care of inner json fields.
    itemName = json_details['product']['name']

    cleanedName = unquote(itemName)
    print(cleanedName)
    items.append(cleanedName)
    count += 1;

## Write to csv file. read the previous file.

with open('WMTM_items.csv', mode='w') as WMTM_items:
    item_writer = csv.writer(WMTM_items, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in items:
        item_writer.writerow([item])

print(count);


# def
# TODO: Need to step through and load the rest of the site to get the full list.
# TODO: Need to figure out how to retrieve the correct URL for men's WMTM,
# which may change over the weeks?
