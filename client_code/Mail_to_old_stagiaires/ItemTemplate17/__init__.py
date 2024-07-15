from ._anvil_designer import ItemTemplate17Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
#import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate17(ItemTemplate17Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.label_mail.text = self.item['mail']
        try:
            nom_p = self.item['nom'] + " " + self.item['prenom']   # cas où nom prenom vides
        except:
            pass
        self.label_nom.text = nom_p
        self.check_box_envoi.checked = self.item['envoi']
        try:
            self.label_date_heure.text = str(self.item['Date_time_envoi'])[0:16]  # cas où date encore vide
        except:
            pass
        self.label_date.text = self.item['date_diplome']
        self.check_box_selection.checked = self.item['select']


    def check_box_envoi_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        # Récup de l'id pour MAJ de l'item
        result = anvil.server.call("maj_histo_envoi",self.item,self.check_box_envoi.checked)
        if result is not True:
            alert("Erreur de MAJ")

    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous enlever cet historique ?",buttons=[("oui",True),("non",False)])
        if r :     
            result = anvil.server.call("del_histo",self.item)
            if result is not True:
                alert("Item non retiré")
        open_form('Mail_to_old_stagiaires')

    def check_box_selection_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        # Récup de l'id pour MAJ de l'item
        result = anvil.server.call("maj_selection",self.item,self.check_box_selection.checked)
        if result is not True:
            alert("Erreur de MAJ")
