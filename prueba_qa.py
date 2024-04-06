from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

#Create a driver

options = Options()
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.amazon.es")

search_box = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))
)

search_box.send_keys("Alexa")
time.sleep(2)
search_btn = driver.find_element(By.XPATH, "//input[@id='nav-search-submit-button']")

search_btn.click()

pagination_bar = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//span[@aria-label='pagination']"))
)

second_page_btn = pagination_bar.find_element(By.XPATH, ".//a[normalize-space()='2']")

second_page_btn.click()

third_item = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@data-cel-widget='search_result_3']"))
)

third_item_name = third_item.find_element(By.XPATH, ".//h2").text
print(third_item_name)
time.sleep(10)


