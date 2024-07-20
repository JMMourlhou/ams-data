from ._anvil_designer import Pre_R_MoulinetteTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Pre_R_Moulinette(Pre_R_MoulinetteTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def button_mailing_click(self, **event_args):
        """This method is called when the button is clicked"""
        # BOUCLE SUR LA TABLE entierre
        self.liste = app_tables.pre_requis_stagiaire.search()
        self.cpt = 0
        for row in self.liste:
            self.cpt += 1
            #if row['doc1'] is not None and self.cpt <= 3:
            if  self.cpt <= 3:
                print(self.cpt)
                self.task_img = anvil.server.call('run_bg_task_reseize_jpg', row)    
                self.timer_1.interval=0.5


    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        if self.task_img.is_completed(): # lecture de l'image sauvée en BG task
            print(f"{self.cpt} lignes traitées")
            self.timer_1.interval=0
            anvil.server.call('task_killer',self.task_img)
