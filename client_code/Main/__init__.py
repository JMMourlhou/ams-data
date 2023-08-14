from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import French_zone
from .. import calling_signing_up
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from ..Saisie_info_de_base import Saisie_info_de_base
from ..Stage_creation import Stage_creation


class Main(MainTemplate):
    def __init__(self, nb=1, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        print("nb: ", nb)
        self.bt_se_deconnecter.visible = False
        self.bt_user_mail.text = "Déconnecté"
        self.nb=nb
        """ Incrémentation de nb """
        self.nb = self.nb + 1

        """ cas 2: soit ouverture de l'app """
        """        ou retour par URL suite à SignIn ou PW reset"""
        if self.nb == 2:   
            h={}
            h = anvil.get_url_hash()
            print(f"h ds init d'AMS_Data: {h}")
            if len(h)!=0 :  # a URL has openned this app
                #self.link_login.visible = True
                #alert(h)
                url_time_str=""
                url_time=h["t"]
                url_time_over=French_zone.time_over(url_time)
                if not url_time_over: 
                    calling_signing_up.calling_form1(h)
                else:
                    alert("Ce lien n'est plus actif, renvoyer un mail")
                    
        if self.nb == 99: #suite à fermeture / saisie fiche renseignements users
            self.content_panel.clear()
            
            
        user=anvil.users.get_user()
        if not user:   # no user: go to insription/connection
            self.content_panel.clear()
        else:   #user connected but no data completed
            if nb != 99: # retour d'annulation en saisie de la fiche de renseignements de base
                if user["prenom"] == None :   # fiche vide  
                    self.content_panel.clear()
                    self.content_panel.add_component(Saisie_info_de_base(), full_width_row=True)
                
        
        # handling buttons display        
        self.display_bt_mail()
        self.display_admin_or_other_buttons()

    """ ****************************************************************************"""
    def bt_se_deconnecter_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.content_panel.clear()
        anvil.users.logout()       #logging out the user
        user= None
        self.display_bt_mail()
        self.display_admin_or_other_buttons()
            
    def button_se_connecter_click(self, **event_args):
        """This method is called when the button is clicked"""
        """Will call the EXTERNAL MODULE DEPENDACY when the link is clicked"""
                
        import sign_up_for_AMS_Data
        from sign_up_for_AMS_Data.Form1 import Form1
        
        self.content_panel.clear()
        self.content_panel.add_component(Form1(), full_width_row=True)

    def display_bt_mail(self, **event_args):
        user=anvil.users.get_user()
        if user:
             self.bt_user_mail.text = user['email']
             self.bt_se_connecter.visible = False
             self.bt_se_deconnecter.visible = True
        else:
             self.bt_user_mail.text = "Déconnecté"
             self.bt_se_deconnecter.visible = False 
             self.bt_se_connecter.visible = True

    def display_admin_or_other_buttons(self, **event_args):
        user=anvil.users.get_user()
        if user:
            if user["admin"] == True:  # Administrator
                self.column_panel_admin.visible = True
                self.column_panel_others.visible = True
            else:                      # no admin
                self.column_panel_admin.visible = False
                self.column_panel_others.visible = True
        else:                          # deconnected
            self.column_panel_admin.visible = False
            self.column_panel_others.visible = False
    
    def button_renseignements_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.content_panel.clear()
        self.content_panel.add_component(Saisie_info_de_base(), full_width_row=True)

    def button_stage_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.content_panel.clear()
        self.content_panel.add_component(Stage_creation(), full_width_row=True)
           
            