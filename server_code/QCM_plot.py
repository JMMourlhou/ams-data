import matplotlib.pyplot as plt           # AFFICHAGE DES RESULTATS de plusieurs tests sur 1 QCM
import anvil.server

# ==================================================================================================
# At the end od a QCM, displays the results
# ==================================================================================================
@anvil.server.callable
def qcm_plot(listx, listy, x_label, y_label):
    plt.xlabel("Nb de passages")
    plt.ylabel("Résultats")
    # Plot some data
    return plt.plot(listx, listy)