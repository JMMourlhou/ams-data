from ._anvil_designer import Qcm_visuTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras.PageBreak import PageBreak
global etat_faux
etat_faux = None
global etat_vrai
etat_vrai = None

class Qcm_visu(Qcm_visuTemplate):
    def __init__(self,pdf_mode=False, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.label_titre.text = "QCM PSE1"
        #lecture du fichier QCM    
        rows = list(app_tables.qcm.search())
            #tables.order_by("name", ascending=True),
            #stage=stage_row
        #))
        nb_questions = len(rows)                    
        #print("nb-questions", nb_questions)
        xx = 1   # position (x=1, y=1)
        yy = 1
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
                            spacing_above=None,
                            spacing_below=None,
                            width="default",
                            )
            self.cp.tag.nom = "column"
            #self.xy_panel.add_component(self.cp,x=xx, y=yy, width = 715)
            self.xy_panel.add_component(self.cp, x=xx, y=yy, width="default")
            
            # Création de la question ds le column panel
            self.q = RichText(content=question,
                        align="center",
                        font_size=14,
                        foreground="theme:On Primary",
                        role="markdown",
                        spacing_above=None,
                        spacing_below=None,
                        )
            self.q.tag.nom = "question"
            self.cp.add_component(self.q, x=xx+5, y=yy, width="default")

            # Création du flow panel ds le column panel
            self.fp = FlowPanel(align="left")
            self.fp.tag.nom = "flow_panel"
            self.cp.add_component(self.fp)
        
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
        
            # Création de l'espace après le Check box Vrai
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
            self.fp.add_component(self.cb_false)
            self.cb_false.set_event_handler('change',self.check_box_false_change)
            
            #fin de boucle, j'incrémente le yy
            
            yy += 145
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
        
        reponses = []   #liste de toutes les réponses du stagiaire {"num":   , "reponse":   }
        # 1 Boucle sur les flow panels  ET cré le dictionaire
        for col_p in self.xy_panel.get_components():  #ds column panel
            reponse = []    
            print(col_p.tag.nom)

            for fl_p in col_p.get_components():   #ds flow panel
                print(fl_p.tag.nom)

                for cpnt in fl_p.get_components():   # ds chaque cmpnt du flow panel
                    print(cpnt.tag.nom)
                    if cpnt.tag.nom == "cb_true":
                        numero_question = cpnt.tag.num_question
                        global etat_vrai
                        etat_vrai = cpnt.checked     #je sauve l'état du combo vrai
                       
                        number=[]
                        number=["num:",numero_question]                      
                        reponses.append(number)                  # je mets à jour la liste  
                            
                    if cpnt.tag.nom == "cb_false":     #si je suis sur le cobo Faux...
                        global etat_faux
                        etat_faux = cpnt.checked   #je sauve l'état du combo faux                       
                        
                        if etat_faux==None and etat_vrai==None:
                            alert(f"La question {numero_question} n'a pas été répondue")
                            return
                            
                        #liste de la réponse {"num":   , "reponse":   }
                        rep=[]
                        if etat_vrai == False:       # le stagiaire a répondu False
                            rep=["reponse:",False]      
                        else:
                            rep=["reponse:",True]    # le stagiaire a répondu True
                        reponses.append(rep)      # je mets à jour la liste    
                        
                        alert(reponses)
                        reponse=[]
        #sortie de boucle ds mes questions    
        
        
        print("num rep2:",reponses[0+2][1])  
        print("réponse 2:",reponses[0+3][1])
        alert("sauvegarde du dico")
