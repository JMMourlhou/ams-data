from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate7(RowTemplate7Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_role.text = self.item['role']
        self.button_nom.text = self.item['nom']
        self.button_prenom.text = self.item['prenom']
        self.button_email.text = self.item['email']
        self.check_box_conf_mail.checked = self.item['confirmed_email']