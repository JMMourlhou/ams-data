from ._anvil_designer import Qcm_testTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Qcm_test(Qcm_testTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
         # lecture question 1
        question = app_tables.qcm.search()[0]
        print(question['question'])
        self.rich_text_1.content = question["question"]
        