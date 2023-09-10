import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from . import French_zone

import anvil.pdf
from anvil.pdf import PDFRenderer

@anvil.server.background_task
def create_trombi_pdf(num_stage, intitule):
    anvil.server.task_state['progress'] = 42
    print("create_trombi_pdf")
    """
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
    "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """
    media_object = PDFRenderer(page_size ='A4',
                               filename = f"{intitule}/{num_stage}.pdf",
                               landscape = False,
                               margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  # en cm
                               scale = 1.0,
                               quality =  "printer"
                              ).render_form('Visu_trombi',num_stage, intitule, True)

    " sauvegarde du media_object ds la table "
    #lecture du fichier stages sur le num de stage
    stage_row = app_tables.stages.get(numero=int(num_stage))
    if not stage_row:   
        print("stage non trouvé à partir de num_stage server module: Stagiaires_trombi")
    else:
        stage_row.update(trombi_media = media_object,
                         trombi_time = French_zone.french_zone_time,
                         trombi_task_id = task.get_id() 
                        ) # sauvegarde du trombi media ds le stage_row
        print("liste pdf du stage stockée")
        
    anvil.server.task_state['progress'] = 0 #finished   
    # get_return_value(): returns the return value of the task, or None if the task has not yet returned.

    return media_object
    
    

@anvil.server.callable
def run_bg_task2(num_stage, intitule):
    task = anvil.server.launch_background_task('create_trombi_pdf',num_stage, intitule)
    #print ("task", task)
    
    if task.is_completed():
        return
    

