import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.pdf import PDFRenderer

"""
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
    "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """
# Calculer la taille du file et ajuster la qualité (screen?)
@anvil.server.callable
def generate_pdf_from_jpg(file, file_name, stage_num, email, item_requis, pr_requis_row):
    pdf_object = PDFRenderer(page_size ='A4',
                            filename = f"{file_name}.pdf",
                            landscape = False,
                            margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  #  cm
                            scale = 1.0,
                            quality =  "printer"
                            ).render_form('Pre_Visu_img_Pdf_Generation',file, file_name)
                            #).render_form('Pre_Visu_img_Pdf',file, file_name, stage_num, email, item_requis)
    # save mediaobject in table pre requi du stage/stagiaire/pre requi  
    """
    # finding the row
    pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = stage_num,
                                              stagiaire_email = email,
                                              item_requis = item_requis                                             
                                             )
    """                                        
    if pr_requis_row:
        pr_requis_row.update(pdf_doc1 = pdf_object)

    return pdf_object



