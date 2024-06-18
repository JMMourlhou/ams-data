from ._anvil_designer import mail_modelTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class mail_model(mail_modelTemplate):
    def __init__(self, subject, text, id, **properties):   
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("Form originale :",  self.f)
        self.text_box_subject.text = subject
        self.text_box_subject.tag = id # je sauve l'id du modele mail row 
        self.text_area_text.text = text

        
    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous enlever ce modèle de mail ?",buttons=[("oui",True),("non",False)])
        if r :   # Oui               
            result = anvil.server.call('del_mails', self.text_box_subject.tag) 
            """
            if not result:
                alert("Mail type non enlevé")
            else:
                alert("Ce modèle de mail a été enlevé")  
            """
        self.f.column_panel_content.clear()
        self.f.drop_down_type_mails_change() #retour ds la forme mère et réaffichage
        
    def text_box_subject_focus(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        # récupération de la forme mère self.f (voir init       self.f = get_open_form() )
        self.f.column_panel_detail.visible = True
        self.f.text_box_subject_detail.text = self.text_box_subject.text
        self.f.text_area_text_detail.text = self.text_area_text.text
        self.f.label_id.text =  self.text_box_subject.tag
        self.f.column_panel_content.clear()
        self.f.column_panel_content.visible = False

    def text_area_text_focus(self, **event_args):
        """This method is called when the text area gets focus"""
        self.text_box_subject_focus()

    def button_sending_click(self, **event_args):
        """This method is called when the button is clicked"""
        id = self.text_box_subject.tag # récup de l'id du modèle cliqué par son TAG      self.text_box_subject.tag 
        # lecture du modèle
        row_model = app_tables.mail_templates.get_by_id(id)
        if row_model:
            # récupération de la forme mère self.f.emails_liste       (voir init       self.f = get_open_form() )
            result = anvil.server.call("send_mail",self.f.emails_liste, row_model['mail_subject'], row_model['mail_text'])
            if result:
                alert("mail envoyé")
        else:
            alert("Modèle non trouvé")
            

   
