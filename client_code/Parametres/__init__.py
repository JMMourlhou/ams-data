from ._anvil_designer import ParametresTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Parametres(ParametresTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

    def button_maj_pr_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Table_Pre_R_MAJ import Table_Pre_R_MAJ
        open_form("Table_Pre_R_MAJ")

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99) 

    def button_gestion_pre_requis_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_R_pour_type_stage import Pre_R_pour_type_stage
        open_form('Pre_R_pour_type_stage')


    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        self.stage_row = self.drop_down_code_stage.selected_value
        self.drop_down_personnes.items = [(r["name"]+" "+r["prenom"], r) for r in app_tables.stagiaires_inscrits.search(
                                                                                                                                tables.order_by("name", ascending=True),
                                                                                                                                stage_txt=self.stage_row["code"]
                                                                                                                                )
                                            ]

    def button_gestion_pre_requis_personnel_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.drop_down_code_stage.items = [(r["code"], r) for r in app_tables.codes_stages.search(tables.order_by("code", ascending=True))]
        self.column_panel_pr_par_personne.visible = True

 
