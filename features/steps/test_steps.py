from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
import requests
from behave import given, when, then
import subprocess
import os

from dotenv import load_dotenv
load_dotenv()

@given('I have created a Chrome driver instance')
def step_impl(context):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument('--lang=en')
    options.add_argument("--disable-extensions")  
    options.add_argument("--disable-popup-blocking")  
    options.add_argument("--disable-default-apps")  
    options.add_argument("--disable-infobars")  
    options.add_argument("--disable-web-security")  
    options.add_argument(  
        "--disable-features=IsolateOrigins,site-per-process"  
    )  
    options.add_argument(  
        "--enable-features=NetworkService,NetworkServiceInProcess"  
    )  
    options.add_argument("--profile-directory=Default")  
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)
    
@when('I connect to a VPN in Australia')
def step_impl(context):
    connect_command = "nordvpn connect -c -n \"Australia #750\""
    subprocess.run(connect_command, shell=True, capture_output=True, text=True)
    
@then('I should verify that my VPN connection is valid')
def step_impl(context):
    australian_location = False
    response = requests.get('https://ipinfo.io')
    data = response.json()
    print(f"Current location: {data['country']}, {data['region']}, {data['city']}")
    if data['country'] == "AU":
        australian_location = True
    assert australian_location is True, "You do not have a valid Australian VPN"
    
    
    
@given('I have a valid VPN connection to Australia')
def step_impl(context):
    australian_location = False
    response = requests.get('https://ipinfo.io')
    data = response.json()
    print(f"Current location: {data['country']}, {data['region']}, {data['city']}")
    if data['country'] == "AU":
        australian_location = True
    assert australian_location is True, "You do not have a valid Australian VPN"
    
@given('I have created a Chrome driver instance')
def step_impl(context):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument('--lang=en')
    options.add_argument("--disable-extensions")  
    options.add_argument("--disable-popup-blocking")  
    options.add_argument("--disable-default-apps")  
    options.add_argument("--disable-infobars")  
    options.add_argument("--disable-web-security")  
    options.add_argument(  
        "--disable-features=IsolateOrigins,site-per-process"  
    )  
    options.add_argument(  
        "--enable-features=NetworkService,NetworkServiceInProcess"  
    )  
    options.add_argument("--profile-directory=Default")  
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)

@when('I navigate to the Airtasker landing page')
def step_impl(context):
    context.driver.get("https://www.airtasker.com")
    
@when('I add the athentication cookies')
def step_impl(context):
    cookie_value = os.getenv("AT_SID")
    context.driver.add_cookie({
            "name": "at_sid",
            "value": cookie_value,
            "domain": ".airtasker.com",
        })
    context.driver.refresh()
    
@then('I should see the Airtasker tasks page loaded')
def step_impl(context):
    context.driver.get("https://www.airtasker.com/tasks")
    accept_btn = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Accept all']"))
            )    
    try:
        accept_btn.click()
        print("Cookies were accepted...")
    except:
        pass
    task_card = WebDriverWait(context.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='group']"))
    )
    assert task_card is not None, "Error in loading the tasks page..."
    
@given('I am on the Airtasker tasks page')
def step_impl(context):
    context.driver.get("https://www.airtasker.com/tasks")
    
@when('I filter to show only remote tasks')
def step_impl(context):
    location_filter_btn = context.driver.find_element(By.XPATH, "//button[@data-ui-test='location-menu']")
    if location_filter_btn.text != "Remote tasks only":
        location_filter_btn.click()
        remote_option = WebDriverWait(context.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Remotely']"))
        )
        remote_option.click()
        apply_btn = context.driver.find_element(By.XPATH, "//button[normalize-space()='Apply']")
        apply_btn.click()
        time.sleep(2)
        
@then('only remote tasks should be shown in the results')
def step_impl(context):
    assert context.driver.find_element(By.XPATH, "//button[@data-ui-test='location-menu']").text == 'Remote tasks only', 'Error in filtering only remote tasks'
    

