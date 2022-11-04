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
def daily_sjc_gold(**kwargs):
  url = "https://sjc.com.vn/giavang/"

  chrome_options = Options()
  chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  try:
    buy_price_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/span")))
    sell_price_el = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/table/tbody/tr[2]/td[3]/span")
  except TimeoutException:
    raise Exception("FAILED TO FIND ELEMENT")

  with db.connection() as conn:
    buy_price = int(buy_price_el.text.replace(",", ""))
    data = {"name": "sjc_gold_buy",
            "value": buy_price,
            "type": "gold",
            "settings": json.dumps({"currency": "VND", "unit": "1luong"}),
            "timestamp": datetime.now()}
    conn.execute(*db.insert_sql("data", data))

    sell_price = int(sell_price_el.text.replace(",", ""))
    data = {"name": "sjc_gold_sell",
            "value": sell_price,
            "type": "gold",
            "settings": json.dumps({"currency": "VND"}),
            "timestamp": datetime.now()}
    conn.execute(*db.insert_sql("data", data))
