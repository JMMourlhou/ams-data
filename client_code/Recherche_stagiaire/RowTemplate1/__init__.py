from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        """
        Je remonte ds mes components pour tester ce que je display
        Si je recherche sur un type de stage ou sur nom, prénom, tel ...

        
        """
        # Any code you write here will run before the form opens.
 
        # Normalement,dans un Data grid, j'initialise mes lignes en donnant data=nom de la colonne de mon fichier affiché
        # Mais ici, je veux pouvoir clicker sur ma ligne, donc je rajoute des boutons
        try:          # List à partir table users
            self.button_1.text = self.item['nom']+" "+self.item['prenom']
            self.button_3.text = self.item['tel']
            self.button_4.text = self.item['email']
            self.button_5.visible = False
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
            
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        try:
            mel = self.item['email']   
        except:
            mel = self.item['user_email']['email']
        from ...Saisie_info_apres_visu import Saisie_info_apres_visu
        open_form('Saisie_info_apres_visu', mel, num_stage=0, intitule="", provenance="recherche")
        
        
        