from ._anvil_designer import videTemplate
from anvil import *
from anvil_extras.PageBreak import PageBreak


# AFFICHAGE vide qd le tuteur a plusieurs stgiaires pour le formulaire de suivi
# APPELE PAR LA FORM 'S.ItemTemplate17' par add component:


class vide(videTemplate):
    def __init__(self, nom_tuteur, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.label_1.text = (f"Autre stagiaire de {nom_tuteur} :")
    

    def form_show(self, **event_args):
        self.add_component(PageBreak())  # si en création de pdf, je saute une page ts les 25 images, NE FONCTIONNE PAS !!!
