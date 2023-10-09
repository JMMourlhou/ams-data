from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate4(RowTemplate4Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        #lecture fichier users, à partir du mail, pour avoir le prénom
        stagiaire_row=app_tables.users.get(email=self.item['user_email']['email'])
        self.text_area_1.text = self.item['name'].capitalize()+" "+stagiaire_row["prenom"].capitalize()
        self.text_box_1.text = self.item['user_email']['email']
        self.text_box_2.text = stagiaire_row['tel']

    def text_area_1_focus(self, **event_args):
        """This method is called when the text area gets focus"""
        pass

    def text_box_1_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        pass

    def text_box_2_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        pass



        