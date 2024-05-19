from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import json

options = ChromeOptions()
# options.set_capability('sessionName', 'Flipkart Selenium test')
driver = webdriver.Chrome(options=options)

def extract_results(driver):
    time.sleep(2)
    product_elements = driver.find_elements(By.XPATH, "//a[@class='CGtC98']")
    product_names = driver.find_elements(By.XPATH, "//div[@class='KzDlHZ']")
    product_prices = driver.find_elements(By.XPATH, "//div[@class='Nx9bqj _4b5DiR']")

    results = []
    for name, price, element in zip(product_names, product_prices, product_elements):
        product_info = {
            "Product Name": name.text,
            "Display Price": price.text,
            "Product Link": element.get_attribute("href")
        }
        results.append(product_info)

    return results


try:
    driver.get("https://www.flipkart.com")
    try:
        close_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'✕')]"))
        )
        close_btn.click()
    except Exception as e:
        pass
    try:
        search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Search for Products, Brands and More')]"))).click()
        search_box=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//input[contains(@type,'search')]")))
    except:
        search_box=driver.find_element(By.NAME,"q")
    # search_box=driver.find_element(By.NAME, "q")
    # search_box = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME, "q")))
    # search_box.click()
    search_box.send_keys("Samsung Galaxy S10")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    
    mobiles_category = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Mobiles')]"))
    )
    mobiles_category.click()
    time.sleep(2)
    
    brand_filter = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'SAMSUNG')]"))
    )
    brand_filter.click()
    time.sleep(2)
    
    flipkart_assured_filter = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//img[contains(@src, 'fa_62673a.png')]"))
    )
    flipkart_assured_filter.click()
    time.sleep(2)

    sort_dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Price -- High to Low')]"))
    )
    sort_dropdown.click()
    time.sleep(2)
    
    results = extract_results(driver)
    print(results)
    # for result in results:
    #         print(result)
    if len(results) != 0:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Requested Data Found"}}')
    else:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Requested data not found"}}')
    
except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')

except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
finally:
    # Stop the driver
    driver.quit()