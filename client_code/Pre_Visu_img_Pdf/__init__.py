from ._anvil_designer import Pre_Visu_img_PdfTemplate
from anvil import *
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pre_Visu_img_Pdf(Pre_Visu_img_PdfTemplate):
    def __init__(self, file, new_file_name, stage_num, email, item_requis, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.image_1.source = file          
        self.new_file_name = new_file_name
        self.stage_num = stage_num
        self.email = email
        self.item_requis = item_requis
        self.label_1.text = self.new_file_name

    def retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')

    def download_click(self, **event_args):
        """This method is called when the button is clicked"""
        # finding the stagiaire's row et envoi du row au serveur
        pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = self.stage_num,
                                              stagiaire_email = self.email,
                                              item_requis = self.item_requis                                             
                                             )                                      
        if not pr_requis_row:
            alert("Erreur: stagiaire not found !")
    
        media_object = anvil.server.call("generate_pdf_from_jpg", self.image_1.source, self.new_file_name, self.stage_num, self.email, self.item_requis, pr_requis_row)
        anvil.media.download(media_object) 

            



 