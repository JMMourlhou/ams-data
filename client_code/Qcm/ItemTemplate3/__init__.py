from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global etat_vrai  # etat du bouton vrai
etat_vrai = None
global etat_faux  # etat du bouton faux
etat_faux = None

class ItemTemplate3(ItemTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        question = str(self.item["num"])+"-   "+self.item['question']
        nb = self.item["num"]      
        # Création du column panel de la question et check boxes
        cp = ColumnPanel(role="outlined-card",
                         background="theme:Primary",
                         wrap_on="mobile",
                         spacing_above=None,
                         spacing_below=None, 
                        )
        self.add_component(cp)

        # Création de la question ds le colomn panel
        q = RichText(content=question,
                     align="center",
                     font_size=14,
                     foreground="theme:On Primary",
                     role="markdown",
                     spacing_above=None,
                     spacing_below=None,                    
                    )
        cp.add_component(q)

        # Création du flow panel ds le column panel
        fp = FlowPanel()
        cp.add_component(fp)
        
        # Création de l'espace avant le Check box Vrai
        space1=Spacer(height=5, width=50, spacing_above=None, spacing_below=None)
        fp.add_component(space1)
        
        # Création Check box Vrai ds le flow panel pour créer le tag et reconnaitre quelle question est chekée 
        cb_true = CheckBox(text="Vrai",
                                 checked=None,
                                 allow_indeterminate=True,
                                 spacing_above=None,
                                 spacing_below=None,
                                 tag=self.item['num'],
                                 enabled=True
                                )
        fp.add_component(cb_true)
        cb_true.set_event_handler('change',self.check_box_true_change)
        
        # Création de l'espace après le Check box Vrai
        space2=Spacer(height=5, width=50, spacing_above=None, spacing_below=None)
        fp.add_component(space2)
        
        # Création Check box Faux ds le flow panel pour créer le tag et reconnaitre quelle question est chekée 
        cb_false = CheckBox(text="Faux",
                                 checked=None,
                                 allow_indeterminate=True,
                                 spacing_above=None,
                                 spacing_below=None,
                                 tag=self.item['num'],
                                 enabled=True
                                )
        fp.add_component(cb_false)
        cb_false.set_event_handler('change',self.check_box_false_change)
        

    
    def text_area_1_show(self, **event_args):
        """This method is called when the text area is shown on the screen"""
        global cpt  # Cpt le nb de form imprimée
        cpt += 1

    def check_box_true_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        """ contenu du dictionaire event_args 
        {'button': 1, 'keys': {'meta': False, 'shift': False, 'ctrl': False, 'alt': False}, 'sender': <anvil.Image object>, 'event_name': 'mouse_down'}"""
        
        question_nb = event_args["sender"].tag   # j'extrais le tag du sender (le num de la question)
        print("question_nb: ",question_nb)
        global etat_vrai
        etat_vrai = True
        #global etat_faux
        #etat_faux = False
        print(etat_vrai, etat_faux)
        if etat_faux == etat_vrai:
            alert("Réponse ne peut pas être vrai et fausse")
            #fp[question_nb].cb_true.checked=None
            "fp[question_nb].cb_false.checked=None
            
            lp.tag.answertextbox = tb
        # maj dico connaissant la ligne, l'état

    def check_box_false_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        question_nb = event_args["sender"].tag   # j'extrais le tag du sender (le num de la question)
        print("question_nb: ",question_nb)
        #global etat_vrai
        #etat_vrai = False
        global etat_faux
        etat_faux = True
        print(etat_vrai, etat_faux)
        if etat_faux == etat_vrai:
            alert("Réponse ne peut pas être vrai et fausse")
        # maj dico connaissant la ligne, l'état
        

