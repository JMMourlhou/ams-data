from ._anvil_designer import Table_Pre_R_MAJTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Table_Pre_R_MAJ(Table_Pre_R_MAJTemplate):
    def __init__(self, **properties):  # row stagiaire inscrit, vient de pré_requis_pour stagiaire admin
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

        # search de tous les pré-requis existants
        liste_tous_pr = app_tables.pre_requis.search(
                                                        tables.order_by("requis", ascending=True),
                                                        q.fetch_only("requis", "code_pre_requis"),
                                                    )
        
        # affichage des pré-requis
        self.repeating_panel_1.items = liste_tous_pr


        # réaffichage des pré requis
        #open_form("Table_Pre_R_MAJ")

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)
