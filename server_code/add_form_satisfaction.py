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
    new_row=app_tables.stage_satisf.add_row(stage_row=stage_row,
                                    stage_type_txt=stage_row["code_txt"],
                                    stage_num_txt=str(stage_row["numero"]),
                                    date_heure=date_time,
                                    rep_dico_rep_ferm=dico_rep_q_ferm,
                                    rep_dico_rep_ouv=dico_rep_q_ouv
                                   )
    #relecture du row:
    re_read_row = app_tables.stage_satisf.get(stage_row=new_row["stage_row"],
                                            date_heure=new_row["date_heure"],
                                            rep_dico_rep_ferm=new_row["rep_dico_rep_ouv"])
    if re_read_row:                        
        return(True)
    else:
        return(False)
