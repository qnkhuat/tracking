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

def insert_sql(table, data):
  """
  Generate a sql to insert a data as a dict.
  insert_sql('task_history', {'name': 'a task', 'status': 'done'})

  ;; => ['INSERT INTO task_history (name, status) VALUES (?, ?) ', ['a task', 'done']]
  """
  columns = data.keys()
  params = list(data.values())
  sql = f"""INSERT INTO {table}
  ({', '.join(columns)})
  VALUES
  ({', '.join(['?']*len(columns))})
  """
  return [sql, params]

def update_sql(table, changes, where = None):
  """
  Generate a sql to update data.
  update("task_history", {"data": "new_data", "sup": "new_stuff"}, "id=1")
  ;; => ['UPDATE task_history SET data = ?, sup = ?  WHERE id=1', ['new_data', 'new_stuff']]
  """
  columns = changes.keys()
  set_columns = [f"{col} = ?" for col in columns]
  params = list(changes.values())
  sql = f"""UPDATE {table}
  SET {', '.join(set_columns)}
  """
  if where:
    sql += f" WHERE {where}"
  return [sql, params]

@contextmanager
def connection():
  """
  Connection context manager that conviently rollback if bad things happen, otherwise commits the result.

  with connection() as conn:
    conn.execute("insert into data values ('name')")
  """
  try:
    yield DB
  except Exception as e:
    print("Error during connection: ", e)
    DB.rollback()
    # reraise it again
    raise e
  else:
    DB.commit()

