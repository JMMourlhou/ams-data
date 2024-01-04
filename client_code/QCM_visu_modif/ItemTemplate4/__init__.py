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

class ItemTemplate4(ItemTemplate4Template):
    def __init__(self, **properties):               # "creation" = mode création/MAJ pas de test stagiaire
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        # lecture  user: si user admin A: mode création 
        user=anvil.users.get_user()
        print("admin: ", user[''])
        if user:
            self.admin = user['admin']
            #if admin[0:1]=="A":
            if self.admin == True:
                self.mode= "creation"
            else:
                self.mode = "test"

        self.flow_panel_num.tag.nom = "fp_num"
        self.cp_father.tag.nom = "cp_father"
        self.cp_img.tag.nom = "cp_img"
        self.fp_modif.tag.nom = "fp_modif"
        self.fp_vf_barem.tag.nom = "fp_vrai/faux_bareme"
        self.check_box_reponse.tag.nom = "reponse"
        self.spacer_2.tag.nom = "spacer"
        self.label_1.tag.nom = "label"
        self.drop_down_bareme.tag.nom = "bareme"
        
        self.qcm_nb = self.item["qcm_nb"]    # récup qcm nb
        #recherche nb de questions (sauvées ds temp table)
        table_temp = app_tables.temp.search()[0]
        self.label_4.text = table_temp['nb_questions_qcm']
        
        self.label_2.tag.nom = "cpt"
        self.label_2.text = self.item['num']
        self.label_2.tag.numero = self.item['num']
        self.label_2.tag.nom = "num"
        
        self.text_box_question.text = self.item['question']
        self.text_box_question.tag.nom = "question"
        self.text_box_question.tag.numero = self.item['num']
        
        self.text_box_correction.text = self.item['correction']
        self.text_box_correction.tag.nom = "correction"
        self.text_box_correction.tag.numero = self.item['num']
        
        self.check_box_reponse.checked = self.item['reponse']
        self.check_box_reponse.tag.nom = "reponse"
        self.check_box_reponse.tag.numero = self.item['num']
        
        self.drop_down_bareme.items=["1","5"]
        self.drop_down_bareme.selected_value = self.item['bareme']                 
        self.drop_down_bareme.tag.nom = "bareme"
        self.drop_down_bareme.tag.numero = self.item['num']
        
        self.button_modif.tag.numero = self.item['num']          #Je sauve le NUMERO de question ds le tag      
        self.button_modif.tag.nom = "button"
     
        self.image_1.source = self.item['photo']
        self.image_1.tag.nom = "photo"
        self.image_1.tag.numero = self.item['num']

        print(self.mode)
        if self.mode != "creation":
            self.text_box_question.enabled = False
            self.file_loader_1.visible = False
            self.text_box_correction.visible = False
            self.drop_down_bareme.enabled = False
        
    def text_box_question_change(self, **event_args):   # Question a changé
        """This method is called when the text in this text box is edited"""
        # je récupère le contenu du cpnt
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_1.source = thumb_pic
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
       
    def drop_down_bareme_change(self, **event_args):     # Bareme a changé
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
        global ancien_num_ligne
        ancien_num_ligne = self.drop_down_bareme.tag.numero
    
    def check_box_reponse_change(self, **event_args):   # Reponse a changé: 
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
        global ancien_num_ligne
        ancien_num_ligne = self.check_box_reponse.tag.numero
  
    def button_modif_click(self, **event_args):   #ce n'est que l'orsque le user a clicker sur modif que je prend le contenu
        """This method is called when the button is clicked"""
  
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
            
            if cpnt.tag.nom == "question":
                print(cpnt, cpnt.tag.nom)
                num = int(cpnt.tag.numero)           # j'ai le num de la question
                question = cpnt.text                 #         question
                
                # mettre la 1ere lettre en maj mais laisser le reste comme tappé
                #je boucle à partir de la deuxieme lettre et cumul le text             
                txt = question[0].capitalize()    # txt commence par la position 1 de la question, mise en majuscule
                txt2 = question[1:len(question)]   #Slice je prends toute la question à partir de la position 2
                question = txt + txt2 
                
            if cpnt.tag.nom == "correction":
                print(cpnt, cpnt.tag.nom)
                correction = cpnt.text               #    j'ai la correction
                
            print("avt test2",cpnt, cpnt.tag.nom)
            if cpnt.tag.nom == "fp_vrai/faux_bareme":       # fp_vf_barem contient reponse et bareme   
                print("test2", cpnt, cpnt.tag.nom)
                for cpnt2 in cpnt.get_components():   #( cp_img contient image_1)
                    if cpnt2.tag.nom =="reponse":
                        print(cpnt2, cpnt2.tag.nom)
                        reponse = cpnt2.checked            # j'ai la réponse ( v/F )
                    if cpnt2.tag.nom =="bareme":
                        print(cpnt2, cpnt2.tag.nom)
                        bareme = cpnt2.selected_value
           
        #recup qcm_nb ds fichier temp

        qcm_descro_row = self.qcm_nb
        print(qcm_descro_row)
        result = anvil.server.call('modif_qcm', qcm_descro_row, num, question, reponse, bareme, photo, correction)
        if not result:
            alert("erreur de création d'une question QCM")
            return
            
        # j'initialise la forme principale
        from anvil import open_form       
        open_form("QCM_visu_modif_Main",qcm_descro_row)

    def text_box_question_lost_focus(self, **event_args):
        """This method is called when the TextBox loses focus"""
        global ancien_num_ligne
        ancien_num_ligne = self.text_box_question.tag.numero
        
    def text_box_question_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        num = self.text_box_question.tag.numero
        # Je recherche le bouton de l'ancienne ligne pour le désactiver
        #Je remonte du component sur 3 niveaux (jusqu'au repeat panel de la form 'QCM_visu_modif') 
        global ancien_num_ligne
        if ancien_num_ligne != 0 and num != ancien_num_ligne:
            n1 = self.button_modif.parent    # conteneur d'1 ligne 
            n2 = n1.parent            # conteneur cpanel : contient cp_img, tb question, tb correction
            repeat_item_panel = n2.parent    # conteneur objet ligne (item)
            repeat_panel = repeat_item_panel.parent  # conteneur des lignes (repeat panel) ds QCM_visu_modi
            print("**** repeating panel *****", type(repeat_panel))
           
            for item_lignes in repeat_panel.get_components():
                for ligne in item_lignes.get_components():
                    for cpnt in ligne.get_components():
                        if cpnt.tag.nom == "button" and cpnt.tag.numero == ancien_num_ligne:
                            #c'est le bt de l'ancienne ligne
                            self.button_modif.enabled = False
                            self.button_modif.background = "theme:Tertiary"
                            self.button_modif.foregroundground = "theme:Error"
                            ancien_num_ligne = 0

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        global cpt    # cpt = nb de questions
        cpt += 1
        print(cpt)

    
                                

            




        

   
        


    

        

    

        




 


        
        