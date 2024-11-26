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
        self.spacer_1.height = space(self.item['q1'])
        self.label_2.text = self.display(self.item['pourcent_2'])
        self.label_12.text = self.item['q2']
        self.label_3.text = self.display(self.item['pourcent_3'])
        self.label_13.text = self.item['q3']
        self.label_4.text = self.display(self.item['pourcent_4'])
        self.label_14.text = self.item['q4']
        self.label_5.text = self.display(self.item['pourcent_5'])
        self.label_15.text = self.item['q5']
        self.label_6.text = self.display(self.item['pourcent_6'])
        self.label_16.text = self.item['q6']
        self.label_7.text = self.display(self.item['pourcent_7'])
        self.label_17.text = self.item['q7']
        self.label_8.text = self.display(self.item['pourcent_8'])
        self.label_18.text = self.item['q8']
        self.label_9.text = self.display(self.item['pourcent_9'])
        self.label_19.text = self.item['q9']
        self.label_10.text = self.display(self.item['pourcent_10'])
        self.label_20.text = self.item['q10']
        
    def display(self, nb, **properties):
        nb1=round(nb)
        print(nb1)
        text = str(nb1)+" %"
        print(text)
        return text

    def space_heihgt(self, question):