import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import anvil.pdf
from anvil.pdf import PDFRenderer

@anvil.server.background_task
def create_list(num_stage, intitule):
    #lecture du fichier père stages
    stage_row = app_tables.stages.get(numero=int(num_stage))    
    if not stage_row:   
        print("stage non trouvé à partir de num_stage server module: Stagiaires_list_pdf")
    else:
        " sauvegarde de la liste ds la table "
        list = app_tables.stagiaires_inscrits.search(stage=stage_row)
        
        stage_row.update(list_display = list) # sauvegarde de la liste ds le stage_row
        print("liste du stage stockée")
    return
        

@anvil.server.callable
def run_bg_task1(num_stage, intitule):
    task = anvil.server.launch_background_task('create_list',num_stage, intitule)
    print ("task", task)
    return task
