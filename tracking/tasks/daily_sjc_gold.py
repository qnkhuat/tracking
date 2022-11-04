import json
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tracking.tasks.base import runner
from tracking import database as db

@runner("daily_sjc_gold")
def run(**kwargs):
  url = "https://sjc.com.vn/giavang/"

  chrome_options = Options()
  chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/span")))
  except TimeoutException:
    raise Exception("FAILED TO FIND ELEMENT")

  with db.connection() as conn:
    value = int(element.text.replace(",", ""))
    data ={"name": "sjc_gold_buy",
           "value": value,
           "type": "gold",
           "settings": json.dumps({"currency": "VND"}),
           "timestamp": datetime.now()}
    conn.execute(*db.insert_sql("data", data))
run()
