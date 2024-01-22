import anvil.files
from anvil.files import data_files

#anvil.users
import anvil.tables as tables
#import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# lecture d'1 fichier txt pour en extraire les données
@anvil.server.callable
def file_reading():
    # Read the contents of a file
    cpt=0
    question_txt = ""
    f = open(data_files['qcm1.txt'])              # à fermer en sortie qd ligne vide
    x = True
    while x:
        ligne = f.readline()  # lecture  1 ligne
        if not ligne:
            print(f"question # {cpt}, nb de choix: {nb_de_choix-1}, question:{question_txt}")
            print('Fin du fichier')
            break
        else:
            dernier_caract = ligne[len(ligne)-1:len(ligne)]
            print(f"dernier caract: '{dernier_caract}'")
        
        #print(f"lg: {len(ligne)}")
        n = ligne[0:1] 
        #print(n)
        try:
            num = int(n) # cette ligne est le début d'une question car contient un nombre

            if cpt != 0:
                # SAUVER LA QUESTION et SON NUM et le nb de choix et les réponses 
                print(f"question # {cpt}, nb de choix: {nb_de_choix-1}, question:{question_txt}")
                print()
            nb_de_choix = 0
            dico = {}
            cpt += 1     # incrément du num de question
            #print(f"début question {cpt}")
            # puis effacer la question
            question_txt = ""  # je remets à "" ma question
        except:
            if len(ligne)>4:
                nb_de_choix += 1
                #print(f"except, nb de choix: {nb_de_choix}")
                question_txt = question_txt + ligne
            # créer le dictionnaire qui décrit les reponses (clé est le num de choix, valeur est la réponse si on trouve le caractère "✔" )
    f.close()

       
        


        
            
            
        
