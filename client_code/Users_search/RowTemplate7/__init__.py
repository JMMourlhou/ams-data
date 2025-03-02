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
        self.sov_old_conf_mail = self.item['confirmed_email']
        self.sov_old_enabled = self.item['enabled']

    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
       
        r=alert("Voulez-vous vraiment modifier cette ligne ?",buttons=[("oui",True),("non",False)])
        if r :   # oui
            # 1 modif ds les lieux stages 
            alert(self.check_box_conf_mail.ckecked)
            bool2 = self.check_box_cpt_enabled.checked
            result=anvil.server.call('modify_users_from_parameters', self.item, bool1, bool2)
            if result is not True:
                alert("ERREUR, Modification non effectuée !")
                return
            alert("Modification effectuée !")
        else:   # non
            self.check_box_conf_mail.checked = sov_old_conf_mail
            self.check_box_cpt_enabled.checked = sov_old_enabled
            self.button_modif.visible = False
        self.button_modif.visible = False

    def check_box_conf_mail_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.visible = True



  

    
        
        
        