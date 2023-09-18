from ._anvil_designer import QcmTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Qcm(QcmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.repeating_panel_1.items = app_tables.qcm.search()
            #tables.order_by("name", ascending=True),
            #stage=stage_row
        #)

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def button_validation_copy_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

