from ._anvil_designer import Mail_subject_attach_txtTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Mail_subject_attach_txt(Mail_subject_attach_txtTemplate):
    def __init__(self, **properties): 
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

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
        #self.column_panel_headers.visible = True
        self.repeating_panel_1.items = liste_mails
        self.button_new.visible = False
        

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99) 
