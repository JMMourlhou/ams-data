from ._anvil_designer import ItemTemplate16Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

class ItemTemplate16(ItemTemplate16Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        #self.image_doc.source = self.item[0]        # 1er élément de l'item, le media file choisit pour téléchargement (si pdf, le transfomer en jpg)
        self.label_address_doc.text = self.item[1]  # 2eme élément de l'item, le nom du fichier en txt
        
        # Type de fichier en attachement ?
        path_parent, file_name, file_extension = anvil.server.call('path_info', str(self.item[0].name))
        if file_extension == ".pdf":
            liste_images = anvil.server.call('display_pdf', self.item[0]) 
        
            #extraction 1ere image de la liste (il peut y avoir plusieurs pages)
            print("nb d'images jpg crées par pdf_into_jpg:", len(liste_images))
            file = liste_images[0]
            self.image_doc.source =  file
        else:
            self.image_doc.source = self.item[0]        # 1er élément de l'item, le media file choisit pour téléchargement (si pdf, le transfomer en jpg)
        
    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("form mère atteingnable (en modif): ", self.f) 
        
        self.f.list_attach = [] # réinitialisation de la liste pour le repeating panel
        del  self.f.dico_attachements[self.item[0]]
        
        for clef, valeur in self.f.dico_attachements.items():
                self.f.list_attach.append((clef,valeur))  # transformation dict en liste pour le repeating panel
        
        self.f.repeating_panel_2.items = self.f.list_attach
