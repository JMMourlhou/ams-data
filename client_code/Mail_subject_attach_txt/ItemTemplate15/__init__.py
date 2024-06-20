from ._anvil_designer import ItemTemplate15Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Mail_subject_attach_txt
from ..._Constant_parameters_public_ok import emails_liste   # liste des emails  
from ..._Constant_parameters_public_ok import ref_model   # type de modèles de mail 

class ItemTemplate15(ItemTemplate15Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
         # Any code you write here will run before the form opens.
        
        self.f = Mail_subject_attach_txt(emails_liste,ref_model, 2)
        #self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("form mère récupérable: ", self.f)
       
        self.text_box_subject.text = self.item['mail_subject']
        self.text_box_subject.tag.id = self.item.get_id() # je sauve l'id du modele mail row 
        self.text_area_text.text = self.item['mail_text']

        # j'affiche bt envoi de mail sila liste de mail non vide
        if self.f.label_emails_liste.text != "":
            self.button_sending.visible = True

    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous enlever ce modèle de mail ?",buttons=[("oui",True),("non",False)])
        if r :   # Oui               
            anvil.server.call('del_mails', self.text_box_subject.tag.id) 
            
        # Je lis la liste d'emails et le ref du modèle pour réaffichage    
        emails_liste = self.f.label_emails_liste.text
        ref_model = self.f.label_ref_model.text
        open_form('Mail_subject_attach_txt', emails_liste, ref_model) # réouverture pour réaffichage sans le modèle enlevé 

    def text_box_subject_focus(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        # récupération de la forme mère par  self.f = get_open_form() en init
        
        self.f.column_panel_detail.visible = True # montre la form création/modif de modèle
        self.f.repeating_panel_1.visible = False # cache les modèles 
        self.f.label_id.text =  self.text_box_subject.tag # récupère l'id du modele mail row (pour la modif en serveur)
        
        self.f.text_box_subject_detail.text = self.text_box_subject.text
        self.f.text_area_text_detail.text = self.text_area_text.text
       

    def text_area_text_focus(self, **event_args):
        """This method is called when the text area gets focus"""
        self.text_box_subject_focus()

    def button_sending_click(self, **event_args):
        """This method is called when the button is clicked"""
        id = self.text_box_subject.tag.id # récup de l'id du modèle cliqué par son TAG      self.text_box_subject.tag 
        # lecture du modèle
        row_model = app_tables.mail_templates.get_by_id(id)
        if row_model:
            # récupération de la forme mère self.f.emails_liste       (voir init       self.f = get_open_form() )
            result = anvil.server.call("send_mail", self.f.label_emails_liste, row_model['mail_subject'], row_model['mail_text'])
        if result:
                alert("mail envoyé")
        else:
            alert("Modèle non trouvé")

