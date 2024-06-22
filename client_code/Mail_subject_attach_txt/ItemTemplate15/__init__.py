from ._anvil_designer import ItemTemplate15Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Mail_subject_attach_txt

class ItemTemplate15(ItemTemplate15Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
         # Any code you write here will run before the form opens.
        self.text_box_subject.text = self.item['mail_subject']
        self.text_box_subject.tag.id = self.item.get_id() # je sauve l'id du modele mail row 
        self.text_area_text.text = self.item['mail_text']

        # j'affiche bt envoi de mail 
        # récupération de la forme mère par  self.f = get_open_form() en init 
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("form mère atteingnable (en visu): ", self.f) 
        try: # ne fonctionera que si envoi par option mail du menu
            if self.f.label_emails_liste == []:
                self.f.button_sending.visible = False # cache envoi de mail ds forme mere
                self.button_sending = False           # cache envoi de mail ds cette forme
        except:
            pass

    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous enlever ce modèle de mail ?",buttons=[("oui",True),("non",False)])
        if r :   # Oui               
            anvil.server.call('del_mails', self.text_box_subject.tag.id) 
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("form mère récupérable (delete): ", self.f)   
        # Je lis la liste d'emails et le ref du modèle pour réaffichage    
        emails_liste = self.f.label_emails_liste.text
        ref_model = self.f.label_ref_model.text
        open_form('Mail_subject_attach_txt', emails_liste, ref_model, 2) # réouverture pour réaffichage sans le modèle enlevé 

    def text_box_subject_focus(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        # Appui sur objet ou texte du modèle pour le modifier
        
        # récupération de la forme mère par  self.f = get_open_form() en init
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("form mère atteingnable (en modif): ", self.f) 

        # si pas d'email liste, provenance mail du menu principal, je ne permets pas d'envoi de mail ou attachements
        
        if self.f.label_emails_liste.text == []:
            self.f.button_sending.visible = False # cache envoi de mail ds forme mere
            self.f.button_attachments.visible = False
            
        self.f.button_annuler.visible = False
        self.f.button_new.visible = False
        self.f.column_panel_detail.visible = True # montre la form création/modif de modèle
        self.f.repeating_panel_1.visible = False # cache les modèles 
        
        self.f.label_id.text =  self.item.get_id() # récupère l'id du modele mail row (pour la modif en serveur)
        self.f.text_box_subject_detail.text = self.text_box_subject.text
        self.f.text_area_text_detail.text = self.text_area_text.text
       

    def text_area_text_focus(self, **event_args):
        """This method is called when the text area gets focus"""
        self.text_box_subject_focus()

    def button_sending_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Envoi du mailing ?",buttons=[("oui",True),("non",False)])
        if r :   # Oui
    
            id = self.text_box_subject.tag.id # récup de l'id du modèle cliqué par son TAG      self.text_box_subject.tag 
            # lecture du modèle
            row_model = app_tables.mail_templates.get_by_id(id)
            if row_model:
                # récupération de la forme mère self.f.emails_liste       (voir init       self.f = get_open_form() )
                self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
                print("email liste (sending mail): ", self.f.label_emails_liste.text) 
                result = anvil.server.call("send_mail", self.f.label_emails_liste.text, row_model['mail_subject'], row_model['mail_text'])
            if result:
                    if result:
                        msg = "Mail envoyé ! "
                        n=Notification(msg,timeout=1)
                        n.show()
            else:
                alert("Modèle non trouvé")



