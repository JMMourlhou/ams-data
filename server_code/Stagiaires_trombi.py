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
def create_trombi_pdf(num_stage, intitule):
    print("create_trombi_pdf")
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
        print("stage non trouvé à partir de num_stageds server module: Stagiaires_list_pdf")
    else:
        stage_row.update(list_media = media_object) # sauvegarde de la liste pdf ds le stage_row
        print("liste pdf du stage stockée")
    return media_object
    """
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
    "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """
    

@anvil.server.callable
def run_bg_task2(num_stage, intitule):
    task = anvil.server.launch_background_task('create_trombi_pdf',num_stage, intitule)
    print ("task", task)
    return task

