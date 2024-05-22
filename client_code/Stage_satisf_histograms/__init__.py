from ._anvil_designer import Stage_satisf_histogramsTemplate
from anvil import *
import plotly.graph_objects as go


from plotly import graph_objects as go

# AFFICHAGE DES RESULTATS d pour 1 question fermée du formulaire de satisfaction
# APPELE PAR LA FORM 'STAGE_SATISF_TATITICS' par add component: 
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
        def SetColor(x):
            if x == 0:
                return "red"
            elif x == 1:
                return "yellow"
            elif x == 2:
                return "green"
            if x == 3:
                return "blue"
            elif x == 4:
                return "black"
            elif x == 5:
                return "green"   
        # Plot some data
        self.plot_1.data = [
            go.Bar(x=listx,
                   y=data,
                   marker=dict(color=("red", "yellow","green","blue","black","white")),
                   text=[t0,t1,t2,t3,t4,t5])                 # texte ds les barres
        ]
        #marker=dict(color="rgb(16, 32, 77)" ),    # couleur des barres 
        # Configure the plot layout
        titre = qt
        self.plot_1.layout = {
                'title': titre,    # titre du graphique
            
                'xaxis':  {
                    'title': "(0:Très insatisfait à 5:Très satisfait)",
                            },

                "yaxis": {
                    "title": 'Nb de réponses',
                    "visible": False,  # Montre l'axe y et son titre  !!
                    'tickmode': 1,           # de 1 en 1
                },
                "plot_bgcolor": "lightblue",  # Couleur de fond personnalisée
                "showlegend": False,  # True pour montrer la légende (false par défaut voir l'init)
            }