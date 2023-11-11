#import anvil.email
#import anvil.google.auth, anvil.google.drive, anvil.google.mail
#from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
@anvil.tables.in_transaction
def modify_pre_r_pour_stagiaire(,
                                )
    # finding the stgiaire's row 
    row = app_tables.users.get(email=mel)
    if not row:
        raise Exception("Erreur: stagiaire not found !")
        return False
    else:           
        row.update(
                   photo = photo,
                   
                            )
        return True