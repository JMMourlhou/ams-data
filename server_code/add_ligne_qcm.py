import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def add_ligne_qcm(num_question, question, reponse, bareme, image, code_stage="PSE1",):
    
    #lecture fichier père code stages
    code_stage = app_tables.codes_stages.get(code=code_stage)          # A MODIFIER QD RAJOUTE DIFFERENRS QCM
    if not code_stage:   
        alert("Code stage non trouvé ds fichier param Code_stages")
        valid=False
        return valid        

    new_row=app_tables.qcm.add_row(num= int(num_question),
                                   question=question,
                                   reponse=reponse,
                                   bareme=str(bareme),
                                   photo = image,
                                   pour_stage=code_stage)

             
    qcm_row = app_tables.qcm.search(num=new_row['num'])
    if qcm_row:
        valid=True
        
    else:
        valid=False
    return valid