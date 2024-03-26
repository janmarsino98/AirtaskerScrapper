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



def main():
    categorize_task("Create resumé and cv")
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
        
    def get_cookie_value(self):
        load_dotenv()
        cookie_value = os.getenv("AT_SID")
        return cookie_value
    
    def load_cookies(self):
        self.driver.get("https://www.airtasker.com/")
        self.driver.add_cookie({
            "name": "at_sid",
            "value": self.get_cookie_value(),
            "domain": ".airtasker.com",
        })
        self.driver.get("https://www.airtasker.com/tasks")
        time.sleep(5)
        task_card = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='group']"))
        )
        try:
            accept_btn = self.driver.find_element(By.XPATH, "//button[text()='Accept all']")
            accept_btn.click()
        except:
            pass
        
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

def categorize_task(task_name):
    categories = []
    nfkd_form = unicodedata.normalize('NFKD', task_name)
    task_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
    if ("resume" in task_name):
        categories.append("resume")
    if ("cv" in task_name | "cover letter" in task_name):
        categories.append("cv")
    if ("linkedin" in task_name):
        categories.append("linkedin")
          
if __name__  == "__main__":
    main()