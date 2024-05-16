import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable           #AJOUT d'un formulaire ds table _transaction, anonyme
@anvil.tables.in_transaction
def add_1_formulaire_satisfaction(  user_stagiaire,              
                                    stage_row,
                                    dico_rep_q_ferm,
                                    dico_rep_q_ouv,
                                    date_time    
                                ):
    # Print pour vérif des 2 dicos    
    print("=============== serveur side:")
    print("============== Dict reponses fermées: ")
    print(dico_rep_q_ferm)   
    print()
    print("============== Dict reponses ouvertes: ")
    print(dico_rep_q_ouv)
    print()
    print(date_time)
    return(False)
