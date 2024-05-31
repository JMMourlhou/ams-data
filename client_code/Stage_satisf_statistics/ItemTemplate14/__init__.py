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


class ItemTemplate14(ItemTemplate14Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.button_mail.tag = self.item['user_email']
        # Any code you write here will run before the form opens.
        self.text_box_1.text = self.item['name']+" "+self.item['prenom']

    def button_mail_click(self, **event_args):
        """This method is called when the button is clicked"""
        stagiaire_email = self.button_mail.tag
        rich_text = "Formulaire de satisfaction à entrer \n \n Voici le lien à clicker: "
        subject_txt = "Formulaire de satisfaction"
        
        result = anvil.server.call("send_mail",stagiaire_email, subject_txt, rich_text)
        if result:
            alert("mail envoyé")
