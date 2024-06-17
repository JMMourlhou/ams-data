from ._anvil_designer import ItemTemplate14Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ...Mail_subject_attach_txt import Mail_subject_attach_txt


class ItemTemplate14(ItemTemplate14Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.button_mail.tag = self.item['user_email']
        # Any code you write here will run before the form opens.
        self.text_box_1.text = self.item['name']+" "+self.item['prenom']

    def button_mail_click(self, **event_args):
        """This method is called when the button is clicked"""
        liste_email = []
        liste_email.append(self.button_mail.tag)   # user row
        
        open_form("Mail_subject_attach_txt",  liste_email)




        
    def temp(self, **event_args):
        row_stagiaire = self.button_mail.tag
        subject_txt = "Formulaire de satisfaction"
        # Envoi au module de choix/modif du texte
        rich_text = """
                        S'il te plaît, effectue l'enquête de satisfaction !

                    """
        result = anvil.server.call("send_mail",row_stagiaire, subject_txt, rich_text)
        if result:
            alert("mail envoyé")

        
        