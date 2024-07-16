import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.files
from anvil.files import data_files


@anvil.server.callable
def xls_file_reader(csv_file):
    
    f = open(data_files[csv_file.name])    # csv_file est : file du file loader. RAJOUTER .name ici pour obtenir on nom
    x = True
    nb = 0 # Nb de mails ajoutés

    while x:
        ligne = []
        text=f.readline()  # lecture  1 ligne
        if not text:                                        # FIN DE FICHIER TEXT           #rep = rep + dernier_caract
            print('Fin du fichier')
            return('Fin du fichier',nb)
        
        # création d'une liste, à prtir du séparateur ";"
        ligne = text.split(';')
        
        num=ligne[0]           # extraction du num ligne excel
        mail=ligne[1]          # extraction du mail
        date_diplome=ligne[2]  # extraction date du diplome
        nom=ligne[3]           # extraction du nom
        prenom=ligne[4]        # extraction du prenom
        date_naissance=ligne[5]  # extraction date N
        lieu_naissance=ligne[6]  # extraction lieu N
        rue=ligne[7]             # extraction rue
        cp=ligne[8]             # extraction cp
        ville=ligne[9]          # extraction ville
        tel=ligne[10]            # extraction du tel

        # je recherche si un doublon existe déjà
        row = app_tables.stagiaires_histo.get(mail=mail)
        if row:                            # DOUBLON, le mail existe déjà
            if diplome == "PSE2":
                # je mets à jour le diplome
                row.update(diplome="PSE2")
        else:                              # mail innexistant, je l'ajoute
            nb += 1
            app_tables.stagiaires_histo.add_row(mail=mail,
                                                num=num,
                                                date_diplome=date_diplome,
                                                nom=nom,
                                                prenom=prenom,
                                                date_n=date_naissance,
                                                lieu_n=lieu_naissance,
                                                rue=rue,
                                                ville=ville,
                                                cp=cp,
                                                tel=tel
                                            )
    """
    wb = openpyxl.load_workbook(f)
    sheet = wb[wb.sheetnames[0]]
    print("feuille 1:", sheet)
    cell=sheet(["A1"])
    return cell
    """

# MAJ du l'envoi à partir de Mai_to_old_stagiaires (Coche Envoi a changé)
@anvil.server.callable
def maj_histo_envoi(item, envoi):   # item de l'enregistrement d'un ancien stagiare 
    item.update(envoi=envoi)
    return True

# del d'une row d'un ancien stgiaire  à partir de  Mai_to_old_stagiaires
@anvil.server.callable
def del_histo(item):   # item de l'enregistrement d'un ancien stagiare 
    item.delete()
    return True

# MAJ de la sélection à partir de Mail_to_old_stagiaires (Coche Envoi a changé)
@anvil.server.callable
def maj_selection(item, select):   # item de l'enregistrement d'un ancien stagiare 
    item.update(select=select)
    return True