import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable           #Création d'un nouveau stage
@anvil.tables.in_transaction
def add_stagiaire(stagiaire, stage, mode_fi):

    # lecture fichier père stages
    code_stage = app_tables.stages.get(numero=int(stage))
    if not code_stage :
        err="Stage non trouvé ds fichier stages !"
        valid=False
        return valid, err
  
    # lecture fichier père user
    user=anvil.users.get_user()
    if user:
        if user != stagiaire :
            err="Stagiaire non trouvé ds fichier users !"
            valid=False
            return valid, err

    # lecture fichier père mode financemnt
    mode_fin = app_tables.mode_financement.get(code_fi=mode_fi)    
    if not mode_fin :
        err="Mode de financemnt non trouvé ds fichier param mode financemnt !"
        valid=False
        return valid, err  

    #vérification si user pas déjà inscrit ds fichier stagiaire inscrit, POUR CE STAGE:
    test = app_tables.stagiaires_inscrits.search(user_email=user,                 # ce user
                                                 stage=code_stage)                # ET pour ce stage
    if test :
        err="Vous êtes déjà inscrit à ce stage !"
        valid=False
        return valid, err  
        
    new_row=app_tables.stagiaires_inscrits.add_row(
                              stage = code_stage,  
                              user_email = user,
                              name = user['nom'].lower(),    # nom pour permettre le tri sur le nom
                              financement = mode_fin,
                              )
             
    stagiaire_row = app_tables.stagiaires_inscrits.search(stage=new_row['stage'])
    if stagiaire_row:
        #effacemnt du code stage ds user et incrément du nb de stgiaires ds le stage:
        user.update(stage_num_temp = None)
        # Incrément nb de stagiaires début stage ds fichier père stage
        nb = int(code_stage['nb_stagiaires_deb'])
        nb =+ 1
        code_stage.update(nb_stagiaires_deb=nb)
        err = "Incrément nb de stagiaires inscrits: (" + nb + ")"
        valid=True
    else:
        err="Stagiaire non retrouvé dans fichier stagiaires inscrits"
        valid=False
    return(valid, err)