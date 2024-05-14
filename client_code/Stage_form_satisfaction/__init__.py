from ._anvil_designer import Stage_form_satisfactionTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global user_stagiaire
user_stagiaire = anvil.users.get_user()
global stage_row
stage_row = None


class Stage_form_satisfaction(Stage_form_satisfactionTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

        
        #if isinstance(stage_row['satis_dico1_q_ferm'], dict): 
        #n'afficher que les stages ayant un dico 

        
        global user_stagiaire
        if user_stagiaire:
            #self.label_0.text = "Documents à fournir pour " + user_pr['prenom'] + " " + user_pr['nom']
            # Drop down stages inscrits du user
            liste0 = app_tables.stagiaires_inscrits.search(q.fetch_only("user_email","stage"),           # <----------------------  A Modifier? 
                                                            user_email=user_stagiaire
                                                          )
            print("nb; ", len(liste0))
            liste_drop_d = []
            for row in liste0:
                #lecture fichier père stage
                stage=app_tables.stages.get(numero=row['stage']['numero'])
                if isinstance(stage['satis_dico1_q_ferm'], dict): # si dict ds table 
                    #lecture fichier père type de stage
                    type=app_tables.codes_stages.get(q.fetch_only("code"),
                                                        code=stage['code']['code']
                                                    )
                    if type['code'][0]!="F":    # Si formateur, je n'affiche pas la dat
                        liste_drop_d.append((type['code']+"  du "+str(stage['date_debut']), stage))
                    else:
                        liste_drop_d.append((type['code'], stage))
                    
            #print(liste_drop_d)
            self.drop_down_code_stage.items = liste_drop_d

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        global stage_row
        stage_row = self.drop_down_code_stage.selected_value
        if stage_row is None:
            alert("Vous devez sélectionner un pré-requis !")
            self.drop_down_code_stage.focus()
            return
        #self.column_panel_2.visible = True
        # extraction des 2 dictionnaires du stage
        dico_q_ferm = {}
        dico_q_ouv = {}
        dico_q_ferm = stage_row['satis_dico1_q_ferm']
        nb_questions_ferm = int(dico_q_ferm['NBQ'])   # nb de questions fermées ds le dico

        if nb_questions_ferm > 0:   # Check du nb de questions fermées à afficher et affectation des questions
            self.column_panel_1.visible = True
            self.label_1.text = dico_q_ferm['1']
        if nb_questions_ferm > 1:
            self.column_panel_2.visible = True
            self.label_2.text = dico_q_ferm['2']
        if nb_questions_ferm > 2:
            self.column_panel_3.visible = True
            self.label_3.text = dico_q_ferm['3']
        if nb_questions_ferm > 3:
            self.column_panel_4.visible = True
            self.label_4.text = dico_q_ferm['4']
        if nb_questions_ferm > 4:
            self.column_panel_5.visible = True
            self.label_5.text = dico_q_ferm['5']
        if nb_questions_ferm > 5:
            self.column_panel_6.visible = True
            self.label_6.text = dico_q_ferm['6']
        if nb_questions_ferm > 6:
            self.column_panel_7.visible = True
            self.label_7.text = dico_q_ferm['7']
        if nb_questions_ferm > 7:
            self.column_panel_8.visible = True
            self.label_8.text = dico_q_ferm['8']
        if nb_questions_ferm > 8:
            self.column_panel_9.visible = True
            self.label_9.text = dico_q_ferm['9']
        if nb_questions_ferm > 9:
            self.column_panel_10.visible = True
            self.label_10.text = dico_q_ferm['10']

        dico_q_ouv = stage_row['satis_dico2_q_ouv']  # check du nb de questions ouvertes à afficher et affectation des questions
        nb_questions_ouvertes = int(dico_q_ouv['NBQ'])
        if nb_questions_ouvertes > 0:
            self.column_panel_a1.visible = True
            self.label_a1.text = dico_q_ouv['1']
        if nb_questions_ouvertes > 1:
            self.column_panel_a2.visible = True
            self.label_a2.text = dico_q_ouv['2']
        if nb_questions_ouvertes > 2:
            self.column_panel_a3.visible = True   
            self.label_a3.text = dico_q_ouv['3']
        if nb_questions_ouvertes > 3:
            self.column_panel_a4.visible = True   
            self.label_a4.text = dico_q_ouv['4']
        if nb_questions_ouvertes > 4:
            self.column_panel_a5.visible = True      
            self.label_a5.text = dico_q_ouv['5']
        if nb_questions_ouvertes > 5:
            self.column_panel_a6.visible = True   
            self.label_a6.text = dico_q_ouv['6']
        if nb_questions_ouvertes > 6:
            self.column_panel_a7.visible = True  
            self.label_a7.text = dico_q_ouv['7']
        if nb_questions_ouvertes > 7:
            self.column_panel_a8.visible = True 
            self.label_a8.text = dico_q_ouv['8']
        if nb_questions_ouvertes > 8:
            self.column_panel_a9.visible = True     
            self.label_a9.text = dico_q_ouv['9']
        if nb_questions_ouvertes > 9:
            self.column_panel_a10.visible = True     
            self.label_a10.text = dico_q_ouv['10']

    def check_box_1_1_change(self, **event_args):             # 1 seule réponse doit être checker
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_1_1.checked is True:
            self.check_box_1_2.checked = False
            self.check_box_1_3.checked = False
            self.check_box_1_4.checked = False
            self.check_box_1_5.checked = False
            self.check_box_1_6.checked = False

    def check_box_1_2_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_1_2.checked is True:
            self.check_box_1_1.checked = False
            self.check_box_1_3.checked = False
            self.check_box_1_4.checked = False
            self.check_box_1_5.checked = False
            self.check_box_1_6.checked = False

    def check_box_1_3_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_1_3.checked is True:
            self.check_box_1_1.checked = False
            self.check_box_1_2.checked = False
            self.check_box_1_4.checked = False
            self.check_box_1_5.checked = False
            self.check_box_1_6.checked = False

    def check_box_1_4_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_1_4.checked is True:
            self.check_box_1_1.checked = False
            self.check_box_1_3.checked = False
            self.check_box_1_2.checked = False
            self.check_box_1_5.checked = False
            self.check_box_1_6.checked = False

    def check_box_1_5_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_1_5.checked is True:
            self.check_box_1_1.checked = False
            self.check_box_1_2.checked = False
            self.check_box_1_4.checked = False
            self.check_box_1_3.checked = False
            self.check_box_1_6.checked = False

    def check_box_1_6_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_1_6.checked is True:
            self.check_box_1_1.checked = False
            self.check_box_1_2.checked = False
            self.check_box_1_4.checked = False
            self.check_box_1_3.checked = False
            self.check_box_1_5.checked = False
    #================================================================================= 2eme ligne
    def check_box_2_1_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_2_1.checked is True:
            self.check_box_2_2.checked = False
            self.check_box_2_3.checked = False
            self.check_box_2_4.checked = False
            self.check_box_2_5.checked = False
            self.check_box_2_6.checked = False

    def check_box_2_2_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_2_2.checked is True:
            self.check_box_2_1.checked = False
            self.check_box_2_3.checked = False
            self.check_box_2_4.checked = False
            self.check_box_2_5.checked = False
            self.check_box_2_6.checked = False

    def check_box_2_3_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_2_3.checked is True:
            self.check_box_2_1.checked = False
            self.check_box_2_2.checked = False
            self.check_box_2_4.checked = False
            self.check_box_2_5.checked = False
            self.check_box_2_6.checked = False

    def check_box_2_4_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_2_4.checked is True:
            self.check_box_2_1.checked = False
            self.check_box_2_3.checked = False
            self.check_box_2_2.checked = False
            self.check_box_2_5.checked = False
            self.check_box_2_6.checked = False

    def check_box_2_5_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_2_5.checked is True:
            self.check_box_2_1.checked = False
            self.check_box_2_2.checked = False
            self.check_box_2_4.checked = False
            self.check_box_2_3.checked = False
            self.check_box_2_6.checked = False

    def check_box_2_6_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_2_6.checked is True:
            self.check_box_2_1.checked = False
            self.check_box_2_2.checked = False
            self.check_box_2_4.checked = False
            self.check_box_2_3.checked = False
            self.check_box_2_5.checked = False

    #================================================================================= 3eme ligne
    def check_box_3_1_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_3_1.checked is True:
            self.check_box_3_2.checked = False
            self.check_box_3_3.checked = False
            self.check_box_3_4.checked = False
            self.check_box_3_5.checked = False
            self.check_box_3_6.checked = False

    def check_box_3_2_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_3_2.checked is True:
            self.check_box_3_1.checked = False
            self.check_box_3_3.checked = False
            self.check_box_3_4.checked = False
            self.check_box_3_5.checked = False
            self.check_box_3_6.checked = False

    def check_box_3_3_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_3_3.checked is True:
            self.check_box_3_1.checked = False
            self.check_box_3_2.checked = False
            self.check_box_3_4.checked = False
            self.check_box_3_5.checked = False
            self.check_box_3_6.checked = False

    def check_box_3_4_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_3_4.checked is True:
            self.check_box_3_1.checked = False
            self.check_box_3_3.checked = False
            self.check_box_3_2.checked = False
            self.check_box_3_5.checked = False
            self.check_box_3_6.checked = False

    def check_box_3_5_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_3_5.checked is True:
            self.check_box_3_1.checked = False
            self.check_box_3_2.checked = False
            self.check_box_3_4.checked = False
            self.check_box_3_3.checked = False
            self.check_box_3_6.checked = False

    def check_box_3_6_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_3_6.checked is True:
            self.check_box_3_1.checked = False
            self.check_box_3_2.checked = False
            self.check_box_3_4.checked = False
            self.check_box_3_3.checked = False
            self.check_box_3_5.checked = False

    def button_valider_click(self, **event_args):
        """This method is called when the button is clicked"""
        # check si une reponse par ligne
        nb = 0
        if (self.check_box_1_1.checked is True) or \
            (self.check_box_1_2.checked is True) or \
            (self.check_box_1_3.checked is True) or \
            (self.check_box_1_4.checked is True) or \
            (self.check_box_1_5.checked is True) or \
            (self.check_box_1_6.checked is True):
            nb += 1
        if (self.check_box_2_1.checked is True) or \
            (self.check_box_2_2.checked is True) or \
            (self.check_box_2_3.checked is True) or \
            (self.check_box_2_4.checked is True) or \
            (self.check_box_2_5.checked is True) or \
            (self.check_box_2_6.checked is True):
            nb += 1
        print(nb)
            

        
       
        
        
    