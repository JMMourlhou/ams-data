import anvil.stripe
import anvil.files
from anvil.files import data_files
import anvil.email

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def task_killer(task):
    task.kill()
    print("task killed")