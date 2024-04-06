#IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
import pandas as pd
import random
import unicodedata
from dotenv import load_dotenv
import os
import subprocess



def main():
    bot = Bot()
    bot.connect_to_australia_vpn()
    bot.load_cookies()
    bot.scrap_tasks()
    # bot = Bot()
    # bot.load_cookies()
    # bot.scrap_tasks()
    # print("DONE....")


class Bot:
    def __init__(self):
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
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def connect_to_australia_vpn(self):
        connect_command = "nordvpn connect -c -n \"Australia #750\""
        result = subprocess.run(connect_command, shell=True, capture_output=True, text=True)
        print("Connected to Australia VPN...")
        time.sleep(3)
        return
      
    def get_cookie_value(self):
        load_dotenv()
        cookie_value = os.getenv("AT_SID")
        return cookie_value
    
    def load_cookies(self):
        self.connect_to_australia_vpn()
        time.sleep(4)
        self.driver.get("https://www.airtasker.com/")
        
        self.driver.add_cookie({
            "name": "at_sid",
            "value": self.get_cookie_value(),
            "domain": ".airtasker.com",
        })
        self.driver.get("https://www.airtasker.com/tasks")
        
        accept_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Accept all']"))
        )
        
        try:
            accept_btn.click()
            print("Cookies were accepted...")
        except:
            pass
        
        time.sleep(random.randint(1,3))
        task_card = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='group']"))
        )
        
        
        time.sleep(10)
        
    def filter_only_remote_tasks(self):
        location_filter_btn = self.driver.find_element(By.XPATH, "//button[@data-ui-test='location-menu']")
        if location_filter_btn.text != "Remote tasks only":
            location_filter_btn.click()
            remote_option = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Remotely']"))
            )
            remote_option.click()
            apply_btn = self.driver.find_element(By.XPATH, "//button[normalize-space()='Apply']")
            apply_btn.click()
            time.sleep(2)
            
        
    def scrap_tasks(self):
        new_tasks = []
        df = pd.read_excel("new_df.xlsx", index_col=0)
        tasks_container = self.driver.find_element(By.XPATH, "//div[@class='group']")
        tasks = tasks_container.find_elements(By.XPATH, ".//a[@data-ui-test='task-list-item']")
        for task in tasks:
            link = task.get_attribute("href")
            if link in df["Link"]:
                continue
            else:
                task.click()
                time.sleep(1)
                title = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//h1"))
                )
                title = title.text.strip()
                price = self.driver.find_element(By.XPATH, "//div[@class='task-price']").text.replace("$", "").replace(",", "").strip()
                username = self.driver.find_element(By.XPATH, "//span//a[@data-ui-test='user-name']").text.split(" ")[0]
                new_tasks.append([link, title, price, username])
                time.sleep((random.random()+1)*2)
                
        new_df = pd.DataFrame(new_tasks, columns = ["Link", "Title", "Price", "Username"])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel("new_df.xlsx")

    def apply_to_task(self, task_link, desired_price, description):
        self.driver.get(task_link)
        offer_btn = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Make an offer']"))
        )
        offer_btn.click()
        price_input = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-ui-test='currency-prefix-input']"))
        )
        price_input.clear()
        price_input.send_keys(desired_price)
        next_btn = self.driver.find_element(By.XPATH, "//button[text()='Next']")
        time.sleep(4)
        next_btn.click()
        description_input = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@data-ui-test='comment-input']"))
        )
        description_input.clear()
        description_input.send_keys(description)
        next_btn = self.driver.find_element(By.XPATH, "//button[text()='Next']")
        next_btn.click()
        submit_btn = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Submit Offer']"))
        )
        submit_btn.click()
        
        
        
        
        
        
        
        
        
        
def categorize_task(task_name):
    categories = []
    nfkd_form = unicodedata.normalize('NFKD', task_name)
    task_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
    if ("resume" in task_name):
        categories.append("resume")
    if ("cv" in task_name or "cover letter" in task_name):
        categories.append("cv")
    if ("linkedin" in task_name or "linked in" in task_name):
        categories.append("linkedin")
    return categories
          
if __name__  == "__main__":
    main()