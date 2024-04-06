from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--lang=en")
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://Utest.com")
signup_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Become a uTester']"))
)

signup_btn.click()

first_name_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='firstName']"))
)

first_name_field.send_keys("Jan")

last_name_field = driver.find_element(By.XPATH, "//input[@id='lastName']")
last_name_field.send_keys("Marsino")

email_field = driver.find_element(By.XPATH, "//input[@id='email']")

email_field.send_keys("janmarsinopique98@gmail.com")

birth_month_field = driver.find_element(By.XPATH, "//select[@id='birthMonth']")
birth_month_field.click()
october_option = driver.find_element(By.XPATH, "//option[@label='October']")
october_option.click()
birth_day_field = driver.find_element(By.XPATH, "//select[@id='birthDay']")
birth_day_field.click()
sixteen_option = driver.find_element(By.XPATH, "//option[@label='16']")
sixteen_option.click()
birth_year_field = driver.find_element(By.XPATH, "//select[@id='birthYear']")
birth_year_field.click()
year_option = driver.find_element(By.XPATH, "//option[@label='1998']")
year_option.click()


print("The form is field so the script will proceed to the next page in 10 seconds...")

time.sleep(2)
next_btn = driver.find_element(By.XPATH, "//button[contains(normalize-space(), 'Next: Location')]")
next_btn.click()
time.sleep(3)
city = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='city']"))
)

zip_code = driver.find_element(By.XPATH, "//input[@id='zip']")
country = driver.find_element(By.XPATH, "//span[@aria-label='Select a country']")

city_group, zip_group, country_group = driver.find_elements(By.XPATH, "//div[@class='form-group']")



try:
    city_group.find_element(By.XPATH, ".//span[@class='check-mark']")
    print(f"The city was autodetected. The autodetected city by the website is {city.text.strip()}")
    
except:
    city.send_keys("La Seu d'Urgell")
    
try:
    zip_group.find_element(By.XPATH, ".//span[@class='check-mark']")
    print(f"The zip_code was autodetected. The autodetected zip_code by the website is {zip_code.text.strip()}")
    
except:
    zip_code.send_keys("25700")
try:
    country_group.find_element(By.XPATH, ".//span[@class='check-mark']")
    print(f"The country was autodetected. The autodetected country by the website is {country.text.strip()}")
    
except:
    country.click()
    country.send_keys("Spain")


time.sleep(10)

