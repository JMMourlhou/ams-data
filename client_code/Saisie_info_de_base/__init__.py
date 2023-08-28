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
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        
        # Drop down mode de financemnt
        
        self.drop_down_fi.items = [(r['intitule_fi'], r) for r in app_tables.mode_financement.search()]
        
        user=anvil.users.get_user()
        if user:
            #self.drop_down_fi.selected_value = à faire ?
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
            alert("Entrez le prénom !")
            return
        if self.text_box_nom.text == "" :           # dates vides ?
            alert("Entrez le nom !")
            return
        if self.text_box_tel.text == "" :              # tel vides ?
            alert("Entrez le teléphone")
            return    
        if self.date_naissance.date == None :           # dateN vide ?
            alert("Entrez la date de naissance")
            return   
        if self.text_box_ville_naissance.text == "" :    # ville N vide ?
            alert("Entrez la ville de Naissance")
            return   
        if self.drop_down_fi.selected_value == None :
            alert("Vous devez sélectionner un mode de financement !")
            return
        if self.check_box_accept_data_use.checked != True:
            r=alert("Voulez-vous valider l'utilisation de vos données par AMsport ?",buttons=[("oui",True),("non",False)])
            if r :   #Non, nom pas correct
                self.check_box_accept_data_use.checked = True
                return
    
        user=anvil.users.get_user()
        if user:
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
                alert("Renseignements enregistés !")    # *************************************
                # insertion du stagiaire automatiqt si num_stage != 0
                user=anvil.users.get_user()
                if user:
                    stage = str(user['stage_num_temp'])
                    if  stage :
                        row = self.drop_down_fi.selected_value
                        code_fi=row['code_fi']
                        alert(code_fi)
                        self.insertion_du_stagiaire(user, code_fi, stage)
                    self.button_annuler_click()
            else :
                alert("Renseignements non enregistés !")
            self.button_annuler_click()
        else:
            alert("utilisateur non trouvé !")
            self.button_annuler_click()
            
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        #open_form('Main',99)
        open_form('Main')

        #js.call_js('showSidebar')
        
    """ INSERTION DU STAGIAIRE **********************************************"""
    def insertion_du_stagiaire(self, user, code_fi, stage, **event_args):
        #alert("insertion du stagiaire")
        alert(code_fi)
        result = anvil.server.call("add_stagiaire", user, stage, code_fi)
        if result:
            alert("Vous avez été inscrit au stage")
        else:
            alert("Inscription non effectuée !")

        # le code stage ds user a été effacé au server module add_stagiaire
    
    def text_box_nom_change(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.button_validation.visible = True

    def text_box_prenom_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def text_box_tel_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def text_box_mail_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def date_naissance_change(self, **event_args):
        """This method is called when the selected date changes"""
        self.text_box_nom_change()

    def text_box_ville_naissance_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def text_box_cp_naissance_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def text_box_pays_naissance_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def text_area_rue_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.text_box_nom_change()

    def text_box_ville_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def text_box_code_postal_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def text_box_email2_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.text_box_nom_change()

    def text_area_commentaires_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.text_box_nom_change()

    def drop_down_fi_change(self, **event_args):
        """This method is called when an item is selected"""
        self.text_box_nom_change()
            














            

        

