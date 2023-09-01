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
def create_pdf(num_stage, intitule):
    media_object = PDFRenderer(page_size ='A4',
                               filename = f"{intitule}/{num_stage}",
                               landscape = False,
                               margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  # en cm
                               scale = 1.0,
                               quality =  "printer"
                              ).render_form('Visu_1_stage',num_stage, intitule, True)  
    """
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
    "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """
    return media_object

@anvil.server.callable
def run_bg_task(num_stage, intitule):
    media_object = anvil.server.launch_background_task('create_pdf',num_stage, intitule)
    return media_object