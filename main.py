import time
import schedule

from tracking import database as db
from migrations import run_migrations

from tracking.tasks.daily_sjc_gold import daily_sjc_gold

def schedule_tasks():
  print("Scheduling tasks")
  schedule.every().day.at("00:00").do(daily_sjc_gold)

def main ():
  run_migrations()
  schedule_tasks()

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()

