from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from PIL import Image
import io
import pathlib

@anvil.server.callable
def path_info(file):
    path = pathlib.Path(file)
    return str(path.parent), str(path.name), str(path.suffix)

@anvil.server.callable
@anvil.tables.in_transaction
def modify_pre_r_par_stagiaire(stage_num, item_requis, email, file, thumb_file):
    # finding the stagiaire's row 
    row = app_tables.pre_requis_stagiaire.get(stage_num = stage_num,
                                              stagiaire_email = email,
                                              item_requis = item_requis                                             
                                             )
    if not row:
        raise Exception("Erreur: stagiaire not found !")
        return False
    
    # appel module path (path_info)
    path_parent, file_name, file_extension = path_info(str(file.name))       #module path info 
    
    if file_extension != ".pdf":
        print("serveur: Ce fichier est une image")

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
        
    # SAUVEGARDE QUELQUESOIT L'EXTENSION IMG OU PDF dans doc1
    row.update(check=True,               
                doc1 = file,
                thumb_doc1 = thumb_file
                )
    return True

        