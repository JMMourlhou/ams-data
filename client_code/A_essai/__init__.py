from ._anvil_designer import A_essaiTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..common import publisher


class A_essai(A_essaiTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        publisher.publish(channel="general", title="Hello world", content="contenu")
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # j'affiche tous les stagiaires
        self.repeating_panel_1.items = app_tables.users.search(
                tables.order_by("nom", ascending=True),
                admin =q.not_(True)    # on n'affiche pas l'admin !
                )