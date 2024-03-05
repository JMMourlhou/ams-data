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
        self.button_qcm_time.text = self.item['time'].strftime("%d/%m/%Y, %Hh%M")
        if self.item['success'] == True:
            self.button_qcm_result.background = "green"
        else:
            self.button_qcm_result.background = "red"
        self.button_qcm_result.text = self.item['p100_sur_nb_rep']