import anvil.email

import anvil.files
from anvil.files import data_files

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
@anvil.tables.in_transaction
def modify_users_after_trombi(mel,
                     nom,
                     prenom,
                     photo,
                     ville_naissance,
                     cp_naissance,
                     date_naissance,
                     pays_naissance,
                     rue,
                     ville,
                     cp,
                     tel,
                     mail2,
                     accept_storage,
                     comments,
                     role
                ):
    # finding the stagiaire's row 
    row = app_tables.users.get(email=mel)
    if not row:
        raise Exception("Erreur: stagiaire not found !")
        return False
    else:           
        row.update(nom=nom,
                   prenom=prenom,
                   photo = photo,
                   ville_naissance = ville_naissance,
                   code_postal_naissance = cp_naissance,
                   date_naissance = date_naissance,
                   pays_naissance = pays_naissance,
                   adresse_rue = rue,
                   adresse_ville = ville,
                   adresse_code_postal = cp,
                   tel = tel,
                   email2 = mail2,
                   accept_data = accept_storage,
                   commentaires = comments,
                   role = role
                            )
        return True