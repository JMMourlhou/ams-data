import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable           #Création d'un nouveau stage
def add_stagiaire(stagiaire, stage, mode_fi):

    # lecture fichier père stages
    code_stage = app_tables.stages.get(numero=int(stage))
    if len(code_stage)==0 :
        alert("Stage non trouvé ds fichier stages !")
        valid=False
        return valid

    # lecture fichier père user
    user=anvil.users.get_user()
    if user:
        if user != stagiaire :
            alert("Stagiaire non trouvé ds fichier users !")
            valid=False
            return valid

    # lecture fichier père mode financemnt
    mode_fin = app_tables.mode_financement.get(code_fi=mode_fi)    
    if len(mode_fi)==0 :
        alert("Mode de financemnt non trouvé ds fichier param mode financemnt !")
        valid=False
        return valid   
        
    new_row=app_tables.stagiaires_inscrits.add_row(
                              stage = code_stage,  
                              stagiaire = user["email"],
                              financement = mode_fin,
                              )
             
    stagiaire_row = app_tables.stagiaires_inscrits.search(stage=new_row['stage'])
    if len(stagiaire_row)>0:
        valid=True
        #effacemnt du code satge ds user:
        user.update(stage_num_temp=None)
        
    else:
        valid=False
    return valid