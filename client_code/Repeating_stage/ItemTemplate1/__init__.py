from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate1(ItemTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_1.text = self.item['numero']
        self.button_2.text = self.item['type']['code']
        self.label_1.text = self.item['date_debut']
        #self.date_picker_2.date = self.item['date_fin']
        #self.button_3.text = self.item['date_fin'].strftime("%d %m %Y")

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        num_stage = self.button_1.text
        msg = f("Inscrition {self.button_2.text})
        alert("",self.button_2.text,num_stage)

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

    def link_date_debut_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.button_1_click()


