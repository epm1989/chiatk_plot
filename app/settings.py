import os

working_dir = os.environ.get('working_dir')
concurrent_plots = int(os.environ.get('concurrent_plots', 1))
db_name = os.environ.get('db_name', 'db.sqlite3')
