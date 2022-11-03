from database import connection, DB

def create_migration_table_if_needed():
  sql = """
  CREATE TABLE IF NOT EXISTS migration (
    name text NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP);
  """

  return DB.execute(sql)

def save_migration_sql(name):
  return ["INSERT INTO migration values (?);", [name]]

def _run_migrations(migrations):
  print("Start migration")
  create_migration_table_if_needed()

  for migration in migrations:
    migration_name = migration['name']
    is_migration_exists = DB.execute("SELECT count(*) FROM migration WHERE name = ?;",
                                       [migration_name]).fetchone()[0]
    if is_migration_exists == 0:
      print(f"Running migration: {migration_name}")
      with connection() as conn:
        if conn.execute(migration["sql"]).fetchone() is None:
          conn.execute("INSERT INTO migration (name) values (?);",
                              [migration_name]).fetchall()
    else:
      print(f"Skip migration {migration_name}")

  print("Migrated successfully!")

## ------------------------------------- Migrations definition ------------------------------------- ##

create_data_table = {
    "name": "create_data_table",
    "sql" : """
    CREATE TABLE data (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    value REAL,
    settings TEXT,
    timestamp datetime NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP)
    """}

create_task_history_table = {
    "name": "create_task_history_table",
    "sql" : """
    CREATE TABLE task_history (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    start_time datetime NOT NULL,
    end_time datetime,
    duration INTEGER,
    status TEXT NOT NULL,
    error TEXT);
    """}

migrations = [
    create_data_table,
    create_task_history_table,
    ]

# run migrations by default
run_migrations = lambda : _run_migrations(migrations)

if __name__ == "__main__":
  run_migrations()
