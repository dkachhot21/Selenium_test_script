from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

def setup_driver(browser):
    print(f"Setting up {browser} driver.")
    if browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "msedge":
        driver = webdriver.Edge()
    else:
        raise ValueError("Unsupported browser!")
    # driver.maximize_window()
    return driver

def search_product(driver, product_name):
    driver.get("https://www.flipkart.com")
    
    try:
        close_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
        )
        close_btn.click()
    except Exception as e:
        pass
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)

def apply_filters(driver):
    mobiles_category = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Mobiles')]"))
    )
    mobiles_category.click()
    time.sleep(2)
    
    brand_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'SAMSUNG')]"))
    )
    brand_filter.click()
    time.sleep(2)
    
    flipkart_assured_filter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'fa_62673a.png')]"))
    )
    flipkart_assured_filter.click()
    time.sleep(2)

    sort_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Price -- High to Low')]"))
    )
    sort_dropdown.click()
    time.sleep(2)

def extract_results(driver):
    time.sleep(5)
    
    product_elements = driver.find_elements(By.XPATH, "//a[@class='CGtC98']")
    product_names = driver.find_elements(By.XPATH, "//div[@class='KzDlHZ']")
    product_prices = driver.find_elements(By.XPATH, "//div[@class='Nx9bqj _4b5DiR']")

    results = []
    for name, price, element in zip(product_names, product_prices, product_elements):
        product_info = {
            "Product Name": name.text,
            "Display Price": price.text.encode("utf-8", "replace"),
            "Product Link": element.get_attribute("href")
        }
        results.append(product_info)

    return results

@pytest.mark.parametrize("browser", ["chrome", "firefox", "msedge"])
def test_flipkart_search(browser):
    # sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    print(f"Running test on {browser}")
    driver = setup_driver(browser)
    try:
        search_product(driver, "Samsung Galaxy S10")
        time.sleep(2)
        apply_filters(driver)
        results = extract_results(driver)
        for result in results:
            print(result)
    finally:
        driver.quit()

if __name__ == "__main__":
    pytest.main()
