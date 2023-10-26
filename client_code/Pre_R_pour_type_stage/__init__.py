from ._anvil_designer import Pre_R_pour_type_stageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Pre_R_visu_modif import Pre_R_visu_modif


class Pre_R_pour_type_stage(Pre_R_pour_type_stageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # Drop down codes stages
        self.drop_down_code_stage.items = [(r['code'], r) for r in app_tables.codes_stages.search()]

        # affiches toutes les lignes de la table pré requis
        self.affiche_lignes_pre_requis()

    def affiche_lignes_pre_requis(self):
        self.column_panel_content.clear()
        self.column_panel_content.add_component(Pre_R_visu_modif(), full_width_row=True)

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)


