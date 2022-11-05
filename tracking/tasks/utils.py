from tracking.database import DB

def task_ran_count(name):
  """Return how many time a task with given name has been ran.."""
  task_count = DB.execute("SELECT count(*) from task_history where name = ? and status = 'done'", [name]).fetchone()[0]
  return task_count
