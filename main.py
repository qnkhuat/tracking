from tracking import database as db
from migrations import run_migrations

def main ():
  run_migrations()


if __name__ == "__main__":
  main()

