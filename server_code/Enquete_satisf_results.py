#import anvil.tables as tables
#import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.pdf import PDFRenderer
"""
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
 ** "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """
# Calculer la taille du file et ajuster la qualité (screen : pas assez bon)
@anvil.server.background_task
def generate_satisf_results(stage_num, type, row):
    pdf_object = PDFRenderer(page_size ='A4',
                            filename = f"Enquete_satisf_{type}_{stage_num}.pdf",
                            landscape = False,
                            margins = {'top': 0.3, 'bottom': 0.1, 'left': 0.2, 'right': 0.2},  #  cm
                            scale = 1.0,                                                       
                            quality = "screen"      
                            ).render_form('Stage_satisf_statistics',True,row)    # True: pdf mode, j'efface le bt return et passe le row du stage qui avait été sélectionné
    """   
    #lecture du fichier stages sur le num de stage
    stage_row = app_tables.stages.get(numero=stage_num)
    if not stage_row:   
        print("stage non trouvé à partir de num_stage server module: Stagiaires_trombi")
    else:
        # sauvegarde du résultat de l'enquete media
        stage_row.update(satis_pdf = pdf_object)              
        print("Sauvegarde trombi pdf")
    """
    # sauvegarde du résultat de l'enquete media
    row.update(satis_pdf = pdf_object) 

# A FAIRE APPELER from client side
@anvil.server.callable
def run_bg_task_satisf(stage_num, type, row):
    task = anvil.server.launch_background_task('generate_satisf_results',stage_num, type, row)
    return task