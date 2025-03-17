from ._anvil_designer import ItemTemplate29Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate29(ItemTemplate29Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        #                              0             1              2                 3
        #                              qcm_exam_row    , qcm enfant nb, qcm_destination,  nb de questions
        self.button_qcm_enfant.text = str(self.item[1]) + " - " + self.item[2] 
        nb_questions_qcm_enfant = 
        self.text_box_nb_questions.text = self.item[3]
        