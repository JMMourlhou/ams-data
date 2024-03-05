from ._anvil_designer import ItemTemplate8Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate8(ItemTemplate8Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_qcm_descro.text = self.item['qcm_number']['destination']
        self.button_qcm_time.text = "le " + str(self.item['time'].strftime("%d/%m/%Y")) + " à " + str(self.item['time'].strftime("%Hh%M")) 
        if self.item['success'] == True:
            self.button_qcm_result.background = "green"
            self.button_qcm_time.background = "green"
        else:
            self.button_qcm_result.background = "red"
            self.button_qcm_time.background = "red"
        self.button_qcm_result.text = str(self.item['p100_sur_nb_rep']) + " %"

    def button_qcm_descro_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def button_qcm_result_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def button_qcm_time_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
