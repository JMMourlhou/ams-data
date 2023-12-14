from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from PIL import Image
import io
import pathlib
import z_pdf_to_img


@anvil.server.callable
def path_info(file):
    path = pathlib.Path(file)
    return str(path.parent), str(path.name), str(path.suffix)  # path, file name, extension

@anvil.server.callable
@anvil.tables.in_transaction
def modify_pre_r_par_stagiaire(stage_num, item_requis, email, file, file_extension, thumb_file=None):
    # finding the stagiaire's row 
    pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = stage_num,
                                              stagiaire_email = email,
                                              item_requis = item_requis                                             
                                             )                                      
    if not pr_requis_row:
        raise Exception("Erreur: stagiaire not found !")
        return False, None   
    
    if file_extension != ".pdf":
        print("serveur Preq: Ce fichier est une image")

        # Img file, Convert the 'file' Media object into a Pillow Image
        img = Image.open(io.BytesIO(file.get_bytes()))
        width, height = img.size
        print('size', width, height)
        """
        # Si img de très haute qualité je divise en deux
        if width >= height:   #landscape
            if width > 3000:
                width = width / 2
                height = height / 2
        if height > width:
            if height > 3000:
            width = int(width / 2)
            height = int(height / 2)
        # Resize the image to the required size
        img = img.resize((width,height))    
        width, height = img.size
        print('new_size', width, height)
        
        # Convert the Pillow Image into an Anvil Media object and return it
        bs = io.BytesIO()
        img.save(bs, format="JPEG")
    
        file_name=str(stage_num['numero'])+"_"+item_requis['code_pre_requis']
        file = anvil.BlobMedia("image/jpeg", bs.getvalue(), name=file_name)   
        """ 
        
        # SAUVEGARDE IMG ds doc1 et thumb_nail, je ne change pas pdf_doc1
        pr_requis_row.update(check=True,               
                            doc1 = file,
                            thumb_doc1 = thumb_file
                            )
        return True, None    # Sov effectué et None liste_images (car img, pas pdf)   
        

    if file_extension == ".pdf":
        print("serveur Preq: Ce fichier est un pdf")
        # SAUVEGARDE du fichier pdf 'file'
        pr_requis_row.update(check=True,               
                            pdf_doc1 = file
                            )
        print("Preq maj du pdf_doc1, envoi au module z_pdf_to_img.pdf_into_image")
        liste_images = z_pdf_to_img.pdf_into_images(stage_num, item_requis, email)
    return True, liste_images
        