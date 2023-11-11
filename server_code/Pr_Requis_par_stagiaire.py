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
def modify_pre_r_par_stagiaire(stage_num, item_requis, email, file, thumb_file):
    # finding the stgiaire's row 
    row = app_tables.pre_requis_stagiaire.get(stage_num = stage_num,
                                              stagiaire_email = email,
                                              item_requis = item_requis                                             
                                             )
    if not row:
        raise Exception("Erreur: stagiaire not found !")
        return False
    else:           
        row.update(check=True,
                   doc1 = file,
                   thumb_doc1 = thumb_file
                   )
        return True