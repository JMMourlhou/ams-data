import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from . import French_zone_server_side
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
                               margins = {'top': 0.8, 'bottom': 0.5, 'left': 1.0, 'right': 1.0},  # en cm
                               scale = 1.0,
                               quality =  "printer"
                              ).render_form('Visu_trombi',num_stage, intitule, True)

    " sauvegarde du media_object ds la table "
    #lecture du fichier stages sur le num de stage
    stage_row = app_tables.stages.get(numero=int(num_stage))
    if not stage_row:   
        print("stage non trouvé à partir de num_stage server module: Stagiaires_trombi")
    else:
        # sauvegarde du trombi media ds le stage_row
        stage_row.update(trombi_media = media_object,
                        ) 
        print("trombi pdf du stage stockée")
        
    anvil.server.task_state['progress'] = 0 #finished   
    # get_return_value(): returns the return value of the task, or None if the task has not yet returned.

    return media_object

@anvil.server.callable
def run_bg_task2(num_stage, intitule):
    task = anvil.server.launch_background_task('create_trombi_pdf',num_stage, intitule)
    #print ("task", task)
    
    #lecture du fichier stages sur le num de stage
    stage_row = app_tables.stages.get(numero=int(num_stage))
    if not stage_row:   
        print("stage non trouvé à partir de num_stage server module: Stagiaires_trombi")
    else:
        # sauvegarde du trombi time et id media ds le stage_row

        stage_row.update(trombi_time = French_zone_server_side.time_french_zone(), 
                         trombi_task_id = task.get_id()        
                        ) 
        print("time et id trombi stockée")
    
    if task.is_completed():
        return
    

