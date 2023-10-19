from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



global num_stage  # pour le click sur button_5 et envoie ds le stage
num_stage = 0

class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        """
        Je remonte ds mes components pour tester le tag du repeating panel ("inscription" ?)
        """
        panel = self.button_1.parent
        row = panel.parent
        grid = row.parent
        cp = grid.parent
        print(panel, panel.tag)
        print(row, row.tag)
        #print(grid, grid.tag)
        print(cp, cp.tag)
        
        
        
        
        # Normalement,dans un Data grid, j'initialise mes lignes en donnant data=nom de la colonne de mon fichier affiché
        # Mais ici, je veux pouvoir clicker sur ma ligne, donc je rajoute des boutons
        try:          # List à partir table users
            cumul_clefs_histo = ""
            if self.item['histo'] != {} or self.item['histo'] != None:   #lecture du dictionnaire hisorique des stages du stagiaire
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
        except:                                      # List à partir table Stagiaires inscrits
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
            
            
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        try:
            mel = self.item['email']   
        except:
            mel = self.item['user_email']['email']
        from ...Saisie_info_apres_visu import Saisie_info_apres_visu
        open_form('Saisie_info_apres_visu', mel, num_stage=0, intitule="", provenance="recherche")

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



        
        
        