from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate7(RowTemplate7Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_role.text = self.item['role']
        self.button_nom.text = self.item['nom']
        self.button_prenom.text = self.item['prenom']
        self.button_email.text = self.item['email']
        self.check_box_conf_mail.checked = self.item['confirmed_email']
        self.check_box_cpt_enabled.checked = self.item['enabled']

    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous vraiment modifier cette ligne ?",buttons=[("oui",True),("non",False)])
        sov_old_conf_mail = self.check_box_conf_mail.checked
        sov_old_enabled = self.check_box_cpt_enabled.checked
        if r :   # oui
            # 1 modif ds les lieux stages 
            anvil.server.call('modify_users_from_parameters',self.item(),self.check_box_conf_mail.ckecked,self.check_box_cpt_enabled.checked)
            if result is not True:
                alert("ERREUR, Modification non effectuée !")
                return
            alert("Modification effectuée !")
            
        else:   # non
            self.text_box_1.text = sov_old_adresse
            self.text_box_2.text = sov_old_lieu
        self.button_modif.visible = False
        
        
        