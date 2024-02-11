from ._anvil_designer import PlotTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from plotly import graph_objects as go           # AFFICHAGE DES RESULTATS de plusieurs tests sur 1 QCM

class Plot(PlotTemplate):
    def __init__(self, nb, legend = False, **properties):        # le nb vient de temp3 ds user (à cause du qcm BNSSA tiré de plusieurs qcm)
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        
        # lecture du qcm
        qcm_n = app_tables.qcm_description.get(qcm_nb=nb)
        
        # lecture du stagiaire
        user=anvil.users.get_user()
        if user:
            qcm_rows = app_tables.qcm_result.search(
                                            user_qcm = user,
                                            qcm_number = qcm_n
                                        )
            
            
            listx_int = []           # liste nb de fois qcm effectué         (1,    2,   3,  ...)
            listx_str = []           # liste nb de fois, mais en str pour affichage de x
            listy = []           # liste du résultat obtenu àch passage  (10%, 25%, 35%, ...)
            list_min = []
            liste_date =[]
            cpt=0
            nb_qcm_passe = len(qcm_rows)

            for q in qcm_rows:
                cpt += 1
                listx_int.append(cpt)
                listx_str.append(str(cpt))
                listy.append(q['p100_sur_nb_rep'])    
                min_rep = 75                         # max = 75 %
                list_min.append(min_rep)
                if len(qcm_rows)>1:
                    liste_date.append(str(q['time'].strftime("%d/%m")))
                else:
                    liste_date.append(str(q['time'].strftime("%d/%m/%Y, %Hh%M")))            
            
            print('date / h : ', str(liste_date[nb_qcm_passe-1]))
            print("x int  ",listx_int)
            print("x text ",listx_str)
            print("y", listy)
            print(list_min)
                
        # Plot some data     SI PLUSIEURS QCM EFFECTUES j'affiche la ligne de 75%
        if len(qcm_rows)>1:
            self.label_nom.text = f"{user['email']}"
            title = f"{nb_qcm_passe} passages pour le QCM '{qcm_n['destination']}''"
            self.plot_1.data = [
                go.Scatter(
                        x = listx_int,
                        y = listy,
                        marker = dict(color= 'rgb(16, 32, 77)' )
                    ),
                go.Scatter(
                        x = listx_int,
                        y = list_min,
                        marker = dict(color= 'rgb(204, 0, 0)' ),
                        mode="lines",
                        line=dict(dash='dash')
                    )
            ]
        else:                            # 1 SEUL QCM : Camembert
            date_qcm = str(liste_date[nb_qcm_passe-1])
            title = f"QCM {qcm_n['destination']} du {date_qcm}, de {user['email']}"
            colors = ['green', 'lightblue']  # couleurs pour chaque tranche
            labels = ['% Bonnes réponses','Erreurs']  # Les étiquettes correspondantes
            listy_pour1qcm = [listy[0],100-listy[0]]
            if  listy[0] >= 75:
                self.label_nom.text = f"Réussite au QCM {qcm_n['destination']} / {user['nom']} {user['prenom']}"
                title_pie = "Réussite"
            else:
                self.label_nom.text = f"Echec au QCM {qcm_n['destination']} / {user['nom']} {user['prenom']}"
                title_pie = "Echec"
            
            self.plot_1.data = [
                go.Pie(
                        values=listy_pour1qcm,
                        labels=labels,
                        hole=0.4,
                        title = title_pie,
                        marker_colors=colors
                    )
            ]
          
        # Configure the plot layout
        if len(qcm_rows)>1:
            self.plot_1.layout = {  'displayModeBar' : True,          # False: n'affiche que qd passe au dessus
                                    'modeBarButtonsToRemove' : ['zoomIn2d', 'zoomOut2d', 'pan2d' ],
                                    'title': title,
                                    'xaxis': {'title': title,
                                            'visible': False                 # Masque l'axe X et son titre  !!
                                            },
                                    'yaxis': dict(range=[0, 100]),    
                                    'plot_bgcolor': 'lightblue',       # Couleur de fond personnalisée
                                    'tickmode': 'array',               # de 1 en 1
                                    'tickvals' : listx_int,            # position des marques de graduation
                                    'ticktext' : listx_str,            # texte qui doit être affiché sur x
                                    'showlegend': legend     # True pour montrer la légende (false par défaut voir l'init)
                                }
        else:      # 1 seul QCM: Pie, je n'affiche pas les axes
            self.plot_1.layout = {  'displayModeBar' : True,          # False: n'affiche que qd passe au dessus
                                    'modeBarButtonsToRemove' : ['zoomIn2d', 'zoomOut2d', 'pan2d' ],
                                    'title': title,
                                    'xaxis': {'title': title,
                                            'visible': False                 # Masque l'axe X et son titre  !!
                                            },
                                    'yaxis': {'title': title,
                                            'visible': False                # Masque l'axe y et son titre  !!
                                            },
                                    'plot_bgcolor': 'lightblue',       # Couleur de fond personnalisée
                                }
            
        self.plot_1.layout.yaxis.title = '% réponses ok - ' + user['email']
        
        date_deb = liste_date[0]     #dernière date
        date_fin = liste_date[nb_qcm_passe-1]   # derniere date
        if len(qcm_rows)>1:
            self.plot_1.layout.annotations = [
                                                dict(
                                                        text = date_deb,            # flèche commentaire
                                                        x = 1,
                                                        xref = 'x',
                                                        y = 0,
                                                        yref = 'y',
                                                        showarrow=True,       # Montre lea flèche :True
                                                        arrowhead=15,
                                                        ax=0,
                                                        ay=-20, 
                                                        color = 'white',
                                                        fontsize = 12
                                                    ),
                                                dict(
                                                        text = date_fin,            # flèche commentaire
                                                        x = nb_qcm_passe,
                                                        xref = 'x',
                                                        y = 0,
                                                        yref = 'y',
                                                        showarrow=True,
                                                        arrowhead=15,
                                                        ax=0,                    # 0
                                                        ay=-20,                    # -20
                                                        color = 'white',
                                                        fontsize = 12
                                                    )
                                            ]
      
            
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from .Main import Main
        open_form('Main',99)

    def plot_1_click(self, points, **event_args):
        """This method is called when a data point is clicked."""
        print("download")
        #anvil.media.download(self.plot_1)

