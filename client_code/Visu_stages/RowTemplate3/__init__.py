from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Visu_stages
from anvil import open_form


class RowTemplate3(RowTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_1.text = self.item['numero']
        self.button_2.text = self.item['type']['code']                     # link key
        if self.item['date_debut'] != None:
            self.button_3.text = self.item['date_debut'].strftime("%d/%m/%Y")   # format date française avec fonction Python strftime
        

    # récupération par l'event:
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        num_stage = int(self.button_1.text)
        
        open_form('Stage_visu_modif',num_stage)   
    
    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

    def button_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.button_1_click()


