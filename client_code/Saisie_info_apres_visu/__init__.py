from ._anvil_designer import Saisie_info_apres_visuTemplate
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

class Saisie_info_apres_visu(Saisie_info_apres_visuTemplate):
    def __init__(self, mel, num_stage=0, intitule="", provenance="", **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.num_stage = num_stage
        self.intitule = intitule
        self.mel = mel
        self.provenance=provenance
        # Any code you write here will run before the form opens.

        # Drop down mode de financemnt
        self.drop_down_fi.items = [(r['intitule_fi'], r) for r in app_tables.mode_financement.search()]

        # lecture sur le mail du stagiaire après click sur trombi
        user=app_tables.users.get(email=self.mel)

        if user:
            self.text_box_mail.text =                user['email']
            self.text_box_nom.text =                 user["nom"].capitalize()
            self.text_box_prenom.text =              user["prenom"].capitalize()

            #self.image_photo.source =                user["photo"]
            if user["photo"] != None:
                thumb_pic = anvil.image.generate_thumbnail(user["photo"], 320)
                self.image_photo.source = thumb_pic
            else:
                self.image_photo.source =            user["photo"]

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
        #self.image_photo.source = file
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_photo.source = thumb_pic
        self.button_validation.visible = True

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
        if len(self.text_box_tel.text) < 10:    # tel inf à 10 caract ?
            alert("Le numéro de teléphone n'est pas valide")
            return
        if self.date_naissance.date == None :           # dateN vide ?
            alert("Entrez la date de naissance")
            return
        if self.text_box_ville_naissance.text == "" :    # ville N vide ?
            alert("Entrez la ville de Naissance")
            return

        if self.check_box_accept_data_use.checked != True:
            r=alert("Voulez-vous valider l'utilisation de vos données par AMsport ?",buttons=[("oui",True),("non",False)])
            if r :   #Non, nom pas correct
                self.check_box_accept_data_use.checked = True
                return

        # lecture sur le mail du stagiaire après click sur trombi
        user=app_tables.users.get(email=self.mel)
        if user:
            result = anvil.server.call("modify_users_after_trombi", self.mel,
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
                alert("Renseignements enregistés !")
            else :
                alert("Renseignements non enregistés !")
            self.button_annuler_click()
        else:
            alert("utilisateur non trouvé !")
            self.button_annuler_click()



        #js.call_js('showSidebar')

    def text_box_nom_change(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
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

    def button_download_photo_click(self, **event_args):
        """This method is called when the button is clicked"""
        "lecture du media object que j'ai stocké en server module ds table stages, ligne du stage"
        # lecture sur le mail du stagiaire après click sur trombi
        user=app_tables.users.get(email=self.mel)
        if not user:
            print("user non trouvé à partir de son mail en saisie après trombi")
        else:
            anvil.media.download(user['photo'])
            alert("Photo téléchargée")

    def button_annuler_copy_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_annuler_click()
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.provenance == "trombi":
            from ..Visu_trombi import Visu_trombi
            open_form('Visu_trombi',self.num_stage, self.intitule, False)
        if self.provenance == "recherche":
            from ..Recherche_stagiaire import Recherche_stagiaire
            open_form('Recherche_stagiaire')
        if self.provenance == "visu_stage":
            from ..Stage_visu_modif import Stage_visu_modif
            open_form('Stage_visu_modif',"recherche",self.num_stage)

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        self.column_panel_1.scroll_into_view()
