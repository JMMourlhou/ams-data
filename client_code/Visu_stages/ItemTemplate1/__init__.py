from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..

class ItemTemplate1(ItemTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_1.text = self.item['numero']
        self.button_2.text = self.item['type']['code']                     # link key
        self.label_1.text = self.item['date_debut'].strftime("%d %m %Y")   # format date française avec fonction Python strftime

    # J'ai mis la variable date ds un link, ce qui la rend clikable ! 
    # et récupération par l'event:
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        num_stage = self.button_1.text
        msg = "Affichage du stage "+ self.button_2.text 
        alert(msg)
        self.content_panel.clear()
        self.content_panel.add_component(Stage_visu_modif(num_stage), full_width_row=True)

    
    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

    def link_date_debut_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.button_1_click()
