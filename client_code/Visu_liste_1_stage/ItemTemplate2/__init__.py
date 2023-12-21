from ._anvil_designer import ItemTemplate2Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras.PageBreak import PageBreak
from ... import constant_parameters

global cpt  # compteur des lignes
cpt = 0

class ItemTemplate2(ItemTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        
        #lecture fichier users à partir du mail
        mel=self.item["user_email"]['email']
        stagiaire = app_tables.users.get(email=mel)    
        if stagiaire :
            #Photo
            orig_pic = stagiaire['photo']
            if orig_pic != None:
                thumb_pic = anvil.image.generate_thumbnail(orig_pic, 320)
                self.image_1.source = thumb_pic
            
            # self.text_box_5.text
            fi = self.item["financement"]["code_fi"]
            finance = app_tables.mode_financement.get(code_fi=fi)
            #self.text_box_5.text = finance['intitule_fi']

            self.rich_text_1.border="0px solid blue"
            self.rich_text_1.font_size=17
            self.rich_text_1.bold=False
            self.rich_text_1.italic=False
            self.rich_text_1.align="center"
            self.rich_text_1.font="Noto"
            #self.rich_text_1.background="theme:Primary"
            #self.rich_text_1.foreground="theme:On Primary"
            self.rich_text_1.content=f" {stagiaire['nom']} {stagiaire['prenom']} ({finance['code_fi']}) \n{stagiaire['email']} \n {stagiaire['tel']} "
            self.rich_text_2.content=f" Né le {stagiaire['date_naissance']} " #" ({stagiaire['code_postal_naissance']}, {stagiaire['pays_naissance']})} "
            #self.rich_text_2.content=f" Né le {stagiaire['date_naissance']} à {stagiaire['ville_naissance'] ({stagiaire['code_postal_naissance']}, {stagiaire['pays_naissance']})} "


    def image_1_show(self, **event_args):
        """This method is called when the Image is shown on the screen"""
        
        global cpt  # Cpt le nb de form imprimée
        cpt += 1
        print(cpt)
        #récup du param 
        nb_stag_par_page = constant_parameters.nb_fiche_stagiaire_pdf
        if (cpt // nb_stag_par_page) * nb_stag_par_page == cpt:          # ts les 1 ou 6 stagiaires, selon param global
           #print("saut")
           self.add_component(PageBreak())      # si en création de pdf, je saute une page ts les 6 stagiares 
       
           
        

                                    