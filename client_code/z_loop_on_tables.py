import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


#boucle sur la table users pour modif rapide d'une colonne, ici sur le role (sauf l'administrateur)
def loop():
    table_users = app_tables.users.search()
    result="erreur"
    if table_users:
        for row in table_users:
            if row['email'] != "jmarc@jmm-formation-et-services.fr":
                row.update(role="S")
        result="loop ok"     
    return result


#boucle sur la table qcm pour modif rapide d'une colonne, ici sur la reponse multi critères
def loop_qcm():
    table = app_tables.qcm.search()
    result="erreur"
    if table:
        for row in table:
            if row['reponse'] == True:
                rep_multi = "10"
            else:
                rep_multi = "01"
            row.update(rep_multi = rep_multi)
        result="loop ok"     
    return result