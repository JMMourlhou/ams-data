from ._anvil_designer import Pre_Visu_img_PdfTemplate
from anvil import *  # pour la notification

import anvil.server
from anvil.tables import app_tables

class Pre_Visu_img_Pdf(Pre_Visu_img_PdfTemplate):
    def __init__(self, file, new_file_name, stage_num, email, item_requis, origine, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.f = get_open_form()
        
        self.image_1.source = file          
        self.new_file_name = new_file_name
        self.stage_num = stage_num          # stage row
        self.email = email                  # user row
        self.item_requis = item_requis      # item requis row
        self.label_1.text = self.new_file_name
        self.origine = origine
       

    def retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form(self.f)
        """
        stage = self.stage_num['numero']
        
        if self.origine == "admin":
            from ..Pre_R_pour_stagiaire_admin import Pre_R_pour_stagiaire_admin
            open_form('Pre_R_pour_stagiaire_admin',stage)
        else:     #origine = "stagiaire"
            if self.origine == "recherche":
                from ..Recherche_stagiaire import Recherche_stagiaire
                open_form('Recherche_stagiaire') 
            else:
                from ..Pre_R_pour_stagiaire import Pre_R_pour_stagiaire
                open_form("Pre_R_pour_stagiaire")
        """   

    def download_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        # finding the stagiaire's row et envoi du row au serveur
        pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = self.stage_num,
                                              stagiaire_email = self.email,
                                              item_requis = self.item_requis                                             
                                             )                                      
        if not pr_requis_row:
            print("Erreur: stagiaire not found !")
        
        # Si le doc pdf a un nom déjà formatté, je le télécharge direct
        media = pr_requis_row['doc1']   #j'extrai le nom du doc ds la table
       
        anvil.media.download(media)
        n = Notification("Téléchargement effectué !",
                 timeout=1)   # par défaut 2 secondes
        n.show()

            



 