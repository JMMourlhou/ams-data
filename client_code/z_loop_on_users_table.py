import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


#boucle sur la table users pour modif rapide d'une colonne, ici sur le role
table_users = app_tables.stages.search()
if list_users:
    for row in table_users:
        row