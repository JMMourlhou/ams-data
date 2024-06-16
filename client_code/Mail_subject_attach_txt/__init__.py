from ._anvil_designer import Mail_subject_attach_txtTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .mail_model import mail_model   # la forme à ajouter par add component

class Mail_subject_attach_txt(Mail_subject_attach_txtTemplate):
    def __init__(self, emails_liste=["jmmourlhou@gmail.com"], **properties):    # emails_liste liste des mails
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.mode_creation = False
        self.emails_liste = emails_liste # liste des mails
        # import anvil.js    # pour screen size
        from anvil.js import window  # to gain access to the window object

        global screen_size
        screen_size = window.innerWidth

        # INITIALISATION Drop down   drop_down_type_mails
        self.drop_down_type_mails.items = [(r['type_mail'], r) for r in app_tables.mail_type.search()]
       

    def drop_down_type_mails_change(self, **event_args):
        type_mail_row = self.drop_down_type_mails.selected_value
        liste_mails =  app_tables.mail_templates.search(
                                                        tables.order_by("mail_subject", ascending=True),
                                                        type = type_mail_row
                                                        )
        self.column_panel_content.visible = True
        self.column_panel_content.clear()   
        for mail in liste_mails:
            self.column_panel_content.add_component(mail_model(mail['mail_subject'], mail['mail_text'], mail.get_id()))
            #self.column_panel_content.raise_event_on_children("x-click", **event_args)

        self.button_attachments.visible = True
        self.button_sending.visible = True
        self.button_new.visible = True
        self.button_modif.visible = False

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
        
        