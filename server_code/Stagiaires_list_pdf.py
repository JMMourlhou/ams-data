import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import anvil.pdf

@anvil.server.callable
def create_pdf():
  media_object = anvil.pdf.render_form('Visu_1_stage')
  return media_object