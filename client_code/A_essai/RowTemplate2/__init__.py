from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ...common import publisher



class RowTemplate2(RowTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        test= publisher.subscribe(
            
            channel="general", subscriber=self, handler=self.general_messages_handler,
            with_logging=True
        )
        self.init_components(**properties)
        
        # Any code you write here will run before the form opens.
        self.button_1.text = self.item['nom']
        #global msg
        #self.button_2.text = msg
        
    def general_messages_handler(self, message):
        #if message.title == "Hello world":
        print(message.content)
        print(message.title)
