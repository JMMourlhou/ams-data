import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.pdf import PDFRenderer

@anvil.server.callable
def add_ligne_qcm(num_question, question, correction, rep, bareme, image, qcm_nb, type, param):
    
    # qcm_nb est la row venant du dropdown choix du qcm
   
    new_row=app_tables.qcm.add_row(num= int(num_question),
                                   question = question,
                                   correction = correction,
                                   rep_multi = rep,
                                   bareme = str(bareme),
                                   photo = image,
                                   qcm_nb = qcm_nb,
                                   type = type,
                                   param = param)

            
    qcm_row = app_tables.qcm.search(qcm_nb = qcm_nb,
                                    num=num_question
                                    )
    if qcm_row:
        valid=True
    else:
        valid=False
    return valid

# =================================================================================================================
# MODIF du QCM (en maj d'un qcm)
@anvil.server.callable           #modif d'une ligne de Qcm
def modif_qcm(qcm_descro_row, num_question, question, rep, bareme, photo, correction):

    # lecture de la ligne à modifier par son numéro             
    qcm_row = app_tables.qcm.get(num=num_question,
                                qcm_nb=qcm_descro_row)
    if not qcm_row:
        print("Ligne qcm non trouvée ds fichier qcm")
        return False
    else:   
        rep_multi = rep
        qcm_row.update(question = question,
                     rep_multi = rep,
                     bareme = str(bareme),
                     photo = photo,
                     correction= correction
                    )
        return True

# =================================================================================================================
# Delete d'1 ligne du QCM (en mode maj d'un qcm)
@anvil.server.callable           #modif d'une ligne de Qcm
def delete_qcm(qcm_descro_row, num_question):
    # lecture de la ligne à enlever par son numéro             
    quest_qcm = app_tables.qcm.get(num=num_question,
                                   qcm_nb=qcm_descro_row)
    if not quest_qcm:
        print("Ligne qcm non trouvée ds fichier qcm")
        return False
    else:   
        #------------------------------------------------------------- tranfert/ ds le qcm 16 de la question annulée
        """
        w_sur_qcm_nb = 16
        r = app_tables.qcm_description.get(qcm_nb=w_sur_qcm_nb)   # acquisition du row du qcm
        liste_qcm_cible = app_tables.qcm.search(qcm_nb=r)
        if liste_qcm_cible: 
            nb_lignes_qcm_cible = len(liste_qcm_cible)
        else:
            nb_lignes_qcm_cible = 0

        num_question = nb_lignes_qcm_cible + 1
        question = quest_qcm['question']  
        correction = quest_qcm['correction']
        rep = quest_qcm['rep_multi']
        bareme = quest_qcm['bareme']
        image = quest_qcm['photo']
        qcm_nb = r
        type = quest_qcm['type']
        param = quest_qcm['param']
        
        result = add_ligne_qcm(num_question, question, correction, rep, bareme, image, qcm_nb, type, param)
        if not result:
            print("Erreur en copy/delete de ligne")
            return
        """
        #-------------------------------------------------------------
        quest_qcm.delete()        
        return True

# ==================================================================================================
# modify the question number of the qcm questions after a deletion of a question
# ==================================================================================================
@anvil.server.callable
def renumber_qcm(qcm_descro_row):
#lecture fichier père qcm descro
        table = app_tables.qcm.search(qcm_nb=qcm_descro_row)
        result=False
        cpt = 0
        if table:
            for row in table:
                cpt += 1
                row.update(num = cpt
                          )
            result=True
        param_table_qcm = qcm_descro_row["destination"]
        print(f"loop Re-numération après delete ds table {param_table_qcm}: {result}")
        return result    

