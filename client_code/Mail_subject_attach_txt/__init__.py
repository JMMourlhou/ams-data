from ._anvil_designer import Mail_subject_attach_txtTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .Mail_model import Mail_model


class Mail_subject_attach_txt(Mail_subject_attach_txtTemplate):
    def __init__(self, emails_liste=["jmmourlhou@gmail.com"], ref_model = "", **properties): 
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        open_form("Mail_subject_attach_txt",emails_liste,ref_model)
        # Any code you write here will run before the form opens.
        self.mode_creation = False
        # emails_liste liste des mails
        # ref_model contient lea ref du modele de mail si vient de qcm ou formul satisf ou recherche etc...du permet de court circuiter la drop down du choix du modèle 
        
        self.ref_model = ref_model
        self.emails_liste = emails_liste # liste des mails
        print('ref_model: ',self.ref_model)
        
        
        
        
        self.label_emails_liste.text = emails_liste
        # import anvil.js    # pour screen size
        from anvil.js import window  # to gain access to the window object

        global screen_size
        screen_size = window.innerWidth

        # INITIALISATION Drop down   drop_down_type_mails
        self.drop_down_type_mails.items = [(r['type_mail'], r) for r in app_tables.mail_type.search()]
        
        # ref_model en init contient la ref du modele si vient de qcm ou formul etc...du permet de court circuiter la drop down du choix du modèle 
        if self.ref_model != "":
            # lecture du modele pour court circuiter la drop down du choix du modèle 
            type_mail_row = app_tables.mail_type.get(ref=self.ref_model)
            print("ok: ", type_mail_row['type_mail'])
            if type_mail_row:
                self.drop_down_type_mails.selected_value = type_mail_row
                self.drop_down_type_mails_change(type_mail_row)
    
       

    def drop_down_type_mails_change(self, type_mail_row=None, **event_args): 
        #si j'ai court circuiter le dropdown (car vient de qcm, form satisf, recherche stag, ...) 
        if type_mail_row is None:
            type_mail_row = self.drop_down_type_mails.selected_value
            #self.ref_model = type_mail_row['ref']
        else:
            alert("vient de module externe avec ce type:", type_mail_row['ref'])
            
        liste_mails =  app_tables.mail_templates.search(
                                                        tables.order_by("mail_subject", ascending=True),
                                                        type = type_mail_row
                                                        )
        self.repeating_panel_1.visible = True
        self.repeating_panel_1.items = liste_mails
        #for mail in liste_mails:
        #    self.column_panel_content.add_component(Mail_model(mail['mail_subject'], mail['mail_text'], mail.get_id(), self.ref_model, self.emails_liste))


        self.button_attachments.visible = True
        self.button_sending.visible = True
        self.button_new.visible = True
        #self.button_modif.visible = False

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99) 

    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.mode_creation is True:  # Création du modèle
            if not self.drop_down_type_mails.selected_value:
                alert("Sélectionnez le type de modèle")
                return
            #r=alert("Enregistrer ce modèle ?",buttons=[("oui",True),("non",False)])
            #if r :   # Oui               
            result = anvil.server.call('add_mail_model', self.drop_down_type_mails.selected_value,self.text_box_subject_detail.text, self.text_area_text_detail.text)
        else:   # Modif du modèle
            #r=alert("Modifier ce modèle ?",buttons=[("oui",True),("non",False)])
            #if r :   # Oui               
            result = anvil.server.call('modify_mail_model',self.label_id.text,self.text_box_subject_detail.text, self.text_area_text_detail.text)
        if not result:
            if self.mode_creation is True:  # Création du modèle
                alert("Modèle de mail non créé")
            else:
                alert("Modèle de mail non modifié")
        else:
            if self.mode_creation is True:  # Création du modèle
                alert("Modèle de mail créé")
            else:
                alert("Modèle de mail modifié")
        self.column_panel_content.clear()       
        self.drop_down_type_mails_change()
        self.column_panel_detail.visible = False
        self.mode_creation = False
        
    def button_attachments_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def button_sending_click(self, **event_args):
        """This method is called when the button is clicked"""
        result = anvil.server.call("send_mail",self.emails_liste, self.text_box_subject_detail.text, self.text_area_text_detail.text)
        if result:
            alert("mail envoyé")

    def text_box_subject_detail_change(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.button_modif.visible = True
        
    def text_area_text_detail_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.text_box_subject_detail_change()

    def button_new_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        self.column_panel_detail.visible = True
        self.mode_creation = True
        self.text_box_subject_detail.text = ""
        self.text_area_text_detail.text = ""
        
        