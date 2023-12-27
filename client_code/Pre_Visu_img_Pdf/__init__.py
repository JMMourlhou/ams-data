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

        # Si le doc pdf a un nom déjà formatté, je le télécharge direct
        media = pr_requis_row['pdf_doc1']   #j'extrai le nom du doc pdf ds la table
        if media != None:
            name_media = media.name[0:3]  
            print(name_media)
            try:
                test_if_integer = int(name_media) # pas d'erreur TRY doc pdf a un nom déjà formatté, je le télécharge direct
                print("nom déja formatté: téléchrgt")

            except:      # si 3 1eres lettres ne sont pas numériques: c'est le doc pdf chargé au départ, et nom d'origine en table, je sauve
                # Il serait bien de trouver la façon de changer le nom de ce fichier binaire avec python
                # https://www.pythoniste.fr/python/travailler-avec-les-i-o-de-fichiers-en-python/
                print("nom pas encore formatté: doc pdf original, téléchrgt après traitement cht de nom")
                media = anvil.server.call("generate_pdf_from_jpg", self.image_1.source, self.new_file_name, self.stage_num, self.email, self.item_requis, pr_requis_row)
               
        else:  # si pas de doc pdf pour ce doc, je le génère et le sauverai   
            print("pdf pas encore créé, téléchrgt après génération et cht de nom")
            
            media = anvil.server.call("generate_pdf_from_jpg", self.image_1.source, self.new_file_name, self.stage_num, self.email, self.item_requis, pr_requis_row)
        anvil.media.download(media)

            



 