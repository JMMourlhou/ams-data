from ._anvil_designer import ItemTemplate20Template
from anvil import *
import anvil.server

import anvil.users
import anvil.tables as tables

from anvil.tables import app_tables


class ItemTemplate20(ItemTemplate20Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.label_nom.text = self.item['nom']
        self.label_1.text = self.display(self.item['pourcent_1'])
        self.label_11.text = self.item['q1']
        self.label_2.text = self.display(self.item['pourcent_2'])
        self.label_3.text = self.display(self.item['pourcent_3'])
        self.label_4.text = self.display(self.item['pourcent_4'])
        self.label_5.text = self.display(self.item['pourcent_5'])
        self.label_6.text = self.display(self.item['pourcent_6'])
        self.label_7.text = self.display(self.item['pourcent_7'])
        self.label_8.text = self.display(self.item['pourcent_8'])
        self.label_9.text = self.display(self.item['pourcent_9'])
        self.label_10.text = self.display(self.item['pourcent_10'])

    def display(self, nb, **properties):
        text = str(nb)
        lg = len(text)
        
        if lg == 3:   # 100 --> 100,0 
            text = text + ",0"
        if lg == 2 or lg ==1:   # 25 --> 25,00
            text = text + ",00"
        if lg > 4 :
            
        return text