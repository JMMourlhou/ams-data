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
        self.title.text = "Fiche de renseignements"
        user=anvil.users.get_user()
        if user:
            self.text_box_nom.text = user["nom"]
            self.text_box_prenom.text = user["prenom"]
            self.text_area_rue.text = user["adresse_rue"]
        else:
            self.content_panel.clear()
            self.content_panel.add_component(Main(), full_width_row=True)
        # Any code you write here will run before the form opens.

    def file_loader_photo_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        self.image_photo.source = file

    def button_validation_click(self, **event_args):
        """This method is called when the button is clicked"""
        result = anvil.server.call("modify_users", user, self.text_box_nom.text, self.text_box_prenom.text)
        if result == True :
            alert("Renseignements validés")
        else :
            alert("Renseignements non validés")
            
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)


