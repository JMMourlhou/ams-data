from ._anvil_designer import Stage_com_results_stagiairesTemplate
from .. import French_zone  # POur acquisition de date et heure Francaise (Browser time)
from anvil import *
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# Le stagiaire note un de ses co-stgiaire du même stage en communication ou autre présentation
class Stage_com_results_stagiaires(Stage_com_results_stagiairesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form("Main", 99)
