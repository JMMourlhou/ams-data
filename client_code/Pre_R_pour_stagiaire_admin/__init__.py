from ._anvil_designer import Pre_R_pour_stagiaire_adminTemplate
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Pre_R_pour_stagiaire_admin(Pre_R_pour_stagiaire_adminTemplate):
    def __init__(self, num_stage, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.num_stage = num_stage
        # Any code you write here will run before the form opens.
        #lecture du stage  
        row_stage = app_tables.stages.get(numero=num_stage)
       
        self.label_1.text = "Gestion des pré-Requis, stage " + row_stage['code']['code'] + " du " + str(row_stage['date_debut'].strftime("%d/%m/%Y"))

        # lecture des stagiaires de ce stage
        liste_stagiaires = app_tables.stagiaires_inscrits.search(stage=row_stage
                                                         )
        self.repeating_panel_1.items = liste_stagiaires

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')