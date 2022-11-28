import time
import schedule

from migrations import run_migrations

from tracking.tasks.utils import task_ran_count
from tracking.tasks import daily_sjc_gold, historical_sjc_gold

def schedule_tasks():
  print("Scheduling tasks")
  schedule.every().day.at("00:00").do(daily_sjc_gold.run)

def run_one_time_tasks():
  if task_ran_count(historical_sjc_gold.TASK_NAME) == 0:
    historical_sjc_gold.run()
  else:
    print(f"SKIP {historical_sjc_gold.TASK_NAME}")

def main ():
  run_migrations()
  run_one_time_tasks()
  schedule_tasks()

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()

