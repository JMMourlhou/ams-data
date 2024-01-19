
import anvil.files
from anvil.files import data_files

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def file_reading():
    # Read the contents of a file
    with open(data_files['qcm1.txt']) as f:
        ligne = f.readline()   # numero 1ere question en 1er
        #print("nb de lignes:", len(fichier)) 
        num = ligne[0:2]   
        print(num)

        question_nb = 1
        question_txt = ""

        
        ligne=f.readline()    #lecture 2eme ligne : début question ?
        while ligne == "":
              ligne=f.readline()    #lecture next line
            
        while ligne != "":      #début question
            question_txt = question_txt + str(ligne) 
            ligne=f.readline()   
        print(f"question # {question_nb} : {question_txt}")

        # il y a eu une ligne vide, # ligne : début prochaine question ?
        ligne=f.readline()    
        while ligne == "":
              ligne=f.readline()    #lecture next line

        
            
            
        
