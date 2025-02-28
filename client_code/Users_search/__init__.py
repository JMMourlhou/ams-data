from ._anvil_designer import Users_searchTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Users_search(Users_searchTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.data_grid_1.visible = True
        # Any code you write here will run before the form opens.
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form("Main", 99)

    def text_box_role_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self.text_box_nom.text = ""
        self.text_box_prenom.text = ""
        self.text_box_mail.text = ""
        self.check_box_confirmed_mail.checked = False
        
        critere = self.text_box_role.text + "%"            #  wildcard search on date
        liste = app_tables.users.search(tables.order_by("role", ascending=True),
                                        role=q.ilike(critere),
                                                )
        self.repeating_panel_1.items=liste

    def text_box_nom_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self.text_box_role.text = ""
        self.text_box_prenom.text = ""
        self.text_box_mail.text = ""
        self.check_box_confirmed_mail.checked = False
        
        critere = self.text_box_nom.text + "%"            #  wildcard search on date
        liste = app_tables.users.search(tables.order_by("nom", ascending=True),
                                        nom=q.ilike(critere)
                                                )
        self.repeating_panel_1.items=liste

    def text_box_prenom_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self.text_box_role.text = ""
        self.text_box_nom.text = ""
        self.text_box_mail.text = ""
        self.check_box_confirmed_mail.checked = False
        
        critere = self.text_box_prenom.text + "%"            #  wildcard search on date
        liste = app_tables.users.search(tables.order_by("prenom", ascending=True),
                                        prenom=q.ilike(critere)
                                                )
        self.repeating_panel_1.items=liste

    def text_box_mail_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self.text_box_role.text = ""
        self.text_box_nom.text = ""
        self.text_box_prenom.text = ""
        self.check_box_confirmed_mail.checked = False
        
        critere = self.text_box_mail.text + "%"            #  wildcard search on date
        liste = app_tables.users.search(tables.order_by("email", ascending=True),
                                        email=q.ilike(critere)
                                                )
        self.repeating_panel_1.items=liste   

    def check_box_confirmed_mail_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.text_box_role.text = ""
        self.text_box_nom.text = ""
        self.text_box_prenom.text = ""
        self.text_box_mail.text = ""
        if self.check_box_confirmed_mail.checked is True:
            critere = None            #  wildcard search on date
            liste = app_tables.users.search(tables.order_by("nom", ascending=True),
                                            confirmed_email=critere
                                                    )
            self.repeating_panel_1.items=liste
        else:
            self.text_box_nom_focus()
   