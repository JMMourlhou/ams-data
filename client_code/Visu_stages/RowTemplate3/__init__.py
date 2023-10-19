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
        self.text_box_1.text = self.item['numero']
        stage = self.item['code']['code']
        stage = stage.trim()
        self.text_box_2.text = self.item['code']['code']                     # link key
        if self.item['date_debut'] != None:
            self.text_box_3.text = self.item['date_debut'].strftime("%d/%m/%Y")   # format date française avec fonction Python strftime
        

    # récupération par l'event:
    def text_box_1_focus(self, **event_args):
        """This method is called when the button is clicked"""
        num_stage = int(self.text_box_1.text)
        open_form('Stage_visu_modif',"visu_stages", num_stage)   
    
    def text_box_2_focus(self, **event_args):
        """This method is called when the button is clicked"""
        self.text_box_1_focus()

    def text_box_3_focus(self, **event_args):
        """This method is called when the link is clicked"""
        self.text_box_1_focus()

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass



