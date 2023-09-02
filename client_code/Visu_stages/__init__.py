from ._anvil_designer import Visu_stagesTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Stage_visu_modif
from .. import constant_parameters  # importation du module contenant mes variables globales


class Visu_stages(Visu_stagesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
     
        # Initilisation de la liste à afficher
        # Je prend les 10 derniers stages, triés de la derniere date de début à la première
        nb_stages_max = constant_parameters.nb_stages_a_montrer
        num = app_tables.cpt_stages.search()[0]
        num_max = int(num['compteur'])+1
        num_min = num_max-10
        self.repeating_panel_1.items = app_tables.stages.search(
                                                                tables.order_by("date_debut", ascending=False),
                                                                numero = q.between(
                                                                min=num_min,
                                                                max=num_max,
                                                                min_inclusive=False)
                                                                )
       
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main')

    def button_annuler2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_annuler_click()

    def admin_creation_stage_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Stage_creation import Stage_creation
        open_form('Stage_creation')




                                                                                                                    
                                                                