from contextlib import contextmanager
import sqlite3

DB = sqlite3.connect("test.db")

def add_data(conn, name, value, timestamp):
  sql = """INSERT INTO data
  (name, value, timestamp)
  VALUES
  (?, ?, ?)
  """
  params = [name, value, timestamp]
  return conn.execute(sql, params)

@contextmanager
def connection():
  """
  Connection context manager that conviently rollback if bad things happen, otherwise commits the result.

  with connection() as conn:
    conn.execute("insert into data values ('name')")
  """
  try:
    yield DB
  except Exception:
    DB.rollback()
  else:
    DB.commit()
