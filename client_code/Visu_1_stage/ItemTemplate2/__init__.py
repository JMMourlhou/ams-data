from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate2(ItemTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        
        #lecture fichier users à partir du mail
        mel=self.item["user_email"]['email']
        stagiaire = app_tables.users.get(email=mel)    
        if stagiaire :
            self.text_box_1.text = stagiaire['nom']        #nom
            self.text_box_2.text = stagiaire['prenom']      #prénom
            self.text_box_3.text = stagiaire['email']
            self.text_box_4.text = stagiaire['tel']
            
            #self.image_1.source = stagiaire['photo']      #photo
            orig_pic = stagiaire['photo']
            if orig_pic != None:
                thumb_pic = anvil.image.generate_thumbnail(orig_pic, 320)
                self.image_1.source = thumb_pic

            
            # self.text_box_5.text
            fi = self.item["financement"]["code_fi"]
            finance = app_tables.mode_financement.get(code_fi=fi)
            self.text_box_5.text = finance['intitule_fi']