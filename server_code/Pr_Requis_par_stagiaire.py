#from anvil import *
import pathlib
import anvil.files
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from PIL import Image
import io
import math

@anvil.server.callable
def path_info(file):
    path = pathlib.Path(file)
    return str(path.parent), str(path.name), str(path.suffix)  # path, file name, extension

# ===============================================================================================================
# liste des STAGIAIRES (ADMIN  pour afficher ts les stagiaires d'1 stage et ensuite voir leurs docs prérequis 
#     Pour lecture fichier père users: self.item['user_email']
#     Pour lecture fichier père stages: self.item['stage']
@anvil.server.callable
def preparation_liste_pour_panels_stagiaires(row_stage):
    # lecture des stagiaires de ce stage
    liste_stagiaires = app_tables.stagiaires_inscrits.search(q.fetch_only("user_email", "name"),
                                                            stage=row_stage
                                                            )
    return liste_stagiaires




# ===============================================================================================================
# PRE-REQUIS STAGIAIRES (ADMIN  voir leurs docs prérequis)
#     Pour lecture fichier père users: self.item['user_email']
#     Pour lecture fichier père stages: self.item['stage']
@anvil.server.callable
def preparation_liste_pour_panels_pr(user_email, stage):
    liste_pr = app_tables.pre_requis_stagiaire.search( q.fetch_only("item_requis", "doc1", "stagiaire_email"),
                                                        stagiaire_email = user_email,        # user_email row
                                                        stage_num = stage                    # stage      row
                                                        )
    list(liste_pr).sort(key=lambda x: x["item_requis"]["code_pre_requis"])      # TRI par code pré requis
    return liste_pr



@anvil.server.callable
@anvil.tables.in_transaction
def modify_pre_r_par_stagiaire(stage_num, item_requis, email, file, new_file_name, file_extension):
    #print("file_extension", file_extension)
    #print("new_file-NAME: ", new_file_name)
    valid=False
    pr_requis_row = app_tables.pre_requis_stagiaire.get( q.fetch_only(),
                                                         stage_num = stage_num,          # stage row
                                                         stagiaire_email = email,       # user row
                                                         item_requis = item_requis      # item_requi row                                      
                                             ) 
    if pr_requis_row:
        if file_extension == ".jpg":
            print("serveur Preq: Ce fichier est une image JPG")        
            new_file_name = new_file_name + file_extension

            #-------------------------------------------------------------------------------- à Remplacer par 1 B.G. task / loop traitmt images
            # Img file, Convert the 'file' Media object into a Pillow Image
            img = Image.open(io.BytesIO(file.get_bytes()))
            width, height = img.size
            #print('size', width, height)
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
            #print('new_size', width, height)
            
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
            valid=True
            return True
    else:
        return False


# ===============================================================================================================
# PRE-REQUIS STAGIAIRES, Effacement d'un pré-requis OU destruction
@anvil.server.callable
def pr_stagiaire_del(user_email, stage, item_requis, mode="efface"):
    pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = stage,          # stage row
                                                         stagiaire_email = user_email,       # user row
                                                         item_requis = item_requis      # item_requi row                                      
                                             ) 
    if pr_requis_row and mode=="efface":
        pr_requis_row.update(check=False,               
                                doc1 = None,
                                pdf_doc1 = None
                                )
        return True
    if pr_requis_row and mode=="destruction":
        pr_requis_row.delete()
        return True
    return False
    

