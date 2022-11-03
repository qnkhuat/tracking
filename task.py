import json
from datetime import datetime
import traceback

from database import DB
#from src.logger import logger

# the collection name of task_history table
TASK_HISTORY = 'task_history'

def diff_time_in_microseconds(time1, time2):
  """
  Returns the difference between 2 time in microseconds.
  Use to compute duration of task.
  """
  # apply an abs to ensure the different is always positive
  return abs((time1 - time2).total_seconds() * 1000)

def create_task_history(task_name, task_details):
  task_info = {
      "name": task_name,
      "start_time": datetime.now(),
      "end_time": None,
      "duration": None,
      "status": "started",
      "details": json.dumps(task_details),
      "summary": None,
      "error": None
      }
  return task_info

def on_task_done(task_history, summary):
  now = datetime.now()
  update_task_history = {
      "summary": json.dumps(summary),
      "status": "done",
      "end_time": now,
      "duration": diff_time_in_microseconds(now, task_history.start_time)
      }
  print("TASK DONE", update_task_history)

def on_task_error(task_history, error):
  now = datetime.now()
  update_task_history = {
      "error": str(error),
      "status": "error",
      "end_time": now,
      "duration": diff_time_in_microseconds(now, task_history.start_time)
      }
  print("TASK ERROR", update_task_history)

def runner(task_name):
  def decorator(func):
    def wrapper(*args, **kwargs):
      task_details = kwargs.get("task_details", {})
      task_history = create_task_history(task_name, task_details)
      print(f"Task started {task_name} {task_history.id}")
      result = None
      try:
        # populate task_id to the task function
        kwargs["task_id"] = task_history.id
        result = func(*args, **kwargs)
      except Exception as e:
        print(f"Task error {task_name} {task_history.id} with error: {e}")
        print(traceback.format_exc())
        on_task_error(task_history, e)
      else:
        print(f"Task done {task_name} {task_history.id}: {result}")
        on_task_done(task_history, result)
      return result
    return wrapper
  return decorator
