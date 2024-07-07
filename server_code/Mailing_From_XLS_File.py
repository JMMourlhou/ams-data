import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.files
from anvil.files import data_files


@anvil.server.callable
def xls_file_reader(csv_file_name):
    
    f = open(data_files[csv_file_name])    
    x = True

    while x:
        ligne = []
        text=f.readline()  # lecture  1 ligne
        if not text:                                        # FIN DE FICHIER TEXT           #rep = rep + dernier_caract
            print('Fin du fichier')
            break
        
        #remplacement ; par , 
        ligne = text.split(';')
        # extraction du mail
        mail=ligne[1]
        #extraction du num
        num=ligne[0]
        app_tables.stagiaires_histo.add_row(mail=mail,
                                            num=num)
    



    """
    wb = openpyxl.load_workbook(f)
    sheet = wb[wb.sheetnames[0]]
    print("feuille 1:", sheet)
    cell=sheet(["A1"])
    return cell
    """