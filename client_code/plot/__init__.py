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
            
            listx = []
            listy = []
            list_max = []
            cpt=0
            nb_qcm_passe = len(qcm_rows)

            for q in qcm_rows:
                cpt += 1
                listx.append(cpt)
                listy.append(q['nb_rep_ok'])
                max_rep = q['nb_rep_ok']/q['p100_sur_nb_rep']*100
                list_max.append(max_rep)
                
            print(listx)
            print(listy)
            print(list_max)
                
        # Plot some data
        self.plot_1.data = [
        go.Scatter(
                    x = listx,
                    y = listy,
                    marker = dict(
                                     color= 'rgb(16, 32, 77)'
                                 )
                ),
        go.Bar(
            x = listx,
            y = list_max,
            name = 'max questions'
        )
        ]
    
        # Configure the plot layout
        self.plot_1.layout = {
                                'title': 'Progression des résultats, QCM ' + qcm_n['destination'],
                                'xaxis':    {
                                                'title': "Nb d'essais"
                                            }
                            }
        self.plot_1.layout.yaxis.title = 'Nb bonnes réponses'
        self.plot_1.layout.annotations = [
                                             dict(
                                                    text = 'text !!!!!!!!',
                                                    x = 0,
                                                    xref = 'x ref -------',
                                                    y = 0,
                                                    yref = 'yref --------- '
                                                 )
                                        ]

# title=go.layout.Title(text="Election results", x=0.5),