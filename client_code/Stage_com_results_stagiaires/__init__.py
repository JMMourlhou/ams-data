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


# Résultat des évaluation en comm pour une date précise 
class Stage_com_results_stagiaires(Stage_com_results_stagiairesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # Initialisation dropdown date
        liste_dates = []
        liste_initiale = app_tables.com_sum.search()
        for date_row in liste_initiale:
            if date_row["date"] not in liste_dates:
                liste_dates.append((date_row['date'], date_row))
        self.drop_down_date.items = liste_dates

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form("Main", 99)
