import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import re
import time

modele = input()
browser = webdriver.Chrome()
browser.get("https://www.bestbuy.com/?intl=nosplash")
search = browser.find_element(By.ID, 'gh-search-input').send_keys(f"{modele} 5g")
submit = browser.find_element(By.CLASS_NAME, 'header-search-button').click()
time.sleep(2)
try:
    main_results = browser.find_element(By.ID, 'main-results')
    sku_items = main_results.find_elements(By.CLASS_NAME, 'sku-item')
    first_sku_item = sku_items[0]
    click = first_sku_item.find_element(By.CLASS_NAME, 'product-image').click()
except NoSuchElementException:
    print("No search results found for the provided model.")
    browser.quit()
    exit()

def extract_text(element):
    try:
        return element.text
    except NoSuchElementException:
        return None

def extract_numeric(text):
    numeric = re.search(r'(\d+\.\d+|\d+)', text)
    return numeric.group(1) if numeric else None

inches_element = browser.find_element(By.CLASS_NAME, 'description')
inches_text = extract_text(inches_element)
inches = extract_numeric(inches_text)

Mobile_Details = browser.find_element(By.ID, 'quick-assessment-parent')
rate = extract_text(Mobile_Details.find_element(By.CLASS_NAME, 'ugc-c-review-average.font-weight-medium.order-1'))

try:
    price = browser.find_element(By.CLASS_NAME, 'priceView-hero-price.priceView-customer-price')
    price_span = extract_text(price.find_element(By.CSS_SELECTOR, 'span[aria-hidden="true"]'))
except NoSuchElementException:
    price_span = None

specifications = browser.find_element(By.CLASS_NAME, 'shop-specifications')
zebra_row = specifications.find_elements(By.CLASS_NAME, 'zebra-row')
front_camera_text = extract_text(zebra_row[1])
front_camera_resolution = extract_numeric(front_camera_text)

try:
    show_full_space = browser.find_element(By.CLASS_NAME, 'mb-600')
    button = show_full_space.find_element(By.CLASS_NAME, 'c-button.c-button-outline.c-button-md.show-full-specs-btn.col-xs-6').click()
    specifications_list = browser.find_element(By.CLASS_NAME, 'drawer.large')
    overflow = specifications_list.find_element(By.CLASS_NAME, 'overflow-scroll-wrapper')
    zebra_stripe_list = overflow.find_element(By.CLASS_NAME, 'zebra-stripe-list')
    Category = extract_text(browser.find_element(By.XPATH, '//*[@id="pdp-drawer-overlay-backdrop"]/div/div/div[4]/ul[2]/li/div[2]/div[2]'))
except NoSuchElementException:
    Category = None

try:
    processor_element = browser.find_element(By.XPATH, '//*[@id="pdp-drawer-overlay-backdrop"]/div/div/div[4]/ul[10]/li/div[3]/div[2]')
    processor_text = extract_text(processor_element)
    processor_speed = extract_numeric(processor_text)
except NoSuchElementException:
    processor_speed = None

try:
    RAM_element = browser.find_element(By.XPATH, '//*[@id="pdp-drawer-overlay-backdrop"]/div/div/div[4]/ul[10]/li/div[4]/div[2]')
    RAM_text = extract_text(RAM_element)
    RAM = extract_numeric(RAM_text)
except NoSuchElementException:
    RAM = None

try:
    battery_element = browser.find_element(By.XPATH, '//*[@id="pdp-drawer-overlay-backdrop"]/div/div/div[4]/ul[7]/li/div[1]/div[2]')
    battery_text = extract_text(battery_element)
    battery = extract_numeric(battery_text)
except NoSuchElementException:
    battery = None

try:
    reselution_element = browser.find_element(By.XPATH, '//*[@id="pdp-drawer-overlay-backdrop"]/div/div/div[4]/ul[3]/li/div[2]/div[2]')
    reselution_text = extract_text(reselution_element)
    reselution_width, reselution_height = map(int, reselution_text.split(' x '))
except (NoSuchElementException, ValueError):
    reselution_width = None
    reselution_height = None

try:
    main_rear_camera_resolution_element = browser.find_element(By.XPATH, '//*[@id="pdp-drawer-overlay-backdrop"]/div/div/div[4]/ul[1]/li/div[3]/div[2]')
    main_rear_camera_resolution_text = extract_text(main_rear_camera_resolution_element)
    main_rear_camera_resolution = extract_numeric(main_rear_camera_resolution_text)
except NoSuchElementException:
    main_rear_camera_resolution = None

try:
    framerate_element = browser.find_element(By.XPATH, '//*[@id="pdp-drawer-overlay-backdrop"]/div/div/div[4]/ul[3]/li/div[6]/div[2]')
    framerate_text = extract_text(framerate_element)
    framerate = extract_numeric(framerate_text)
except NoSuchElementException:
    framerate = None

# Create DataFrame
data = {
    "rate": [rate],
    "processor_speed": [processor_speed],
    "inches": [inches],
    "front_camera_resolution": [front_camera_resolution],
    "Category": [Category],
    "RAM": [RAM],
    "battery": [battery],
    "reselution_width": [reselution_width],
    "reselution_height": [reselution_height],
    "framerate": [framerate],
    "main_rear_camera_resolution": [main_rear_camera_resolution],
    # Add other keys and values
}

df = pd.DataFrame(data)
print(df)

browser.close()
