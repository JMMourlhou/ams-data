from ._anvil_designer import plotTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from plotly import graph_objects as go

class plot(plotTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # lecture du qcm
        qcm_n = app_tables.qcm_description.get(qcm_nb=1)
        # lecture du stagiaire
        user=anvil.users.get_user()
        if user:
            qcm_rows = app_tables.qcm_result.search(
                                            user_qcm = user,
                                            qcm_number = qcm_n
                                        )
           
            x = []
            y = []
            cpt=0
            nb_qcm_passe = len(qcm_rows)
            
            for q in qcm_rows:
                cpt += 1
                x.append(cpt)
                y.append(q['nb_rep_ok'])
            print(x)
            print(y)
                
        # Plot some data
        self.plot_1.data = [
            go.Scatter(
                    x = [1, 2, 3],
                    y = [3, 1, 6],
                    marker = dict(
                                     color= 'rgb(16, 32, 77)'
                                 )
                ),
            go.Bar(
                x,
                y,
                name = "essai"
            )
        ]
    
        # Configure the plot layout
        self.plot_1.layout = {
                                'title': 'Progression des résultats, QCM ' + qcm_n['destination'],
                                'xaxis':    {
                                                'title': 'QCM'
                                            }
                            }
        self.plot_1.layout.yaxis.title = 'Nb bonnes réponses'
        self.plot_1.layout.annotations = [
                                             dict(
                                                    text = 'Simple annotation',
                                                    x = 0,
                                                    xref = 'paper',
                                                    y = 0,
                                                    yref = 'paper'
                                                 )
                                        ]