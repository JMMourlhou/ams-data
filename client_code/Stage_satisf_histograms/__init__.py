from ._anvil_designer import Stage_satisf_histogramsTemplate
from anvil import *
import plotly.graph_objects as go


from plotly import graph_objects as go

# AFFICHAGE DES RESULTATS d pour 1 question fermée du formulaire de satisfaction plusieurs tests sur 1 QCM


class Stage_satisf_histograms(Stage_satisf_histogramsTemplate):
    def __init__(self,r0,r1,r2,r3,r4,r5, **properties):  
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        data = [r0,r1,r2,r3,r4,r5]
        listx = [0,1,2,3,4,5]
        
        # Plot some data
        self.plot_1.data = [
            #go.Scatter(x=listx, y=listy, marker=dict(color="rgb(16, 32, 77)")),
            go.Bar(x=listx, y=data),
            go.Histogram(x=listx, y=data),
            
        ]
        