from ._anvil_designer import Plot_matplotlibTemplate
from anvil import *
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#from matplotlib import matplotlib.pyplot as plt           # AFFICHAGE DES RESULTATS de plusieurs tests sur 1 QCM

class Plot_matplotlib(Plot_matplotlibTemplate):
    def __init__(self, nb, legend = True, **properties):        # le nb vient de temp3 ds user (à cause du qcm BNSSA tiré de plusieurs qcm)
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

            listx = []           # liste nb de fois qcm effectué         (1,    2,   3,  ...)
            listy = []           # liste du résultat obtenu àch passage  (10%, 25%, 35%, ...)
            list_max = []
            liste_date =[]
            cpt=0
            nb_qcm_passe = len(qcm_rows)

            for q in qcm_rows:
                cpt += 1
                listx.append(cpt)
                listy.append(q['p100_sur_nb_rep'])
                max_rep = 75                         # max = 75 %
                list_max.append(max_rep)
                liste_date.append(str(q['time'].strftime("%d/%m/%Y")))
                #liste_date.append(str(q['time'].strftime("%d/%m")))
                x_label = "Nb de QCM"
                y_label = "Résultats"

            print(listx)
            print(listy)
            print(list_max)
            
            self.plot_1.source = anvil.server.call("qcm_plot", listx, listy, x_label, y_label)
           
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from .Main import Main
        open_form('Main',99)
