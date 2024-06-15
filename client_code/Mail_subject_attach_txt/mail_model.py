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
    def __init__(self, subject, text, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_box_subject.text = subject
        self.text_area_text.text = text

    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
