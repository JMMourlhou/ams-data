from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import French_zone # calcul tps traitement

from ..._Constant_parameters_public_ok import nb_fiche_stagiaire_pdf   # pour param nb de fiches à imprimer 
from anvil_extras.PageBreak import PageBreak
global cpt      # ATTENTION, si j'utilise self.cpt, le décrément ne s'effectue pas
cpt = 0

# Repeating panel appelée par Visu_liste_1_stage, affichage des fiches stagiaires
class ItemTemplate2(ItemTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.      
        stage_row=self.item['stage']
        liste = app_tables.stagiaires_inscrits.search(stage=stage_row)
        nb_stagiaires = len(liste)
        print(nb_stagiaires)
        # explication: s'il y a 4 stgiaires à afficher ou moins sur une page, je mets le compteur à 5 donc il n'y aura pas de saut de page 
        global cpt
        if nb_stagiaires < nb_fiche_stagiaire_pdf:
            cpt=5
        # explication:    
        # si nb stagiaires = 5, j'initialise le compteur d'image de la page à 1. Qd fonction image_1_show s'exécute, self.cpt sera décrémenté de 1 donc = 0, donc saut de page   
        
        if nb_stagiaires == 5 or nb_stagiaires == 10 or nb_stagiaires == 15 or nb_stagiaires == 20 or nb_stagiaires == 25 or nb_stagiaires == 30:
            cpt=1    
        if nb_stagiaires == 6 or nb_stagiaires == 11 or nb_stagiaires == 16 or nb_stagiaires == 21 or nb_stagiaires == 26 or nb_stagiaires == 31:
            cpt=2
        if nb_stagiaires == 7 or nb_stagiaires == 12 or nb_stagiaires == 17 or nb_stagiaires == 22 or nb_stagiaires == 27 or nb_stagiaires == 32:
            cpt=3
        if nb_stagiaires == 8 or nb_stagiaires == 13 or nb_stagiaires == 18 or nb_stagiaires == 23 or nb_stagiaires == 28 or nb_stagiaires == 33:
            cpt=4
        if nb_stagiaires == 9 or nb_stagiaires == 14 or nb_stagiaires == 19 or nb_stagiaires == 24 or nb_stagiaires == 29  or nb_stagiaires == 34:
            cpt=5
        """    
        if nb_stagiaires == 5 or nb_stagiaires == 10 or nb_stagiaires == 15 or nb_stagiaires == 20 or nb_stagiaires == 25 or nb_stagiaires == 30:
            cpt=1    
        if nb_stagiaires == 6 or nb_stagiaires == 11 or nb_stagiaires == 16 or nb_stagiaires == 21 or nb_stagiaires == 26 or nb_stagiaires == 31:
            cpt=2
        if nb_stagiaires == 7 or nb_stagiaires == 12 or nb_stagiaires == 17 or nb_stagiaires == 22 or nb_stagiaires == 27 or nb_stagiaires == 32:
            cpt=3
        if nb_stagiaires == 8 or nb_stagiaires == 13 or nb_stagiaires == 18 or nb_stagiaires == 23 or nb_stagiaires == 28 or nb_stagiaires == 33:
            cpt=4
        if nb_stagiaires == 9 or nb_stagiaires == 14 or nb_stagiaires == 19 or nb_stagiaires == 24 or nb_stagiaires == 29  or nb_stagiaires == 34:
            cpt=5
        """    
        #lecture fichier users à partir du mail
        mel=self.item["user_email"]['email']
        stagiaire = app_tables.users.get(   q.fetch_only("photo", 'date_naissance', 'nom', 'prenom', 'email', 'tel', 'ville_naissance','code_postal_naissance','pays_naissance','adresse_rue','adresse_code_postal','adresse_ville'),
                                            email=mel)    
        if stagiaire :
            start = French_zone.french_zone_time()  # pour calcul du tps de traitement (environ 25 se)
            #Photo
            self.image_1.source = stagiaire['photo']
            end = French_zone.french_zone_time()
            print("Temps de traitement image: ", end-start)
            
            # self.text_box_5.text
            fi = self.item["financement"]["code_fi"]
            finance = app_tables.mode_financement.get(code_fi=fi)
            #self.text_box_5.text = finance['intitule_fi']

            self.rich_text_1.border="0px solid blue"
            self.rich_text_1.font_size=14
            self.rich_text_1.bold=False
            self.rich_text_1.italic=False
            self.rich_text_1.align="center"
            #self.rich_text_1.font="Noto"
            try: # si pas date de naissance, (user type T, F, A, )
                date_naiss_format = stagiaire['date_naissance'].strftime("%d/%m/%Y")
                self.rich_text_1.content=f" **{stagiaire['nom']} {stagiaire['prenom']}** ({finance['code_fi']}) \n{stagiaire['email']} \n {stagiaire['tel']} "
                self.rich_text_2.content=f" Né le {date_naiss_format} à {stagiaire['ville_naissance']} ({stagiaire['code_postal_naissance']} {stagiaire['pays_naissance']}) \n {stagiaire['adresse_rue']}, {stagiaire['adresse_code_postal']} {stagiaire['adresse_ville']} "
                
            except:
                self.rich_text_1.content=f" **{stagiaire['nom']} {stagiaire['prenom']}**  \n{stagiaire['email']} \n {stagiaire['tel']} "
                self.rich_text_2.content= ""


    def image_1_show(self, **event_args):
        #This method is called when the Image is shown on the screen
        global cpt
        # self.cpt : nb d'images imprimées
        print("cpt en image_schow avat décrément: ", cpt)
        cpt -= 1       
        if cpt == 0 :          # ts les 1 ou 5 stagiaires, selon param global
           self.add_component(PageBreak())      # si en création de pdf, je saute une page ts les n stagiares 
           print("saut") 
           cpt = nb_fiche_stagiaire_pdf    # réinitialisation du nb de fiche par page avec le param global
