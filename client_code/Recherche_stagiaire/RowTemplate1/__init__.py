from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# pour passer des datas d'une forme à l'autre (recherche_stagiaire vers RowTemplate)
from ...common import publisher

global num_stage  # pour le click sur button_5 et envoie ds le stage
num_stage = 0

global msg
msg = ""  # si vient du bt inscription de la forme Visu_stages, "inscription/num_stage" (passation par Anvil extra Messaging) 

global cpt
cpt = 0

class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        """
        Je ne peux pas remonter ds mes components pour savoir si je suis en mode "inscription",
            à partir de la forme Visu_stages
        Donc j'utilise l'Anvil extra 'Messaging' 
        """
        publisher.subscribe(channel="general", subscriber=self, handler=self.general_messages_handler)
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        
        try:          # Liste à partir table users
            cumul_clefs_histo = ""
            if self.item['histo'] != {} or self.item['histo'] != None:   #lecture du dictionnaire historique des stages du stagiaire
                historique = self.item['histo']
                cpt = 1
                for clef,valeur in historique.items():   #Boucle sur le dictionnaire histo ds Users
                    print(clef)
                    global num_stage
                    num_stage = valeur[0]   # le num stage est le premier élément de valeur (clef:valeur) 
                    test_tag_vide = self.button_5.tag
                    if cpt == 1:   # si c'est le stage le plus récent, je le retient pour l'afficher si bt 5 clické
                        self.button_5.tag = num_stage
                    cpt += 1
                    cumul_clefs_histo = cumul_clefs_histo + " " + clef

            self.button_1.text = self.item['nom']+" "+self.item['prenom']
            self.button_3.text = self.item['tel']
            self.button_4.text = self.item['email']
            self.button_5.text = cumul_clefs_histo
        except: # ***********************************  Liste à partir table Stagiaires inscrits
            # lecture table users à partir du mail du stagiaire
            mel = self.item['user_email']['email']
            user = app_tables.users.get(email=mel)
            self.button_1.text = user['nom']+" "+user['prenom']
            self.button_3.text = user['tel']
            self.button_4.text = user['email']
            # lecture fichier père stage pour obtenir le num et date du stage
            st = self.item['stage']['numero']
            stg = app_tables.stages.get(numero=st)
            self.button_5.text = str(stg['date_debut'])+" / "+str(stg['numero'])
            self.button_5.tag = st

    def general_messages_handler(self, message):     # Anvil extra Messaging
        
        global cpt
        if cpt == 0:
            global msg
            msg = message.title
            print("message;", message.title)
        
            
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        global msg
        alert(msg)
        if msg=="recherche":
            try:
                mel = self.item['email']   
            except:
                mel = self.item['user_email']['email']
            from ...Saisie_info_apres_visu import Saisie_info_apres_visu
            open_form('Saisie_info_apres_visu', mel, num_stage=0, intitule="", provenance="recherche")
        else:  # inscription du stgiaire au satge
            alert( msg )
            alert(self.item['email'])

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

    def button_4_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

    def button_5_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.button_5.text != "":
            num_stage = self.button_5.tag
            if num_stage != 0:
                open_form('Stage_visu_modif',"recherche",num_stage) 

    def column_panel_1_show(self, **event_args):
        """This method is called when the column panel is shown on the screen"""
        global cpt
        cpt += 1




        
        
        