from ._anvil_designer import Mail_modelTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class Mail_model(Mail_modelTemplate):
    def __init__(self, subject, text, id, ref_model, emails_liste, **properties):   # passer  ref_model et emails liste permet la réouverture de mail_subject en del d'un modèle 
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.ref_model = ref_model
        self.emails_liste = emails_liste
        if  self.ref_model == "":
            self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
            print("provenance: ", self.f)
        else: 
            
            print("Provenace autre form peut pas utiliser get_open_form(),  ref_model: ", ref_model)
            #for elmt in self.parent.get_components(:
            #    print(elmt.name)
        
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
        #self.f.column_panel_content.clear()
        # autre facon de récupérer la forme mere et d'effacer le col panel content
        from .Mail_subject_attach_txt import Mail_subject_attach_txt
        open_form('Mail_subject_attach_txt', self.emails_liste, self.ref_model)
        #Mail_subject_attach_txt.column_panel_content.clear() 
        #Mail_subject_attach_txt.drop_down_type_mails_change() #retour ds la forme mère et réaffichage
        
    def text_box_subject_focus(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        # récupération de la forme mère 
        
        # si provenance de mail, provenance = "" alors je peux utiliser 
        
        Mail_subject_attach_txt.column_panel_detail.visible = True
        Mail_subject_attach_txt.text_box_subject_detail.text = self.text_box_subject.text
        Mail_subject_attach_txt.text_area_text_detail.text = self.text_area_text.text
        Mail_subject_attach_txt.label_id.text =  self.text_box_subject.tag
        Mail_subject_attach_txt.column_panel_content.clear()
        Mail_subject_attach_txt.column_panel_content.visible = False

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
            from .Mail_subject_attach_txt import Mail_subject_attach_txt
            result = anvil.server.call("send_mail",Mail_subject_attach_txt.label_emails_liste, row_model['mail_subject'], row_model['mail_text'])
            if result:
                alert("mail envoyé")
        else:
            alert("Modèle non trouvé")
            

   
