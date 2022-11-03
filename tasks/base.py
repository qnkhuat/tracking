from datetime import datetime
import traceback

import database
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

def create_task_history(task_name):
  task_info = {
      "name": task_name,
      "start_time": datetime.now(),
      "end_time": None,
      "duration": None,
      "status": "started",
      "error": None
      }
  with database.connection() as conn:
    cursor = conn.cursor()
    cursor.execute(*database.insert_sql("task_history", task_info)).fetchone()
    task_info['id'] = cursor.lastrowid

  assert task_info['id'], "should have task_id"
  return task_info

def on_task_done(task_history):
  now = datetime.now()
  update_task_history = {
      "status": "done",
      "end_time": now,
      "duration": diff_time_in_microseconds(now, task_history['start_time'])
      }
  with database.connection() as conn:
    conn.execute(*database.update_sql("task_history", update_task_history, f"id = {task_history['id']}"))

def on_task_error(task_history, error):
  now = datetime.now()
  update_task_history = {
      "error": str(error),
      "status": "error",
      "end_time": now,
      "duration": diff_time_in_microseconds(now, task_history['start_time'])
      }
  with database.connection() as conn:
    conn.execute(*database.update_sql("task_history", update_task_history, f"id = {task_history['id']}"))

def runner(task_name):
  def decorator(func):
    def wrapper(*args, **kwargs):
      task_history = create_task_history(task_name)
      task_id = task_history['id']
      print(f"Task started {task_name} {task_id}")
      result = None
      try:
        # populate task_id to the task function
        kwargs["task_id"] = task_id
        result = func(*args, **kwargs)
      except Exception as e:
        print(f"Task error {task_name} {task_id} with error: {e}")
        print(traceback.format_exc())
        on_task_error(task_history, e)
      else:
        print(f"Task done {task_name} {task_id}: {result}")
        on_task_done(task_history)
      return result
    return wrapper
  return decorator
