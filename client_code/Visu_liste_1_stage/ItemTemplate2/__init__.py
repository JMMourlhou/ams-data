from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil_extras.PageBreak import PageBreak
global cpt  # Cpt le nb de form imprimée
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
            #self.rich_text_1.font="Noto"
            date_naiss_format = stagiaire['date_naissance'].strftime("%d/%m/%Y")
            #self.rich_text_1.background="theme:Primary"
            #self.rich_text_1.foreground="theme:On Primary"
            self.rich_text_1.content=f" **{stagiaire['nom']} {stagiaire['prenom']}** ({finance['code_fi']}) \n{stagiaire['email']} \n {stagiaire['tel']} "
            self.rich_text_2.content=f" Né le {date_naiss_format} à {stagiaire['ville_naissance']} ({stagiaire['code_postal_naissance']} {stagiaire['pays_naissance']}) \n {stagiaire['adresse_rue']}, {stagiaire['adresse_code_postal']} {stagiaire['adresse_ville']} "


    def image_1_show(self, **event_args):
        #This method is called when the Image is shown on the screen
    
        global cpt  # Cpt le nb de form imprimée
        cpt += 1
        # Lecture de la variable globale "nb_fiche_stagiaire_pdf" ds table variables_globales
        nb_stag_par_page = anvil.server.call('get_variable_value', "nb_fiche_stagiaire_pdf")
        if (cpt // nb_stag_par_page) * nb_stag_par_page == cpt:          # ts les 1 ou 5 stagiaires, selon param global
           self.add_component(PageBreak())      # si en création de pdf, je saute une page ts les n stagiares 
