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
        qcm_n = app_tables.qcm_description.get(qcm_nb=3)
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
            liste_date =[]
            cpt=0
            nb_qcm_passe = len(qcm_rows)

            for q in qcm_rows:
                cpt += 1
                listx.append(cpt)
                listy.append(q['nb_rep_ok'])
                max_rep = q['nb_rep_ok']/q['p100_sur_nb_rep']*100
                list_max.append(max_rep)
                liste_date.append(str(q['time'].strftime("%d/%m/%Y")))
                
            print(listx)
            print(listy)
            print(list_max)
                
        # Plot some data
        self.plot_1.data = [
        go.Scatter(
                    x = listx,
                    y = listy,
                    marker = dict(color= 'rgb(16, 32, 77)' )
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
                                'xaxis': {'title': "Nb d'essais"},
                                'tickmode': 1,           # de 1 en 1
                            }
        self.plot_1.layout.yaxis.title = 'Nb bonnes réponses'
        
        date_deb = liste_date[0]     #dernière date
        date_fin = liste_date[nb_qcm_passe-1]   # derniere date
        self.plot_1.layout.annotations = [
                                             dict(
                                                    text = date_deb,            # flèche commentaire
                                                    x = 1,
                                                    xref = 'x',
                                                    y = 0,
                                                    yref = 'y',
                                                    showarrow=True,
                                                    arrowhead=7,
                                                    ax=0,
                                                    ay=-40
                                                 ),
                                            dict(
                                                    text = date_fin,            # flèche commentaire
                                                    x = nb_qcm_passe,
                                                    xref = 'x',
                                                    y = 0,
                                                    yref = 'y',
                                                    showarrow=True,
                                                    arrowhead=7,
                                                    ax=0,
                                                    ay=-40
                                                 )
                                        ]

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)
"""
'tickmode': 'array',

# Specify the layout
    layout = {
      'title': 'Election results',
      'yaxis': {'title': 'Seats'},
      'xaxis': {
        'tickmode': 'array',
        'tickvals': list(range(27)),
        'ticktext': data['year'],
      },
    }
"""