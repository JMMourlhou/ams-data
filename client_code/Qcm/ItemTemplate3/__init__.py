from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global cpt  # compteur des lignes
cpt = 0

class ItemTemplate3(ItemTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        question = str(self.item["num"])+"-   "+self.item['question']
        self.text_area_1.text = question
        

    
    def text_area_1_show(self, **event_args):
        """This method is called when the text area is shown on the screen"""
        global cpt  # Cpt le nb de form imprimée
        cpt += 1