# =====================================================================================================================
#                 UTILISATION DU QCM PAR UN STAGIAIRE, SAUVEGARDE DES RESULTATS DS table.qcm_result
# =====================================================================================================================
# ENREGITREMENT, en fin de questions du QCM pour un stagiaire
@anvil.server.callable 
@anvil.tables.in_transaction
def qcm_result(user, qcm_numero, nb_bonnes_rep, max_points, points, reponses):      # debut: debut de qcm, enregt du num et user
    import French_zone_server_side
    nb_questions = len(reponses)
    if nb_questions == 0:
        valid = False
        return
    p100_sur_nb_rep = int(nb_bonnes_rep / nb_questions * 100)    # Ce résultat permet de débloquer le prochain QCM si il y en a un 
    p100_sur_points = int(points / max_points * 100)

    # lecture fichier qcm_decription
    qcm_row=app_tables.qcm_description.get(qcm_nb=qcm_numero)

    # si résultat en % >= résultats requis pour réussite ds qcm_descro : je valide le prochain qcm (si colonne next_qcm non vide): je change le dict ds stagiaire_inscrit
    success = False                            # initialisation du success à False
    if qcm_row:
        seuil = qcm_row['taux_success']
        #print("seuil :", seuil)
        if p100_sur_nb_rep >= seuil:
            success = True                     # success TRUE
            #recherche du qcm suivant éventuel
            if qcm_row['next_qcm'] != None:
                next_qcm = str(qcm_row['next_qcm'])   
                #print("next qcm: ", next_qcm)
                
                # je recherche les stages du user à partir de son mail
                liste_stages_stagiaire = app_tables.stagiaires_inscrits.search(user_email=user)
                if liste_stages_stagiaire:
                    for st in liste_stages_stagiaire:
                        print(st['stage']['code']['code'])
                        dict = st['droits_stagiaire_qcms']
                        print("dict droits stagiaire :", dict)
                        try:
                            valeur = dict.get(next_qcm)
                            #print(" ----  next qcm: ", next_qcm)
                            #print(" ----  valeur: ", valeur)
                            
                            new_valeur = [valeur[0],"True"]
                            dict[next_qcm] = new_valeur   #réaffectation de cette clé
                            st.update(droits_stagiaire_qcms = dict)
                        except:
                            pass
    
    app_tables.qcm_result.add_row(
                                    user_qcm= user,
                                    name = user['nom'],
                                    prenom = user['prenom'],
                                    qcm_number=qcm_row,
                                    intitule=qcm_row['destination'],
                                    time= French_zone_server_side.time_french_zone(),
                                    liste_rep = reponses,
                                    nb_rep_ok = nb_bonnes_rep,
                                    p100_sur_nb_rep = p100_sur_nb_rep,
                                    p100_sur_points = p100_sur_points,
                                    success = success
                            )

    qcm_result_row = app_tables.qcm_result.search(qcm_number = qcm_row,
                                                  user_qcm= user,
                                            )
    if qcm_result_row:
        valid=True
    else:
        valid=False
    return valid


# ==================================================================================================
# modify the column temp of table user during qcm (nb of questions)
# ==================================================================================================
@anvil.server.callable
def temp_user_qcm(user, nb_questions_in_qcm, numero_qcm):
    #user.update(temp = int(nb_questions_in_qcm))
    result = False
    if user:
        try:
            user.update(temp = int(nb_questions_in_qcm),        # temp2 contient 'test' si le concepteur a testé son qcm     
                        temp3 = str(numero_qcm)                 # temp3 contient num du qcm réel
                       )                                        # temp contient le nb de questions
            result = True
        except:
            result = False
    return result

# Génération du pdf des résultats du QCM
@anvil.server.callable
def create_qcm_plot_pdf(user, nb, visu_next_qcm = False, visu_legend=False):     # nb : num du qcm
    #from anvil.pdf import PDFRenderer
    """
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
    "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """

    media_object = PDFRenderer(page_size ='A4',
                               filename = "resultat_qcm.pdf",
                               landscape = False,
                               margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  # en cm
                               scale = 1,
                               quality =  "default"
                              ).render_form('Plot',user, nb, visu_next_qcm, visu_legend)
    return media_object

# ------------------------------------------------------------------------------------------------------------------
# ajout d'un droit au qcm pour un stage, table codes_stages, appelé en paramètres par QCM_par_stage / template 18
@anvil.server.callable
def modif_qcm_stage(nb, qcm_descro, stage, visible): # nb: int, num du qcm    stage: stage row ds table  codes_stages    visible: Qcm visible ? True / False
    # préparation de l'option visible ou pas ds la valeur de la clé
    if visible is True:  # la valeur est "True", le qcm est visible dès l'accès du stgiaire au menu QCM
        visu = "True"
    else:
        visu = "False"
        
    # création de la clé / valeur
    cle = str(nb) # clé du QCM doit être str
    valeur = [qcm_descro, visu]   # intiltulé du QCM

    # lecture dictionnaire des qcm ds la table 
    dict={}  
    dict = stage["droit_qcm"]
    if dict is None or dict == {}:
        dict={}    
    print(f"dico: {str(dict)}")
     # ajout du qcm ds le dictionaire
    dict[cle]=valeur
    
    # sauvegarde du dict
    stage.update(droit_qcm=dict)
    

# ------------------------------------------------------------------------------------------------------------------
# effact d'un droit au qcm pour un stage, table codes_stages, appelé en paramètres par QCM_par_stage / template 19
@anvil.server.callable
def del_qcm_stage(nb, stage): # nb: int, num du qcm    stage: stage row ds table  codes_stages   
    
    # création de la clé 
    cle = str(nb) # clé du QCM doit être str

    # lecture dictionnaire des qcm ds la table 
    dict={}  
    dict = stage["droit_qcm"]
    
     # del du qcm ds le dictionaire
    del dict[cle]
    
    # sauvegarde du dict
    stage.update(droit_qcm=dict)

# ------------------------------------------------------------------------------------------------------------------
# modif table qcm descro, qcm d'un stage sélectionné
@anvil.server.callable
def modif_qcm_descro_pour_un_stage(nb, visible, taux_success, next_qcm): # nb: int, num du qcm    stage: stage row ds table  codes_stages   
    
    # lecture du qcm row, table qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=nb)
    
    # sauvegarde du dict
    if len(qcm_row)>0:
        qcm_row.update(
                        visible=visible,
                        taux_success = taux_success,
                        next_qcm=next_qcm
                        )