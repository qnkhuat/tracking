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

def run_migrations(migrations):
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

## ------------------------------------- Migrations definition ------------------------------------- ##

create_data_table = {
    "name": "create_data_table",
    "sql": """
    CREATE TABLE data (
    name TEXT NOT NULL,
    value REAL,
    timestamp datetime NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP)
    """}

migrations = [
    create_data_table,
    ]

if __name__ == "__main__":
  run_migrations(migrations)
