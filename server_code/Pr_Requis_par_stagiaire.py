from anvil import *
import anvil.stripe
import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from PIL import Image
import io
import pathlib
import Pr_pdf_to_jpg


@anvil.server.callable
def path_info(file):
    path = pathlib.Path(file)
    return str(path.parent), str(path.name), str(path.suffix)  # path, file name, extension

@anvil.server.callable
@anvil.tables.in_transaction
def modify_pre_r_par_stagiaire(stage_num, item_requis, email, file, file_extension, thumb_file, new_file_name):
    
    # finding the stagiaire's row 
    pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = stage_num,
                                              stagiaire_email = email,
                                              item_requis = item_requis                                             
                                             )                                      
    if pr_requis_row:
        if file_extension == ".jpg":
            print("serveur Preq: Ce fichier est une image JPG")          
            #--------------------------------------------------------------------------------
            # Img file, Convert the 'file' Media object into a Pillow Image
            img = Image.open(io.BytesIO(file.get_bytes()))
            width, height = img.size
            print('size', width, height)
            # Si img de très haute qualité je divise en deux
            if width >= height:   #landscape
                if width > 2000:
                    width = width / 2.5                       # A RENTRER DS LES PARAM
                    height = height / 2.5
            if height > width:
                if height > 2000:
                    width = int(width / 2.5)
                    height = int(height / 2.5)
            # Resize the image to the required size
            img = img.resize((width,height))    
            width, height = img.size
            print('new_size', width, height)
            
            # Convert the Pillow Image into an Anvil Media object and return it
            bs = io.BytesIO()
            img.save(bs, format="JPEG")
    
            file = anvil.BlobMedia("image/jpeg", bs.getvalue(), name=new_file_name)   
            # -------------------------------------------------------------------------------------            
            # SAUVEGARDE IMG ds doc1, je ne change pas pdf_doc1, je ne sauve plus le thumb
            pr_requis_row.update(check=True,               
                                doc1 = file
                                )
            print("MAJ de la table pre recquis par le doc jpg")
            """
            pr_requis_row.update(check=True,               
                                doc1 = file,
                                thumb_doc1 = thumb_file
                                )
            """           
            return True    # Sov effectué et None liste_images (car img, pas pdf)   
    

        if file_extension == ".pdf":
            print("serveur Preq: Ce fichier est un pdf")
            # SAUVEGARDE du fichier pdf 'file'
            pr_requis_row.update(check=True,               
                                pdf_doc1 = file
                                )
        return True
    else:
        return False