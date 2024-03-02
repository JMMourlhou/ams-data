from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate7(ItemTemplate7Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        nom_p = self.item['user_qcm']['nom']+" "+self.item['user_qcm']['prenom']
        self.button_nom_prenom.text = nom_p
        self.button_qcm_designation.text = self.item['qcm_number']['destination']
        self.button_date_heure.text = self.item['time']
        self.button_result.text = self.item['p100_sur_nb_rep']+" %"