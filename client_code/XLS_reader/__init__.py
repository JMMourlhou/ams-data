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
        #xls_file = "Diplômés PSE Extranet FNMNS 2016-2020.csv"
        

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        result,nb = anvil.server.call('xls_file_reader', file)
        msg = f"Fin de fichiers, {nb} mails ajoutés ds le fichier des anciens stagiaires"
        alert(msg)

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)
        
        
        