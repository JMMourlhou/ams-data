from ._anvil_designer import ItemTemplate15Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate15(ItemTemplate15Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_box_subject.text = self.item['mail_subject']
        self.text_box_subject.tag = self.item.get_id()
        self.text_area_text.text = self.item['mail_text']
        self.text_area_text.tag = self.item.get_id()

    def text_box_subject_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.row=app_tables.mail_templates.get_by_id(self.text_box_subject.tag)
        self.outlined_card_detail.visible = True
        self.text_box_subject_detail = self.text_box_subject.text
        self.text_area_text_detail = self.text_area_text.text

        self.link_1.visible = False

    def text_box_subject_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.row=app_tables.mail_templates.get_by_id(self.text_box_subject.tag)
        self.outlined_card_detail.visible = True
        self.text_box_subject_detail.text = self.text_box_subject.text
        self.text_area_text_detail.text = self.text_area_text.text

        self.column_panel_2.visible = False

    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    

    def text_area_text_detail_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.button_modif.visible = True

    def button_del_click(self, **event_args):   # Effacement du modèle de mail
        """This method is called when the button is clicked"""
        pass

    

