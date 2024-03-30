from anvil import *

import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
#import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from PIL import Image
import io
#import pathlib
#import Pr_pdf_to_jpg
import math

@anvil.server.callable
def path_info(file):
    path = pathlib.Path(file)
    return str(path.parent), str(path.name), str(path.suffix)  # path, file name, extension

@anvil.server.callable
@anvil.tables.in_transaction
def modify_pre_r_par_stagiaire(stage_num, item_requis, email, file, file_extension=".jpg", new_file_name="pr_rq.jpg"):
#def modify_pre_r_par_stagiaire(stage_num, item_requis, email, file, file_extension, thumb_file, new_file_name):
#def modify_pre_r_par_stagiaire(pr_requis_row, file, file_extension=".jpg"):             
    valid=False
    pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = stage_num,
                                                         stagiaire_email = email,
                                                         item_requis = item_requis                                             
                                             ) 
    if pr_requis_row:
        if file_extension == ".jpg":
            print("serveur Preq: Ce fichier est une image JPG")        


            
            #-------------------------------------------------------------------------------- à Remplacer par 1 B.G. task / loop traitmt images
            # Img file, Convert the 'file' Media object into a Pillow Image
            img = Image.open(io.BytesIO(file.get_bytes()))
            width, height = img.size
            print('size', width, height)
            # Si img de très haute qualité je divise en deux
            if width >= height:   #landscape
                if width > 2000:
                    print("**** w > H")
                    width = math.floor(width / 2.5)            # je ne prends pas les virgules           # A RENTRER DS LES PARAM
                    height = math.floor(height / 2.5)
            if height > width:
                if height > 2000:
                    print("**** h > w")
                    width = math.floor(width / 2.5)
                    height = math.floor(height / 2.5)
            # Resize the image to the required size
            img = img.resize((width,height))    
            width, height = img.size
            print('new_size', width, height)
            
            # Convert the Pillow Image into an Anvil Media object and return it
            bs = io.BytesIO()
            img.save(bs, format="JPEG")
    
            file = anvil.BlobMedia("image/jpeg", bs.getvalue(), name=new_file_name)   
            # -------------------------------------------------------------------------------------  



            
            
            # SAUVEGARDE IMG ds doc1, j'efface pdf_doc1 sinon je risque de télécharger un ancien fichier, je ne sauve plus le thumb
            pr_requis_row.update(check=True,               
                                doc1 = file,
                                pdf_doc1 = None
                                )
            print("MAJ de la table pre recquis par le doc jpg")
            
            valid=True    # Sov effectué et None liste_images (car img, pas pdf)   
            return valid

        if file_extension == ".pdf":
            print("serveur Preq: Ce fichier est un pdf")
            # SAUVEGARDE du fichier pdf 'file'
            pr_requis_row.update(check=True,               
                                pdf_doc1 = file
                                )
        return True
    else:
        return False