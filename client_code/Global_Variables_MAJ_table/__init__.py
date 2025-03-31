from ._anvil_designer import Global_Variables_MAJ_tableTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Global_Variables_MAJ_table(Global_Variables_MAJ_tableTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_box_1.placeholder = "Code stage"
        self.text_box_2.placeholder = "Intitulé"
        self.text_box_3.placeholder = "Type de stage (S/B/F/T/V)"

        # search de tous les stages existants et affichage
        liste_tous = app_tables.global_variables.search(
            tables.order_by("name", ascending=True)
        )
        self.repeating_panel_1.items = liste_tous

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Parametres import Parametres
        open_form("Parametres")

    def button_add_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.column_panel_add.visible = True
