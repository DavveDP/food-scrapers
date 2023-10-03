from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException
import sys;
import time

def scroll_down():
    """A method for scrolling the page."""
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        print('Scrolling...')
    
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            print('No more content to load, stopped scrolling')
            break

        last_height = new_height

def extract_product(element: WebElement):
    name = element.find_element(By.XPATH, './/div[contains(@itemprop, "name")]').text
    brand = element.find_element(By.XPATH, './/span[contains(@itemprop, "brand")]').text
    price = element.find_element(By.XPATH, './/span[contains(@class, "sc-9270b5eb-2 fVzqtS")]').text

    return (name, brand, float(price) + .90)

if __name__ == "__main__":

    if (len(sys.argv) != 2):
        print('Missing search argument for physical store')
        quit()

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options, service=FirefoxService(executable_path='/snap/bin/firefox.geckodriver'))

    driver.get("https://www.willys.se/erbjudanden/butik")

    print('Waiting 3 seconds for page to load...')
    sleep(3)

    try:
        reject_all_cookies = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))
        )
        reject_all_cookies.click()
    except TimeoutException:
        pass

    ## Selects the physical store

    searchArg = sys.argv[1]

    print('Selecting physical store from first match using string: {0}'.format(searchArg))

    search = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/main/section/div[2]/div[2]/div/div/div/input')
    search.clear()
    search.send_keys(searchArg)


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

    print('Fetching products')

    productDivs = driver.find_elements(By.XPATH, '//div[contains(@class, "sc-dfc0c17a-0 hmPfuu")]')

    ## Extracts all product data

    products = [extract_product(prod) for prod in productDivs]

    filePath = ''

    try:
        filePath = sys.argv[2]
    except IndexError:
        filePath = 'products.csv'
        print('No output file specified, writing to products.csv')
        

    with open(filePath, 'w') as file:
        for prod in products:
            file.write('{0}, {1}, {2}\n'.format(*prod).capitalize())

    driver.quit()

