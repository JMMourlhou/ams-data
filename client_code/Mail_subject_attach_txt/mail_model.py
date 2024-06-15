from ._anvil_designer import mail_modelTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class mail_model(mail_modelTemplate):
    def __init__(self, subject, text, id, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        
        self.text_box_subject.text = subject
        self.text_box_subject.tag = id # je sauve l'id du modele mail row 
        self.text_area_text.text = text

        
    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        alert(" à faire, annuler ce modèle")

    def text_box_subject_focus(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        f = get_open_form()
        f.column_panel_detail.visible = True
        f.text_box_subject_detail.text = self.text_box_subject.text
        f.text_area_text_detail.text = self.text_area_text.text
        f.label_id.text =  self.text_box_subject.tag
        f.column_panel_content.clear()
        f.column_panel_content.visible = False

    def text_area_text_focus(self, **event_args):
        """This method is called when the text area gets focus"""
        self.text_box_subject_focus()

   
