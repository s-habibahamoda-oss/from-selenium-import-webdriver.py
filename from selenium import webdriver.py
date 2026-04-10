import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

url = 'https://www.amazon.eg/'
user_input = input('Enter a product: ')

def amazon(link):

    try:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)
    
        browser.get(link)
        time.sleep(3)

        search_bar = browser.find_element(By.ID, 'twotabsearchtextbox')
        search_bar.send_keys(user_input)
        search_button = browser.find_element(By.ID, 'nav-search-submit-button')
        search_button.click()
        time.sleep(5)

        scroll_pause = 0.5  
        screen_height = browser.execute_script("return window.innerHeight")  
        scrolls = 15  
        
        for i in range(scrolls):
            browser.execute_script(f"window.scrollBy(0, {screen_height});")
            time.sleep(scroll_pause) 

        products = browser.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        with open('amazon_products.csv', 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Rating', 'Link', 'Image'])

            for product in products:
                try:
                    name = product.find_element(By.TAG_NAME, 'h2').text
                    
                    try:
                        price = product.find_element(By.CLASS_NAME, 'a-price-whole').text
                    except:
                        price = "N/A"

                    try:
                        rating = product.find_element(By.CLASS_NAME, 'a-icon-alt').get_attribute('innerHTML')
                    except:
                        rating = "No rating"

                    link_item = product.find_element(By.CLASS_NAME, 'a-link-normal').get_attribute('href')
                    img = product.find_element(By.CLASS_NAME, 's-image').get_attribute('src')

                    writer.writerow([name, price, rating, link_item, img])
                    
                except:
                    continue
        
        print("Done! Data saved to amazon_products.csv")

    except Exception as e:
        print(f'something went wrong with amazon ==> {e}')
    finally:
        browser.quit()

amazon(url)