
import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# Effacement d'un stagiaire, formateur, tuteur de la table users
@anvil.server.callable
def del_personne(personne_row):   
    print(personne_row)
    print(personne_row['email'])
    msg = "Erreur en effacement"
    row_users = app_tables.users.get(email=personne_row['email'])
    print(row_users)
    print(row_users['email'])
    if row_users:
        row_users.delele()
        row = app_tables.users.get(email=personne_row)
        if not row:
            msg = "Effacement effectué !"
    return msg