from ._anvil_designer import ItemTemplate4Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

global ancien_num_ligne    # pour pouvoir rendre un bt inactif si perte de focus  
ancien_num_ligne = 0

global cpt   # cpt nb de questions
cpt = 0

global nb_bonnes_rep
nb_bonnes_rep = 0

global max_points
max_points = 0

global points
points = 0      # Je cumule les points en fonction de la réponse et du barême

global reponses
reponses = {}   #liste type dict de toutes les réponses du stagiaire {cle:num, valeurV/F}

class ItemTemplate4(ItemTemplate4Template):
    def __init__(self, **properties):               
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        global max_points
        max_points = 0
        global points
        points = 0      # Je cumule les points en fonction de la réponse et du barême
        global nb_bonnes_rep
        nb_bonnes_rep = 0
        global reponses
        reponses = {}   #liste type dict de toutes les réponses du stagiaire {cle:num, valeurV/F}
        global cpt
        cpt=0
        
        # lecture  user: si user role diff S: mode création 
        user=anvil.users.get_user()
        if user:
            self.admin = user['role']
            if self.admin[0:1]!="S":         # si pas stagiaire
                self.mode= "creation"        # "creation" = mode création/MAJ pas de test stagiaire
            else:
                self.mode = "test"

        # Extraction du numéro de qcm
        self.qcm_nb = self.item["qcm_nb"]    # récup qcm nb
        self.tag.nom = "top"
        self.flow_panel_num.tag.nom = "fp_num"
        self.cp_father.tag.nom = "cp_father"
        self.cp_quest_rep.tag.nom = "cp_quest_rep"
        self.cp_options.tag.nom = "cp_options"
        self.cp_img.tag.nom = "cp_img"
        self.fp_modif.tag.nom = "fp_modif"
        self.fp_vf_barem.tag.nom = "fp_vrai/faux_bareme"
        self.button_fin_qcm.tag.nom = "fin_qcm"
        self.column_panel_results.tag.nom = "cp_results"
        self.label_2.tag.nom = "label_2"
        self.label_3.tag.nom = "label_3"
        self.label_nb_questions.nom = "Label_nb_questions"
        self.label_nb_quest_ok.nom = "Label_nb_questions ok"
        self.label_nb_points.nom = "nb points"
        self.button_enregistrer_et_sortir.tag.nom = "sortir"
        self.column_panel_results.tag.nom = "cp_results"
        self.spacer_1.tag.nom = "spacer"

        # acquisition des réponses
        self.reponse = self.item['rep_multi']             # je sauve la correction de la réponse
        self.nb_options = len(self.item['rep_multi'])     # je sais combien d'options j'utilise pour cette question
        if self.nb_options == 2:   # question V/F 
            self.rep1.tag.nom = "rep1-true"
            self.rep1.tag.numero = self.item['num']
            rep = self.item['rep_multi']   # pour afficher correctement les réponses fauses 
            self.rep1.tag.correction = rep[0:1]   # 1er caractère, correspond à la réponse vrai (0 ou 1)

            self.rep2.tag.nom = "rep2-false"
            self.rep2.tag.numero = self.item['num']
            self.rep2.tag.correction = rep[1:2]   # 2eme caractère, correspond à la réponse vrai (0 ou 1)
       
        self.drop_down_bareme.tag.nom = "bareme"
        
        #recherche nb de questions (sauvées ds temp table)
        self.label_nb_questions.text = user['temp']
        
        self.label_2.tag.nom = "cpt"
        self.label_2.text = self.item['num']
        self.label_2.tag.numero = self.item['num']
        self.label_2.tag.nom = "num"
        qst = self.item['question']
        qst = qst.strip()
        
        if self.mode != "creation":
            if int(self.item['bareme']) > 1:
                self.text_area_question.text = (f"{qst} \n  ({self.item['bareme']} points)")
            else:  # bareme 1 point
                self.text_area_question.text = (f"{qst} \n  ({self.item['bareme']} point)")
            self.text_area_question.enabled = False
        else:
            self.text_area_question.text = qst
            self.text_area_question.enabled = True
            
        self.text_area_question.tag.nom = "question"
        self.text_area_question.tag.numero = self.item['num']
        
        self.text_box_correction.text = self.item['correction']
        self.text_box_correction.tag.nom = "correction"
        self.text_box_correction.tag.numero = self.item['num']
        
        self.drop_down_bareme.items=["1","5"]
        self.drop_down_bareme.selected_value = self.item['bareme']                 
        self.drop_down_bareme.tag.nom = "bareme"
        self.drop_down_bareme.tag.numero = self.item['num']
        
        self.button_modif.tag.numero = self.item['num']          #Je sauve le NUMERO de question ds le tag      
        self.button_modif.tag.nom = "button"
     
        self.image_1.source = self.item['photo']
        self.image_1.tag.nom = "photo"
        self.image_1.tag.numero = self.item['num']
        
        #print(self.mode)
        self.button_fin_qcm.visible = False
        if self.mode != "creation":               # mode utilisation du QCM par le stagiare
            self.text_area_question.enabled = False
            self.file_loader_1.visible = False
            self.text_box_correction.visible = False
            self.drop_down_bareme.enabled = False
            self.button_modif.text = "Validation"
            self.drop_down_bareme.visible = False
            self.button_fin_qcm.visible = False
        else:
            self.button_fin_qcm.visible = False    # mode création, j'affiche la réponse
            self.text_area_question.enable = True  # j'affiche la question text box
            if self.rep1.tag.correction == "1":
                self.rep1.checked = True      
            else:
                self.rep1.checked = False
            if self.rep2.tag.correction == "1":
                self.rep2.checked = True      
            else:
                self.rep2.checked = False            
            self.text_box_correction.visible = True  # j'affiche la correction
       
    def text_area_question_change(self, **event_args):                         # Question a changé (en création QCM)
        """This method is called when the text in this text box is edited"""
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"

    def file_loader_1_change(self, file, **event_args):                         # image a changé (en création QCM)
        """This method is called when a new file is loaded into this FileLoader"""
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_1.source = thumb_pic
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
       
    def drop_down_bareme_change(self, **event_args):                             # Bareme a changé (en création QCM)
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
        global ancien_num_ligne
        ancien_num_ligne = self.drop_down_bareme.tag.numero

    def rep1_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.text_area_question_focus()  

        if self.nb_options == 2:
            if self.rep1.checked == True:   # question V/F
                self.rep2.checked = False
            else:
                self.rep2.checked = True
            
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foreground = "yellow"
        
        global ancien_num_ligne
        ancien_num_ligne = self.rep1.tag.numero

    def rep2_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.text_area_question_focus()

        if self.nb_options == 2:
            if self.rep2.checked == True:   # question V/F
                self.rep1.checked = False
            else:
                self.rep1.checked = True
                
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foreground = "yellow"
            
        global ancien_num_ligne
        ancien_num_ligne = self.rep1.tag.numero
       
    # Bouton modif si mode création  // Validation si mode test qcm pour stagiaire
    def button_modif_click(self, **event_args):   #ce n'est que l'orsque le user a clicker sur modif que je prend le contenu
        """This method is called when the button is clicked"""
        num = self.button_modif.tag.numero           # j'ai le num de la question   
        
        # je récupère mes question, reponse, bareme de la ligne du bouton pressé
        # Je remonte au conteneur parent du bouton (le flow panel)
        
        n1 = self.button_modif.parent    # conteneur fpanel du bt modif
        print("n1",n1)
        #print("n1",n1,n1.nom)
        n2 = n1.parent            # conteneur cpanel : contient cp_img, tb question, tb correction
        print("n2",n2)
        #print("n2",n2,n2.nom)
    
        for cpnt in n2.get_components():   #(contient cp_img, tb question, tb correction)
            print("début boucle cpnt",cpnt.tag.nom)
            if cpnt.tag.nom =="cp_img":
                for cpnt1 in cpnt.get_components():   #( cp_img contient image_1)
                    if cpnt1.tag.nom =="photo":
                        print(cpnt, cpnt.tag.nom)
                        photo = cpnt1.source           # j'ai la photo
                        
            if cpnt.tag.nom == "cp_quest_rep":
                for cpnt1 in cpnt.get_components():
                    print(f"+++++++++++++++++++++++++++++++++++++++++++++++++++++ {cpnt1.tag.nom}")
                    if cpnt1.tag.nom == "question":
                        print(cpnt1, cpnt1.tag.nom)
                        print("mode :", self.mode)
                        question = cpnt1.text
                        # mettre la 1ere lettre en maj mais laisser le reste comme tappé
                        #je boucle à partir de la deuxieme lettre et cumul le text             
                        txt = question[0].capitalize()    # txt commence par la position 1 de la question, mise en majuscule
                        txt2 = question[1:len(question)]  # slice: je prends toute la question à partir de la position 2
                        question = txt + txt2 
                    if cpnt1.tag.nom == "cp_options":
                        rep_multi = ""    # initialisation de la codif des réponses 
                        print(f"+++++++++++++++++++++++++++++++++++++++++++ {cpnt1}, {cpnt1.tag.nom}")
                        for rep in cpnt1.get_components():
                            print(f"+++++++++++++++++++++++++++++++++++++++++++ {rep}, {rep.tag.nom}")
                            
                            if rep.tag.nom == "rep1-true": 
                                print(f"rep1 trouvé {rep.checked}")   
                                if rep.checked == True:
                                    rep_multi = rep_multi + "1"
                                else:
                                    rep_multi = rep_multi + "0"
                                
                            if rep.tag.nom == "rep2-false":
                                print(f"rep2 trouvé {rep.checked}")
                                if rep.checked == True:
                                    rep_multi = rep_multi + "1"
                                else:
                                    rep_multi = rep_multi + "0"
                            reponse = rep_multi                       # J'ai la réponse codée
                            print(f" ++++++++++++++++++++++++++++++++++ rep_multi/reponse: {rep_multi}, ({len(rep_multi)} options)")
                
            if cpnt.tag.nom == "correction":
                print(cpnt, cpnt.tag.nom)
                correction = cpnt.text                                #    j'ai la correction
                
            print("avt test2",cpnt, cpnt.tag.nom)
            if cpnt.tag.nom == "fp_vrai/faux_bareme":                 # fp_vf_barem contient  bareme   
                print("test2", cpnt, cpnt.tag.nom)
                for cpnt2 in cpnt.get_components():   #( cp_img contient image_1)
                        
                        if cpnt2.tag.nom =="bareme":
                            print(cpnt2, cpnt2.tag.nom)
                            bareme = cpnt2.selected_value                 # j'ai le bareme

        qcm_descro_row = self.qcm_nb
        print(qcm_descro_row)
        
        if self.mode == "creation":  # ===================================================  MODE CREATION QCM
            
            result = anvil.server.call('modif_qcm', qcm_descro_row, num, question, reponse, bareme, photo, correction)
            if not result:
                alert("erreur de création d'une question QCM")
                return
            # j'initialise la forme principale
            from anvil import open_form       
            open_form("QCM_visu_modif_Main",qcm_descro_row)
        else:                       # ===================================================  MODE UTILISATION QCM
            self.button_modif.enabled = False
            self.button_modif.visible = False
            
            global nb_bonnes_rep
            global max_points
            global points
            global reponses    # liste type dict
            #global cpt         # compteur de ligne pour afficher le bt 'Fin du Qcm' (on affiche en bas, cpt=1)
            
            valeur=[]  # valeur est la reponse du stagiaire
            if self.nb_options == 2:  # qcm de type v/f
                valeur = reponse
            clef = str(num)           # clé du dict des réponses: numéro de qcm
            reponses[clef] = valeur   # je mets à jour la liste dictionaire des réponses

            #cumul de nb bonnes rep et des points si bonne réponse à partir des tags du combo False
            max_points = max_points + int(bareme)   # cumul du max de points possible
            if self.reponse == reponse:      
                nb_bonnes_rep += 1
                points = points + int(bareme)
   
            if num == int(self.label_nb_questions.text):
                self.button_fin_qcm.visible = True

    def text_area_question_lost_focus(self, **event_args):
        """This method is called when the TextBox loses focus"""
        global ancien_num_ligne
        ancien_num_ligne = self.text_area_question.tag.numero
        
    def text_area_question_focus(self, check_box="", **event_args):
        """This method is called when the TextBox gets focus"""
        num = self.text_area_question.tag.numero
        
        # Je recherche le bouton de l'ancienne ligne pour le désactiver
        #Je remonte du component sur 4 niveaux (jusqu'au repeat panel de la form 'QCM_visu_modif') 
        global ancien_num_ligne
        if ancien_num_ligne != 0 and num != ancien_num_ligne:

            n1 = self.button_modif.parent    # conteneur bt bouton modif (flow panel)     
            print("n1_nom/type; ", n1.tag.nom, type(n1))
            n2 = n1.parent            # conteneur cpanel : contient cp_img, tb question, tb correction
            print("n2_nom/type; ", n2.tag.nom, type(n2))
            n3 = n2.parent
            print("n3_nom/type; ", n3.tag.nom, type(n3))
            repeat_panel = n3.parent  # conteneur des lignes (repeat panel) ds QCM_visu_modi
            print("**** repeating panel ", type(repeat_panel))
        
            for lignes in repeat_panel.get_components():
                print("item_lignes", type(lignes))
                
                for ligne in lignes.get_components():
                    print("cpnts", type(ligne))
                    
                    if ligne.tag.nom == "cp_father":        # control panel incluant img, question, rep, fp_vrai faux
                        for c in ligne.get_components():
                            print("ligne", type(c))
                            print("ligne", c.tag.nom)
                            try:    # text area question et réponses n'ont pas de components
                                """
                                if self.mode != "creation":                         # mode utilisation du QCM uniqt:   
                                    if c.tag.nom ==  "fp_vrai/faux_bareme": 
                                            for cpnt in c.get_components():    # je suis ds le fp bareme qui contient le bareme et reponses v/f
                                                print("ligne en utilisation **********************************************",cpnt.tag.numero,'ancien num',ancien_num_ligne)
                                                
                                                if cpnt.tag.nom == "rep_true" and cpnt.tag.numero == ancien_num_ligne:
                                                    alert(f"Validez d'abord la question {ancien_num_ligne}")
                                                    print("CHECK BOX REP TRUE ANCIENNE LIGNE", ancien_num_ligne)
                                                if cpnt.tag.nom == "rep_false":
                                                    print("CHECK BOX REP FALSE ANCIENNE LIGNE", ancien_num_ligne)
                                                #ancien_num_ligne = 0
                                """    
                                if c.tag.nom == "fp_modif":     # je suis ds le fp bareme qui contient le bouton modif/valid
                                    for cpnt in c.get_components():   
                                        print("ligne  **********************************************",cpnt.tag.numero,'ancien num',ancien_num_ligne)
                                        if cpnt.tag.nom == "button" and cpnt.tag.numero == ancien_num_ligne:                    # <=============  mode utiiisation qcm
                                            print("=============================================================== ok bouton ancienne ligne trouvé")
                                            #c'est le bt de l'ancienne ligne
                                            cpnt.enabled = False
                                            cpnt.background = "theme:On Primary Container"
                                            cpnt.foregroundground = "theme:On Primary"
                                            ancien_num_ligne = 0
                            except:
                                pass    # pour les éléments ne contenant pas de d'éléments en eux

  
                
    def text_box_correction_focus(self, **event_args):
        """This method is called when the text area gets focus"""
        self.text_area_question_focus()

    def text_box_correction_lost_focus(self, **event_args):
        """This method is called when the text area loses focus"""
        self.text_area_question_lost_focus()

    def text_box_correction_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.text_area_question_change()
    
    def button_fin_qcm_show(self, **event_args):
        """This method is called when the Button is shown on the screen"""
        global cpt    # cpt = nb de questions  
        cpt += 1
             
    def button_fin_qcm_click(self, **event_args):
        """This method is called when the button is clicked"""
        from InputBox.input_box import InputBox, alert2, input_box, multi_select_dropdown
       
        # enregistrement des résultats ds table qcm_results
        global nb_bonnes_rep
        global max_points
        global points
        global reponses     # liste type dict  des réponses du stagiaire    
        #alert(f"liste réponses contient : {len(reponses)}")
        if len(reponses) != int(self.label_nb_questions.text):
            r=alert2('Ce QCM est inachevé, \n\n'
                      'Voulez-vous vraiment abandonner ?\n'
                      ,
                buttons=['Oui', 'Non'],
                default_button='Non',    
                large=True
                )
            if r == "Oui" :                    
                self.button_enregistrer_et_sortir_click()
            else:
                return
                
        self.button_fin_qcm.visible = False               
        user=anvil.users.get_user()
        if user:
            result = anvil.server.call("qcm_result", user, self.qcm_nb, nb_bonnes_rep, max_points, points, reponses)  
            if result == False :
                alert("QCM non enregisté !")
                
        # affichage des résultats   
        self.label_nb_quest_ok.text = (f"{nb_bonnes_rep} bonnes réponses sur {self.label_nb_questions.text}.")
        self.label_nb_points.text = (f"{points} points obtenus sur {max_points} possibles.")
        self.column_panel_results.visible = True 

        #affichage des corrections
        n1 = self.button_fin_qcm.parent    # conteneur bt bouton fin qcm (self) 
        print("n1", type(n1))
        print("n1_nom; ", n1.tag.nom)
        
        repeat_panel = n1.parent  # conteneur des lignes (repeat panel) ds QCM_visu_modi
        print("**** repeating panel *****", type(repeat_panel))
        
        for lignes in repeat_panel.get_components():
            print("item_lignes", type(lignes))
            for cpt in lignes.get_components():
                print("cpnts", type(cpt))
                
                if cpt.tag.nom == "cp_father":
                    for c in cpt.get_components():
                        print("c", type(c))
                        print("c", c.tag.nom)
                        
                        if c.tag.nom == "correction" :
                            c.visible = True
                            c.enabled = False
                            
                        if c.tag.nom ==  "fp_vrai/faux_bareme": 
                            for cpnt in c.get_components():    # je suis ds le fp bareme qui contient le bareme et reponses v/f
                                if cpnt.tag.nom == "rep_true":
                                    num_ligne = cpnt.tag.numero                  # barem et spacer n'ont pas de tag numero
                                    if reponses[str(num_ligne)] == "10":
                                        print("================================================================> ok")
                                        print("cpnt", type(cpnt))
                                        print("reponse doir être :", self.reponse)
                                        cpnt.enabled = True
                                        cpnt.foreground = "yellow"
                                        if cpnt.tag.correction != "10":
                                            cpnt.background = "red"                               
                                        cpnt.checked = True
                                if cpnt.tag.nom == "rep_false":
                                    num_ligne = cpnt.tag.numero
                                    if reponses[str(num_ligne)] == "01":
                                        print("================================================================> ok")
                                        print("cpnt", type(cpnt))
                                        print("reponse doit être :", self.reponse)
                                        
                                        cpnt.enabled = True
                                        cpnt.foreground = "yellow"
                                        if cpnt.tag.correction != "01":
                                            cpnt.background = "red"  
                                        cpnt.checked = True
                                        
                        if c.tag.nom == "cp_quest_rep":
                            for cpnt1 in c.get_components():
                                print(f"++++++++++++++++++++++++++++++++++++   correction  ++++++++++++++ {cpnt1.tag.nom}")
                                if cpnt1.tag.nom == "question":
                                    pass
                                if cpnt1.tag.nom == "cp_options":
                                    print(f"+++++++++++++++++++++++++++++++++++++++++++ {cpnt1}, {cpnt1.tag.nom}")
                                    for rep in cpnt1.get_components():
                                        print(f"+++++++++++++++++++++++++++++++++++++++++++ {rep}, {rep.tag.nom}")
                                        num_question = rep.tag.numero
                                        # acquisition de la réponse du stagiaire en lisant le dictionaire avec clef numero de question                                      
                                        rep_stagiaire = reponses[str(num_question)]
                                        
                                        if rep.tag.nom == "rep1-true":   
                                            # si réponse stagiaire diff de la correction, j'affiche rouge la réponse fausse
                                            print(f"{rep_stagiaire} {self.reponse}")
                                            # comparaison et affichage si cheched
                                            if rep_stagiaire != self.reponse and rep.checked == True:
                                                rep.background = "red"
                                            if rep_stagiaire == self.reponse and rep.checked == True:
                                                rep.background = "green"
                                                
                                        if rep.tag.nom == "rep2-false":
                                            # comparaison et affichage si cheched
                                            print(f"{rep_stagiaire} {self.reponse}")
                                            if rep_stagiaire != self.reponse and rep.checked == True:
                                                rep.background = "red"
                                            if rep_stagiaire != self.reponse and rep.checked == True:
                                                rep.background = "green"
            
                    
    def button_enregistrer_et_sortir_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ...Main import Main
        open_form('Main',99)

    def column_panel_results_show(self, **event_args):
        """This method is called when the column panel is shown on the screen"""
        self.column_panel_results.scroll_into_view()










                              

            




        

   
        


    

        

    

        




 


        
        