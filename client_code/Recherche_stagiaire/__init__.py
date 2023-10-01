from ._anvil_designer import Recherche_stagiaireTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Recherche_stagiaire(Recherche_stagiaireTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def text_box_nom_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        critere = self.text_box_nom.text
        self.filtre_sur_nom(critere)

    def filtre_sur_nom(self, critere):
        
        self.repeating_panel_1.items = app_tables.users.search(
            tables.order_by("nom", ascending=True),

        )
        """
        self.repeating_panel_1.items = app_tables.users.search(
            tables.order_by("nom", ascending=True),
            nom=q.ilike(self.text_box_nom.text)
        )
        """
