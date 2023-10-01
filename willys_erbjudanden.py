from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options
import time

def scroll_down():
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height

def extract_product(element: WebElement):
    name = element.find_element(By.XPATH, './/div[contains(@itemprop, "name")]').text
    brand = element.find_element(By.XPATH, './/span[contains(@itemprop, "brand")]').text
    price = element.find_element(By.XPATH, './/span[contains(@class, "sc-9270b5eb-2 fVzqtS")]').text

    return (name, brand, float(price) + .90)

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

driver.get("https://www.willys.se/erbjudanden/butik")

sleep(3)
reject_all_cookies = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))
)
reject_all_cookies.click()

## Selects the physical store

search = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/main/section/div[2]/div[2]/div/div/div/input')
search.clear()
search.send_keys("Magistratvägen")


firstResult = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/main/section/div[2]/div[2]/div/div/div[2]/div/ul'))
)
firstResult.click()

## Clicks show more and scrolls to load all producs

showMore = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div[3]/main/section/div[2]/div[3]/div/div/div/div[4]/div/button'))
)
driver.execute_script("arguments[0].scrollIntoView();", showMore)
showMore.click()
scroll_down()

## Fetches all products

productDivs = driver.find_elements(By.XPATH, '//div[contains(@class, "sc-dfc0c17a-0 hmPfuu")]')

## Extracts all product data

products = [extract_product(prod) for prod in productDivs]

for prod in products:
    print(prod)


