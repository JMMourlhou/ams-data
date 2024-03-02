from ._anvil_designer import QCM_ResultsTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global screen_size
screen_size = window.innerWidth

class QCM_Results(QCM_ResultsTemplate):
    def __init__(self, num_stage, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        #lecture des résultats
        liste_results = app_tables.qcm_result.search(tables.order_by("name", ascending=True),
                                                                            stage=stage_row
                                                                           )
        if liste_results:                      # des stagiaires sont déjà inscrits ds stage
            self.repeating_panel_1.items = liste_results