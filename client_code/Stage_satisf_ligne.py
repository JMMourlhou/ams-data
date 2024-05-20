from ._anvil_designer import Stage_satisf_ligneTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Stage_satisf_ligne(Stage_satisf_ligneTemplate):
    def __init__(self, question, r0,r1,r2,r3,r4,r5, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.label_question.text = question
        self.label_0.text = r0
        self.label_1.text = r1
        self.label_2.text = r2
        self.label_3.text = r3
        self.label_4.text = r4
        self.label_5.text = r5
        