from ._anvil_designer import ItemTemplate21Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate21(ItemTemplate21Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_date.text = self.item['date']
        self.button_mot_clef.text = self.item['mot_clef']
        self.button_lieu.text = self.item['lieu_text']

    def button_date_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def button_lieu_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def button_mot_clef_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous vraiment effacer cet évenement ?",dismissible=False,buttons=[("oui",True),("non",False)])
        if r :   # oui
            result = anvil.server.call("del_event", self.item)
            if result is not True:
                alert("ERREUR, Effacement non effectué !")
                return
            alert("Effacement effectué !")
        open_form("Evenements_visu_modif_del")
