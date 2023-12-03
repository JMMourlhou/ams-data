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
    def __init__(self, first_entry=False, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Any code you write here will run before the form opens.
        self.first_entry = first_entry
        if first_entry == True:
            self.button_retour.visible = False
        # Drop down mode de financemnt
        self.drop_down_fi.items = [(r['intitule_fi'], r) for r in app_tables.mode_financement.search()]
        if self.first_entry:  # si 1ere entrée ds fiche d'info
            self.drop_down_fi.visible = True

        user=anvil.users.get_user()
        if user:
            self.text_box_mail.text =                user['email']
            self.text_box_nom.text =                 user["nom"]
            self.text_box_prenom.text =              user["prenom"]

            #self.image_photo.source =                user["photo"]
            if user["photo"] != None:
                thumb_pic = anvil.image.generate_thumbnail(user["photo"], 640)
                self.image_photo.source = thumb_pic
            else:
                self.image_photo.source =            user["photo"]

            self.text_box_v_naissance.text =         user["ville_naissance"]
            self.text_box_c_naissance.text =         user["code_postal_naissance"]
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
            self.histo =                             user['histo']
                
            if user['admin'] == True:
               self.text_box_email2.visible = True
               self.text_area_commentaires.visible = True
        else:
            self.button_retour_click()

    def file_loader_photo_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        #self.image_photo.source = file
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_photo.source = thumb_pic
        self.button_validation.visible = True

    def button_validation_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.text_box_prenom.text == "" :           # dates vides ?
            alert("Entrez le prénom !")
            return
        p=self.text_box_prenom.text
        p=p.capitalize()
        self.text_box_prenom.text = p
        if self.text_box_nom.text == "" :           # dates vides ?
            alert("Entrez le nom !")
            return
        if self.text_box_tel.text == "":    # tel vides ou inf à 10 caract ?
            alert("Entrez le teléphone !")
            return
        if len(self.text_box_tel.text) < 10:    # tel inf à 10 caract ?
            alert("Le numéro de teléphone n'est pas valide !")
            return   
        if self.date_naissance.date == None :           # dateN vide ?
            alert("Entrez la date de naissance !")
            return   
        if self.text_box_v_naissance.text == "" :    # ville N vide ?
            alert("Entrez la ville de naissance !")
            return   
        if self.text_area_rue.text == "":
            alert("Entrez votre adresse (Rue) !")
            return  
        if self.text_box_ville.text == "":
            alert("Entrez votre adresse (Ville) !")
            return
        if self.text_box_code_postal.text == "":
            alert("Entrez votre adresse (Code Postal) !")
            return
        # Si mode de financemt non sélectionné alors que 1ere saisie de la fiche renseignemnt
        if self.drop_down_fi.selected_value == None and self.first_entry==True: 
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
                                                    self.text_box_v_naissance.text,
                                                    self.text_box_c_naissance.text,
                                                    self.date_naissance.date,
                                                    self.text_box_pays_naissance.text,
                                                    self.text_area_rue.text,
                                                    self.text_box_ville.text,
                                                    self.text_box_code_postal.text,
                                                    self.text_box_tel.text,
                                                    self.text_box_email2.text,
                                                    self.check_box_accept_data_use.checked,
                                                    self.text_area_commentaires.text,
                                                    self.histo
                                                    )
            if result == True :
                alert("Renseignements enregistés !")    # *************************************
                # insertion du stagiaire automatiqt si num_stage != 0
                user=anvil.users.get_user()
                if user and self.first_entry:          # 1ERE ENTREE 
                    stage=str(user['stage_num_temp'])
                    if  user['stage_num_temp']==0:
                        alert("User non trouvé en 1ere entrée !")
                        self.button_retour_click()
                    else:
                        row = self.drop_down_fi.selected_value
                        code_fi=row['code_fi']
                        txt_msg = anvil.server.call("add_stagiaire", user, stage, code_fi, type_add="")
                        alert(txt_msg)
                        anvil.users.logout()
                        alert("Connectez-vous maintenand.")
                        self.button_retour_click()
            else :
                alert("Fiche de renseignements non enregistée !")
                self.button_retour_click()
        else:
            alert("utilisateur non trouvé !")
            self.button_retour_click()
            
    def button_retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99) 
        

        #js.call_js('showSidebar')
        
    
    
    def text_box_nom_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.button_validation.visible = True
        self.button_validation_copy.visible = True

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
            














            

        

