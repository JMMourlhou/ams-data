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
import math

"""
**************************************************** ECRITURE DE L'IMAGE EN BGT 
"""
@anvil.server.background_task
def reseize_jpg(row):
    if row:
        print(row['stagiaire_email'])
        file=row['doc1']

        #-------------------------------------------------------------------------------- à Remplacer par 1 B.G. task / loop traitmt images
        # Img file, Convert the 'file' Media object into a Pillow Image
        img = Image.open(io.BytesIO(file.get_bytes()))
        width, height = img.size
        name = img.name
        print('seize', width, height)
        print('nom', name)
        taille = width * height
        print("taille :", taille)
        if taille > 800000:    # si sup à 1000 x 800 ou   800 x 1000
            # img de  haute qualité je calcul le ratio pour ramener à 1000 x 800
            if width >= height:   #landscape
                ratio = width/1000
            else: 
                ratio = height/1000

            width = math.floor(width / ratio)            # je ne prends pas les virgules        
            height = math.floor(height / ratio)
                
        # Resize the image to the required size
        img = img.resize((width,height))

        #width, height = img.size
        #print('new_size', width, height)
        
        # Convert the Pillow Image into an Anvil Media object and return it

        img = img.convert("RGB")
        img_thumb = img                  # Je sauve l'img pour créer la petite img thumbnail
        bs = io.BytesIO()
        img.save(bs, format="JPEG")
        file = anvil.BlobMedia("image/jpeg", bs.getvalue(), name=name)
        
        width = math.floor(width / 6.666)   # la taille de l'img étant de 1000 x 800 ou   800 x 150 je ramene à 150 px  
        height = math.floor(height / 6.666)   # 1000 / 150
        img_thumb = img_thumb.resize((width,height))
        bs = io.BytesIO()                                                       
        img_thumb.save(bs, format="JPEG")
        file_thumb = anvil.BlobMedia("image/jpeg", bs.getvalue(), name=new_file_name)
            
        # -------------------------------------------------------------------------------------            
        
        # SAUVEGARDE IMG ds doc1, j'efface pdf_doc1 sinon je risque de télécharger un ancien fichier, je ne sauve plus le thumb
        row.update(check=True,               
                    doc1 = file,
                    thumb = file_thumb
                    )


@anvil.server.callable
def run_bg_task_reseize_jpg(row):
    task = anvil.server.launch_background_task('reseize_jpg',row)
    return task

"""
**************************************************************** FIN DU PRECESSUS BGT
"""