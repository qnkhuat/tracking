from database import conn

CREATE_MIGRATION_TABLE_IF_NEEDED = """
CREATE TABLE IF NOT EXISTS migration (
  name text NOT NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP);
"""

conn.execute(CREATE_MIGRATION_TABLE_IF_NEEDED)







create_data_table = {
    "name": "create_data_table",
    "sql": """
    CREATE TABLE data (
    name TEXT NOT NULL,
    value REAL,
    timestamp datetime NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP)
    """
    }






## ------------------------------------- Execute migrations ------------------------------------- ##
migrations = [
    create_data_table,
    ]


for migration in migrations:
  is_migration_exists = conn.execute("select count(*) from migration where name = ?", [migration["name"]]).fetchone()[0]
  if is_migration_exists == 0:
    continue
  else:
    conn.execute(migration["sql"])

