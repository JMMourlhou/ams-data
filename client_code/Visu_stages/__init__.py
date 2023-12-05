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
from anvil.js import window # to gain access to the window object (taille fenêtre)
global screen_size
screen_size = window.innerWidth

class Visu_stages(Visu_stagesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.    
        if screen_size < 800:
            self.label_en_tete.text = "Stage du ...              Type           Inscription"
        else:
            self.label_en_tete.text = "Stage du ...                 Type              N°...     Inscription "
        
        # Initilisation de la liste des stages à afficher
        """
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
        """
        self.repeating_panel_1.items = app_tables.stages.search(tables.order_by("date_debut", ascending=False),
                                                               )
        self.spacer_1.scroll_into_view()
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)


    def creation_stage_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Stage_creation import Stage_creation
        open_form('Stage_creation')

    def button_gestion_pre_requis_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_R_pour_type_stage import Pre_R_pour_type_stage
        open_form('Pre_R_pour_type_stage')





