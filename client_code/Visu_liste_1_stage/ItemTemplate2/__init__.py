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
global cpt  # Cpt le nb d'images imprimées
cpt = -1

# Repeating panel appelée par Visu_liste_1_stage, affichage des fiches stagiaires
class ItemTemplate2(ItemTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.      
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
    
        global cpt  # Cpt le nb d'images imprimées
        cpt += 1
        mail = self.item["user_email"]['email']
        test = (cpt // nb_fiche_stagiaire_pdf) * nb_fiche_stagiaire_pdf
        print(f"{cpt}: {mail} / {test}")
        # variable globale "nb_fiche_stagiaire_pdf" (module public variables_globales)   VOIR IMPORT EN HAUT

        #nb_fiche_stagiaire_pdf = anvil.server.call('get_variable_value', "nb_fiche_stagiaire_pdf")
        if (cpt // nb_fiche_stagiaire_pdf) * nb_fiche_stagiaire_pdf == cpt and cpt != 0:          # ts les 1 ou 5 stagiaires, selon param global
           self.add_component(PageBreak())      # si en création de pdf, je saute une page ts les n stagiares 
