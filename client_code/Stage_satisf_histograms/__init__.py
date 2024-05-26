from ._anvil_designer import Stage_satisf_histogramsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server

from plotly import graph_objects as go
from anvil_extras.PageBreak import PageBreak
global    cpt # Compte le nb d'images visualisées pour le page Break
cpt = 10

# AFFICHAGE DES RESULTATS d pour 1 question fermée du formulaire de satisfaction
# APPELE PAR LA FORM 'STAGE_SATISF_Statistics' par add component: 
#   (  self.column_panel_content.add_component(Stage_satisf_histograms(qt,r0,r1,r2,r3,r4,r5)) )


class Stage_satisf_histograms(Stage_satisf_histogramsTemplate):
    def __init__(self,qt,r0,r1,r2,r3,r4,r5, **properties):  
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        data = [r0,r1,r2,r3,r4,r5]     # axe des y
        listx = [0,1,2,3,4,5]          # axe des x
        # texte à afficher ds les barres
        t0 = f"{r0} rép."
        t1 = f"{r1} rép."
        t2 = f"{r2} rép."
        t3 = f"{r3} rép."
        t4 = f"{r4} rép."
        t5 = f"{r5} rép."
        
        # Plot some data
        self.plot_1.data = [
            go.Bar(x=listx,
                   y=data,
                   #marker=dict(color="rgb(16, 32, 77)" ),    # couleur de toutes les barres 
                   marker=dict(color=("red", "orangered","orange","greenyellow","lime","green")),     # couleurs css de chaque barre ( https://lucidar.me/fr/web-dev/css-color-list/ )
                   text=[t0,t1,t2,t3,t4,t5])                 # texte ds les barres
        ]

        # Configure the plot layout
        titre = qt
        self.plot_1.layout = {
                #'title': titre,    # titre du graphique
                'title':   {
                        'text' : titre,
                          },
                'title_font_color' : "darkblue",
                'title_font_size'  : 16,
                'title_font_family'     : "Arial, bold",
                'xaxis':  {
                    'title': "(0:Très insatisfait à 5:Très satisfait)",
                            },

                "yaxis": {
                    "title": 'Nb de réponses',
                    "visible": False,  # Montre l'axe y et son titre  !!
                    'tickmode': 1,           # de 1 en 1
                        },
                "plot_bgcolor": "white",  # Couleur de fond personnalisée
                "showlegend": False,  # True pour montrer la légende (false par défaut voir l'init)

                        }
        
    def form_show(self, **event_args):
        """This method is called when the Image is shown on the screen"""
        global cpt  # Cpt le nb d'images imprimées
        cpt -= 1
        print("compteur :",cpt)
        if cpt == 2 or cpt == 5 or cpt == 8 :   
           print("Page Break", cpt)
           self.add_component(PageBreak())      # si en création de pdf, je saute une page ts les 25 images, NE FONCTIONNE PAS !!!

 