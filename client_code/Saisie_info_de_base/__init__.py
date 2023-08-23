from ._anvil_designer import Saisie_info_de_baseTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global user
user = None

class Saisie_info_de_base(Saisie_info_de_baseTemplate):
    def __init__(self, num_stage=0, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        alert("arrivée en saisie info de base")
        user=anvil.users.get_user()
        if user:
            self.text_box_mail.text =                user['email']
            self.text_box_nom.text =                 user["nom"]
            self.text_box_prenom.text =              user["prenom"]
            self.image_photo.source =                user["photo"]
            self.text_box_ville_naissance.text =     user["ville_naissance"]
            self.text_box_cp_naissance.text =        user["code_postal_naissance"]
            self.date_naissance.date =               user["date_naissance"]
            self.text_box_pays_naissance.text =      user["pays_naissance"]
            if user["pays_naissance"] == None :
                self.text_box_pays_naissance.text = "France"
            self.text_area_rue.text =                user["adresse_rue"]
            self.text_box_ville.text =               user["adresse_ville"]
            self.text_box_code_postal.text =         user["adresse_code_postal"]
            self.text_box_tel.text =                 user['tel']
            self.text_box_email2.text =              user['email2']
            self.check_box_accept_data_use.checked = user['accept_data']
            self.text_area_commentaires.text =       user['commentaires']
            if user['admin'] == True:
               self.text_box_email2.visible = True
               self.text_area_commentaires.visible = True
        else:
            self.button_annuler_click()
       

    def file_loader_photo_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        self.image_photo.source = file

    def button_validation_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.text_box_prenom.text == "" :           # dates vides ?
            alert("Entrez le prénom")
            return
        if self.text_box_nom.text == "" :           # dates vides ?
            alert("Entrez le nom")
            return
        if self.text_box_ville_naissance.text == "" :           # dates vides ?
            alert("Entrez la ville de Naissance")
            return   
        if self.text_box_tel.text == "" :           # dates vides ?
            alert("Entrez le teléphone")
            return    
        if self.date_naissance.date == None :           # dates vides ?
            alert("Entrez la date de naissance")
            return   
             
        result = anvil.server.call("modify_users", user,
                                                  self.text_box_nom.text,
                                                  self.text_box_prenom.text,
                                                  self.image_photo.source,
                                                  self.text_box_ville_naissance.text,
                                                  self.text_box_cp_naissance.text,
                                                  self.date_naissance.date,
                                                  self.text_box_pays_naissance.text,
                                                  self.text_area_rue.text,
                                                  self.text_box_ville.text,
                                                  self.text_box_code_postal.text,
                                                  self.text_box_tel.text,
                                                  self.text_box_email2.text,
                                                  self.check_box_accept_data_use.checked,
                                                  self.text_area_commentaires.text
                                                 )
        if result == True :
            alert("Renseignements enregistés")
            # insertion du stagiaire automatiqt si num_stage != 0
            if self.num_stage != 0:
                self.insertion_du_stagiaire()
        else :
            alert("Renseignements non enregistés !")
        self.button_annuler_click()
            
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        #open_form('Main',99)
        open_form('Main')

        #js.call_js('showSidebar')

    def insertion_du_stagiaire(self, **event_args):
         alert(insertion)
            

        

