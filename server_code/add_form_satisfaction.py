import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable           #AJOUT d'un formulaire ds table _transaction, anonyme
@anvil.tables.in_transaction
def add_1_formulaire_satisfaction(  user_stagiaire,              # users row
                                    stage_row,                   # stages row
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
    id=new_row.get_id()
    #relecture du row:
    re_read_row= app_tables.stage_satisf.get_by_id(id)
    
    if re_read_row:  
        # check de la formule de satisfaction pour que le stgiaire ne puisse pas y revenir
        row = app_tables.stagiaires_inscrits.get(   numero =     stage_row['numero'],
                                                    user_email = user_stagiaire
                                                )
        row.update(enquete_satisf=True)
        return(True)
    else:
        return(False)
