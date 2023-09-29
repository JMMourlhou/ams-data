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
        print("Stage non trouvé ds fichier stages !")
        valid=False
        return valid
    else:
        # Incrément nb de stagiaires début stage 
        nb = int(code_stage['nb_stagiaires_deb'])
        
        print("Incrément avant ",nb)
        nb =+ 1
        code_stage.update(nb_stagiaires_deb=nb)
        print("Incrément après ",nb)
    
    # lecture fichier père user
    user=anvil.users.get_user()
    if user:
        if user != stagiaire :
            print("Stagiaire non trouvé ds fichier users !")
            valid=False
            return valid

    # lecture fichier père mode financemnt
    mode_fin = app_tables.mode_financement.get(code_fi=mode_fi)    
    if not mode_fin :
        print("Mode de financemnt non trouvé ds fichier param mode financemnt !")
        valid=False
        return valid   

    #vérification si user pas déjà inscrit ds fichier stagiaire inscrit, POUR CE STAGE:
    test = app_tables.stagiaires_inscrits.search(user_email=user,                 # ce user
                                                 stage=stage)                     # ET pour ce stage
    if test :
        print("Vous êtes déjà inscrit à ce stage !")
        valid=False
        return valid   
        
    new_row=app_tables.stagiaires_inscrits.add_row(
                              stage = code_stage,  
                              user_email = user,
                              name = user['nom'].lower(),    # nom pour permettre le trie sur le nom
                              financement = mode_fin,
                              )
             
    stagiaire_row = app_tables.stagiaires_inscrits.search(stage=new_row['stage'])
    if stagiaire_row:
        valid=True
        #effacemnt du code stage ds user et incrément du nb de stgiaires ds le stage:
        user.update(stage_num_temp = None)
    else:
        valid=False
    return valid