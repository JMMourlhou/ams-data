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
#import signup_for_AMS_Data
#from signup_for_AMS_Data.Form1 import Form1

class Main(MainTemplate):
    def __init__(self, nb=1, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.nb=nb
        """ Incrémentation de nb """
        self.nb = self.nb + 1

        """ cas 2: soit ouverture de l'app """
        """        ou retour par URL suite à SignIn ou PW reset"""
        if self.nb == 2:   
            h={}
            h = anvil.get_url_hash()
            #print(f"h ds init: {h}")
            if len(h)!=0 :  # a URL has openned this app
                #self.link_login.visible = True
                #alert(h)
                url_time_str=""
                url_time=h["t"]
                url_time_over=French_zone.time_over(url_time)
                if not url_time_over: 
                    calling_signing_up.calling_form1(h)
                else:
                    alert("Ce lien n'est plus actif")


    
    def button_se_connecter_click(self, **event_args):
        """This method is called when the button is clicked"""
        """Will call the EXTERNAL MODULE DEPENDACY when the link is clicked"""
                
        import sign_up_for_AMS_Data
        from sign_up_for_AMS_Data.Form1 import Form1
        
        self.content_panel.clear()
        self.content_panel.add_component(Form1(), full_width_row=True)


