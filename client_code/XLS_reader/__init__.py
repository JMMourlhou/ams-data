from ._anvil_designer import XLS_readerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class XLS_reader(XLS_readerTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # Lecture de la variable globale "code_app1" ds table variables_globales
        xls_file = "Diplômés PSE Extranet FNMNS 2016-2020.csv"
        mail1 = anvil.server.call('xls_file_reader', xls_file)
        alert(mail1)
        
        