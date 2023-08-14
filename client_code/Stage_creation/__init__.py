from ._anvil_designer import Stage_creationTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Stage_creation(Stage_creationTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        
        # Drop down codes stages
        list=[]
        list=app_tables.codes_stages.search()
        print (list)
        self.drop_down_code_stage.items = []
        for code in list:
            self.drop_down_code_stage.items.append(code['code'])
            print(code['code'])

        # Drop down codes lieux
        list2=[]
        list2=app_tables.lieux.search()
        self.drop_down_lieux.items = []
        for lieu in list2:
            self.drop_down_lieux.items.append(lieu)