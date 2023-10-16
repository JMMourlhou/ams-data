import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable           #Création d'un nouveau stagiaire ds le stage
@anvil.tables.in_transaction
def add_stagiaire(stagiaire, stage, mode_fi):
    valid=""
    # lecture fichier père stages
    code_stage = app_tables.stages.get(numero=int(stage))
    if not code_stage :
        valid="Stage non trouvé ds fichier stages !"
        return valid
  
    # lecture fichier père user
    user=anvil.users.get_user()
    if user:
        if user != stagiaire :
            valid="Stagiaire non trouvé ds fichier users !"
            return valid

    # lecture fichier père mode financemnt
    mode_fin = app_tables.mode_financement.get(code_fi=mode_fi)    
    if not mode_fin :
        valid="Mode de financemnt non trouvé ds fichier param mode financemnt !"
        return valid

    #vérification si user pas déjà inscrit ds fichier stagiaire inscrit, POUR CE STAGE:
    
    test = app_tables.stagiaires_inscrits.search(user_email=user,                 # ce user
                                                 stage=code_stage)                # ET pour ce stage
    if len(test)>0:
        valid="Vous êtes déjà inscrit à ce stage !"
        # ******************************************************************* EFFACT code stage ds user avant retour
        user.update(stage_num_temp = 0)
        return valid 
        
    new_row=app_tables.stagiaires_inscrits.add_row(
                              stage = code_stage,  
                              user_email = user,
                              name = user['nom'].lower(),    # nom pour permettre le tri sur le nom
                              financement = mode_fin
                              )
             
    stagiaire_row = app_tables.stagiaires_inscrits.search(stage=new_row['stage'])
    if stagiaire_row:
        # ******************************************************************* EFFACT code stage ds user et INCREMENT du nb de stgiaires ds le stage:
        # ajouter le dico de l'historique du stagiare (ex; {psc1:28/08/2023} )
        user.update(stage_num_temp = 0)
        # Incrément nb de stagiaires début stage ds fichier père stage
        try:  # si nb à None il y aurait une erreur
            if code_stage:
                nb = int(code_stage['nb_stagiaires_deb'])+1
                code_stage.update(nb_stagiaires_deb=nb)
                #print("passage ds try ok")
            else:
                valid="erreur: code_stage vide"
        except:        # nb à None,  
            nb=1
            code_stage.update(nb_stagiaires_deb=nb)
            #print("passage ds except ok")
            
        valid="Vous êtes inscrit ! (" + str(nb) + ")"
    else:
        valid="Stagiaire non retrouvé dans fichier stagiaires inscrits"
    return valid