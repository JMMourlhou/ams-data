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
from ..Visu_stages import Visu_stages
from ..Visu_stages.ItemTemplate1 import ItemTemplate1
from anvil import open_form

class Main(MainTemplate):
    def __init__(self, nb=1, stage_nb=0, **properties):
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
            """ get_url_hash() gets the decoded hash (the part after the ‘#’ character) of the URL used to open this app.

                If the first character of the hash is a question mark (e.g., https://myapp.anvil.app/#?a=foo&b=bar),
                it will be interpreted as query-string-type parameters and returned as a dictionary
                (e.g., {'a': 'foo', 'b': 'bar'} ).

                get_url_hash() is available in Form code only.

                I don’t use extra arguments on forms loaded by the routing module.
                Using extra arguments kind of defeats the purpose of using the routing module.

                I pass all the arguments on the URL, then I use self.url_dict['items'].
                
                """
            
            h={}
            h = anvil.get_url_hash()
            print(f"h ds init d'AMS_Data: {h}")
            if len(h)!=0 :  # a URL has openned this app
                # lien actif < à 10 min ?
                url_time_str=""
                url_time=h["t"]
                url_time_over=French_zone.time_over(url_time)
                if url_time_over: 
                    alert("Ce lien n'est plus actif !")
                    
                # stage number in URL's Hash ? (le user vient-il de flacher le Qr code?)
                try:
                    num_stage=h["stage"]
                    if len(num_stage) != 0 :        #oui le user vient de flacher le Qr code
                        alert("réception en création de stage " + str(num_stage))
                        calling_signing_up.calling_form1(h, num_stage)  #c'est sign in, je passe num stage
                except:
                        calling_signing_up.calling_form1(h)  # pas url venant du qr code, je ne passe pas le num stage
        
        user=anvil.users.get_user()
        if not user:  
            self.content_panel.clear()
        else:
            # renseignements du user pour savoir si on est en 1ere utilisation (on n'affiche pas liste stages)
            if user['prenom'] == "":
                self.liste_stages.visible = False
                self.button_renseignements_click()
        
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
    
    def button_renseignements_click(self, num_stage=0,**event_args):
        """This method is called when the button is clicked"""
        alert("bt renseignements click" + str(num_stage))
        self.content_panel.clear()
        self.button_renseignements.visible = False
        self.content_panel.add_component(Saisie_info_de_base(), full_width_row=True)
        
        
    def button_stage_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.content_panel.clear()
        self.content_panel.add_component(Stage_creation(), full_width_row=True)

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.content_panel.clear()
        self.content_panel.add_component(Visu_stages(), full_width_row=True)

           
            