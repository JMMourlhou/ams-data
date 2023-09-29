from ._anvil_designer import Qcm_visuTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from Pillow import ImageGrab
from anvil.js import window # to gain access to the window object
from anvil_extras.PageBreak import PageBreak
global etat_faux
etat_faux = None
global etat_vrai
etat_vrai = None
global former_screen_size
former_screen_size = window.innerWidth
global timer
timer = False

class Qcm_visu(Qcm_visuTemplate):
    def __init__(self, pdf_mode=False, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        img = ImageGrab.grab()
        alert(img)
        
        if pdf_mode == True:    # Efface les Bouttons
            self.button_retour.visible = False
            self.button_validation.visible = False
            self.button_pdf.visible = False
             # lecture de la liste que j'ai stocké à partir du user
            user=anvil.users.get_user()
            if not user:
                alert("Pas d'utilisateur")
                return
            #print(user['email'])
            stagiaire_row = app_tables.stagiaires_inscrits.get(user_email=user)
            if not stagiaire_row:   
                print("stagiaire inscrit non trouvé")
            liste_rep_sauvée = stagiaire_row["qcm_list"]
            #print(reponses)
            
        self.label_titre.text = "QCM PSE1"
        #lecture du fichier QCM    
        rows = list(app_tables.qcm.search())
            #tables.order_by("name", ascending=True),
            #stage=stage_row
        #))
        self.nb_questions = len(rows)
        """ ***********************************  SCREEN SIZING **********************************"""
        
        self.screen_width = window.screen.width    #text
        self.screen_height = window.screen.height
        self.browser_width = window.innerWidth         
        self.browser_height = window.innerHeight
        self.label_browser_width.text = self.browser_width
        window.onresize = self.screen_resize()
        self.xy_panel.width =  self.screen_width             # largeur de l'xy panel           
        
        self.xy_panel.height = self.nb_questions *185   # hauteur de l'xy panel
        #print("nb-questions", nb_questions)
        xx = 1   # position (x=1, y=1)
        yy = 1
        hauteur_entre_question = 10 
        largeur_espace = 50   #espace de l'espace entre combobox
        cpt_ligne = 0

        "======================== BOUCLE sur le nb questions ds liste =========================================="
        for row in rows :
            question = str(row["num"])+"-   "+row['question']
            self.nb = row["num"] 
            cpt_ligne += 1  # compteur
                        
            # Création du column panel de la question et check boxes
            self.cp = ColumnPanel(role="outlined-card",
                            background="theme:Primary",
                            wrap_on="mobile",
                            spacing_above="small",
                            spacing_below="small",
                            )
            self.cp.tag.nom = "column"
            self.xy_panel.add_component(self.cp, x=xx, y=yy, width=self.browser_width)
            
            
            # Création de la question ds le column panel
            self.quest = TextArea(text=question,
                        enabled=False,
                        align="left",
                        font_size=14,
                        background="theme:Primary",     
                        foreground="theme:On Primary",
                        auto_expand=True,
                        spacing_above=None,
                        spacing_below=None,
                        height=120
                        )
            self.quest.tag.nom = "question"
            self.cp.add_component(self.quest, x=xx+5, y=yy, width="default")

            # Création du flow panel ds le column panel
            self.fp = FlowPanel(align="center")
            self.fp.tag.nom = "flow_panel"
            self.cp.add_component(self.fp, full_width_row=True)
        
            # Création de l'espace avant le Check box Vrai
            self.space1=Spacer(height=5, width=50, spacing_above=None, spacing_below=None)
            self.space1.tag.nom = "space"
            self.fp.add_component(self.space1)
        
            
            # Création Check box Vrai ds le flow panel pour créer le tag et reconnaitre quelle question est chekée 
            self.cb_true = CheckBox(text="Vrai",
                                    checked=None,
                                    allow_indeterminate=True,
                                    spacing_above=None,
                                    spacing_below=None,
                                    enabled=True
                                    )
            self.cb_true.tag.nom = "cb_true"
            self.cb_true.tag.num_question = row['num']
            self.fp.add_component(self.cb_true)
            self.cb_true.set_event_handler('change',self.check_box_true_change)
            # si mode PDF
            if pdf_mode == True and liste_rep_sauvée[cpt_ligne-1][1]==True :   # et si la reponse du stagiaire était Vraie
                self.cb_true.checked=True
                
        
            # Création de l'espace entre les 2 Check boxes
            self.space2=Spacer(height=5, width=50, spacing_above=None, spacing_below=None)
            self.space2.tag.nom = "space"
            self.fp.add_component(self.space2)

            # Création Check box Faux ds le flow panel pour créer le tag et reconnaitre quelle question est chekée 
            self.cb_false = CheckBox(text="Faux",
                                    checked=None,
                                    allow_indeterminate=True,
                                    spacing_above=None,
                                    spacing_below=None,
                                    enabled=True
                                    )
            self.cb_false.tag.nom = "cb_false"
            self.cb_false.tag.num_question = row['num']
            self.cb_false.tag.bareme = row['bareme']    # Je sauve le bareme de la question ds tag de combo false
            self.cb_false.tag.bonne_rep = row['reponse']    # Je sauve le bareme de la question ds tag de combo false
            self.fp.add_component(self.cb_false)
            
            self.cb_false.set_event_handler('change',self.check_box_false_change)
            # si mode PDF
            if pdf_mode == True and liste_rep_sauvée[cpt_ligne-1][1]==False :   # et si la reponse du stagiaire était Vraie
                self.cb_false.checked=True
            """
            # si ligne mutiple de 6, je saute une ligne, n'affecte pas l'affichage normal en mode non pdf
            if pdf_mode == True and cpt_ligne % 6 == 0 : # (modulo 6) 
                #alert("ST")
                self.xy_panel.add_component(PageBreak(), x=1, y=yy + 1)      # si en création de pdf, je saute une page ts les 6 stagiares 
            """
            #fin de boucle, je calcule la hauteur du column panel qui vient d'être créé (evariable en fonction largeur écran et nb de lignes question)
            #w = c.get_width()
            #h = c.get_height()
            flowpanel = self.cb_false.parent    # conteneur d'1 ligne 
            col_panel = flowpanel.parent    # conteneur objet de la question (col panel)
            """
            for cpnt in col_panel.get_components():
                if cpnt.tag.nom == "question":
                    hauteur_quest=cpnt.width                
                    hauteur_quest=int(hauteur_quest)
                    print("hauteur", hauteur_quest)
            """
            #yy = yy + hauteur_quest + 100 + hauteur_entre_question
            yy = yy + 120 + 100 + hauteur_entre_question
            
            #yy += 170
        else:
            """ si pas de questions """
            print("pas de question")
            
    """ Gestion des évenements click sur combo box, extraction grace au TAG """
    def check_box_true_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        """ contenu du dictionaire event_args 
        {'button': 1, 'keys': {'meta': False, 'shift': False, 'ctrl': False, 'alt': False}, 'sender': <anvil.Image object>, 'event_name': 'mouse_down'}"""
       
        tag = event_args["sender"].tag   # j'extrais le tag du sender (le num de la question)
        print("tag: ",tag, type(tag))       
        check_box_changed = event_args['sender']
        #pour récupérer la check_bocx false et la mettre unchecked, je remonte au component parent (le flow panel)
        flowpanel = check_box_changed.parent
        for cpnt in flowpanel.get_components():
            print(cpnt, cpnt.tag)
            if cpnt.tag.nom =="cb_false":
                cpnt.checked = False
        # maj dico connaissant la ligne, l'état

    def check_box_false_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        tag = event_args["sender"].tag   # j'extrais le tag du sender (le num de la question)

        check_box_changed = event_args['sender']
        #pour récupérer la check_bocx false et la mettre unchecked, je remonte au component parent (le flow panel)
        flowpanel = check_box_changed.parent
        for cpnt in flowpanel.get_components():
            print(cpnt, cpnt.tag)
            if cpnt.tag.nom =="cb_true":
                cpnt.checked = False

    def button_retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def button_validation_click(self, **event_args):
        """This method is called when the button is clicked"""
        """ Boucle pour 1- savoir si question non répondue
                        2- ds la boucle créer un dictionnaire réponse
                        
                        3- calculer le résultat en lisant le dico
                        4- sauver le dico ds la table stagiaire_inscrit
        """
        nb_bonnes_rep = 0
        max_points = 0
        points = 0      # Je cumule les points en fonction de la réponse et du barême
        reponses = []   #liste de toutes les réponses du stagiaire {"num":   , "reponse":   }
        # 1 Boucle sur les flow panels  ET cré le dictionaire
        for col_p in self.xy_panel.get_components():  #ds column panel
            print(col_p.tag.nom)

            for fl_p in col_p.get_components():   #ds flow panel
                print(fl_p.tag.nom)

                for cpnt in fl_p.get_components():   # ds chaque cpnt du flow panel
                    print(cpnt.tag.nom)
                    if cpnt.tag.nom == "cb_true":
                        numero_question = cpnt.tag.num_question
                        global etat_vrai
                        etat_vrai = cpnt.checked     #je sauve l'état du combo vrai                                        # je mets à jour la liste  
                            
                    if cpnt.tag.nom == "cb_false":     #si je suis sur le cobo Faux...
                        global etat_faux
                        etat_faux = cpnt.checked   #je sauve l'état du combo faux                       
                        
                        if etat_faux==None and etat_vrai==None:
                            alert(f"La question {numero_question} n'a pas été répondue")
                            return

                        rep_stagiaire = False
                        rep=()
                        if etat_vrai == False:       # le stagiaire a répondu False
                            rep=[numero_question,False]
                            rep_stagiaire = False
                        else:
                            rep=[numero_question,True]    # le stagiaire a répondu True
                            rep_stagiaire = True
                        reponses.append(rep)      # je mets à jour la liste    
                        #alert(reponses)

                        #cumul de nb bonnes rep et des points si bonne réponse à partir des tags du combo False
                        max_points = max_points + int(cpnt.tag.bareme)    # cumul du max de points possible
                        if cpnt.tag.bonne_rep == rep_stagiaire:
                            nb_bonnes_rep += 1
                            points = points + int(cpnt.tag.bareme)
                            
        
        #sortie de boucle ds mes questions, affichage du résultat
        pour_cent = round(nb_bonnes_rep/self.nb_questions*100,2)
        pour_cent_bareme = round(points/max_points*100,2)
        alert(f"Vous avez eu {nb_bonnes_rep} bonnes réponses sur {self.nb_questions} soit {pour_cent} % ! ... ")
        alert(f"... et {points} points sur {max_points} possibles, soit {pour_cent_bareme} % ! ")
        
        print("num question 2:",reponses[2-1][0])  # (0=1ere,1=2eme) 
        print("réponse 2:",reponses[2-1][1])  # 
        print("num question 3:",reponses[3-1][0])  # 
        print("rep 3:",reponses[3-1][1])  # 
        
        # sauvegarde du dico à partir du user
        user=anvil.users.get_user()
        if user:
            print(user['email'])
            # envoi en serveur module pour sauver le qcm ds la table stgiaire inscrit (à partir du stage, user_email, list du qcm
            result = anvil.server.call("save_qcm", user["email"], pour_cent_bareme, reponses)     
            if result:
                alert("liste QCM enregistrée dans votre fichier")
                from ..Main import Main   #retour au menu
                open_form('Main',99)
            else:
                alert("Erreur; liste QCM non sauvegardée")
                return
        else:
            alert("Stagiaire non trouvé")
            return

    

    def button_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        media_object_pdf = anvil.server.call("print_pdf",True)  #pdf mode = True
        anvil.media.download(media_object_pdf)

    def maj_liste_pdf(self):
        pass

    def screen_resize(self):
        """This method is called when the screen is resizing"""
        self.screen_width = window.screen.width    #text
        #self.screen_height = window.screen.height
        #self.browser_width = window.innerWidth         
        #self.browser_height = window.innerHeight
        self.label_browser_width.text = self.browser_width
        global former_screen_size
        if former_screen_size != self.screen_width:
            self.xy_panel.width =  self.screen_width             # largeur de l'xy panel  
            former_screen_size = self.screen_width 

    def timer_1_tick(self, **event_args):
        """This method is called Every 0.5 seconds. Does not trigger if [interval] is 0."""
        self.innerWidth = window.innerWidth    #text
        
        global timer
        if timer == False:
            self.label_browser_width.background = "yellow"
            timer = True
        else:
            self.label_browser_width.background = "red"
            timer = False
        
        global former_screen_size
        if former_screen_size != self.innerWidth:
            self.xy_panel.width =  self.screen_width             # largeur de l'xy panel se réadapte
            self.label_browser_width.text = self.browser_width
            former_screen_size = self.screen_width 







