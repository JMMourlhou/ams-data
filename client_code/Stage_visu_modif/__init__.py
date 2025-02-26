from ._anvil_designer import Stage_visu_modifTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from .. import French_zone
#from anvil import open_form

global intitul
intitul=""

class Stage_visu_modif(Stage_visu_modifTemplate):
    def __init__(self, num_stage=0, bg_task=False, **properties):     # bg_task True: je crée les bg task en entrée de stage visu modif
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.num_stage=num_stage
        self.bg_task = bg_task
        
        self.f = get_open_form()   # récupération de la forme mère pour revenir ds la forme appelante
        print("form mère atteingnable (en modif): ", self.f)
      
        # Any code you write here will run before the form opens.
        if num_stage == 0:
            alert("Numéro de stage non trouvé")
            return
        
        # Drop down codes stages
        self.drop_down_code_stage.items = [(r['code'], r) for r in app_tables.codes_stages.search(tables.order_by("code", ascending=True))]

        # Drop down codes lieux
        self.drop_down_lieux.items = [(r['lieu'], r) for r in app_tables.lieux.search()]
        
        #lecture du stage
        stage_row=app_tables.stages.get(numero=int(num_stage))
        self.stage_row = stage_row
        
        #lecture des stagiaires inscrits
        liste_stagiaires = app_tables.stagiaires_inscrits.search(   q.fetch_only("name", "prenom", 
                                                                    user_email=q.fetch_only("email", "tel")),
                                                                    tables.order_by("name", ascending=True),
                                                                    stage=stage_row
                                                                           )
        if len(liste_stagiaires) > 0:                      # des stagiaires sont déjà inscrits ds stage
            self.repeating_panel_1.items = liste_stagiaires
        else:                                              # stage vide, je n'affiche pas les bt et la liste
            self.button_trombi.visible = False
            self.button_trombi_pdf.visible = False
            self.button_fiches_stagiaires.visible = False
            self.button_visu_fiches_stagiaires.visible = False

        # si option stable cochée, true, on lancera les bgt du trombi et fiches
        if stage_row['allow_bgt_generation'] is False:
            self.button_fiches_stagiaires.visible = False
            self.button_trombi_pdf.visible = False
        else:
            self.button_fiches_stagiaires.visible = True
            self.button_trombi_pdf.visible = True
            
        #lecture intitulé stage
        global intitul
        intitul = stage_row['code']['code']
        type_row = app_tables.codes_stages.get(code=intitul)
        if type_row:
            intit = type_row['intitulé']
        else:
            alert("intitulé du stage non trouvé !")
            return
        
        if stage_row:
            self.text_box_num_stage.text = stage_row['numero']
            self.drop_down_code_stage.selected_value = stage_row['code']
            self.text_box_intitule.text = intit
            self.date_picker_from.date = stage_row['date_debut']
            self.text_box_nb_stagiaires_deb.text = stage_row['nb_stagiaires_deb']
            self.date_picker_to.date = stage_row['date_fin']
            self.text_box_nb_stagiaires_fin.text = stage_row['nb_stagiaires_fin']
            self.text_box_nb_stagiaires_diplom.text = stage_row['nb_stagiaires_diplomes']
            self.text_area_commentaires.text = stage_row['commentaires']
            self.drop_down_lieux.selected_value = stage_row['lieu']
            self.check_box_allow_bg_task.checked = stage_row['allow_bgt_generation']
            self.check_box_allow_satisf.checked = stage_row['saisie_satisf_ok']
            self.check_box_allow_suivi.checked = stage_row['saisie_suivi_ok']
            self.check_box_allow_com.ckecked = stage_row['display_com']
            
            """ *************************************************************************"""
            """       Création de liste et trombi en back ground task si stagiaires ds stage     """
            """ ***********************************************************************"""            
            if self.check_box_allow_bg_task.checked is False or self.bg_task is True:     # ex: en retour de trombi, pas besoin de re-générer les listes
                students_rows = list(app_tables.stagiaires_inscrits.search( q.fetch_only(),
                                                                            stage=stage_row))
                #alert(len(students_rows))
                if students_rows:    # stagiaires existants
                    with anvil.server.no_loading_indicator:
                        self.task_list = anvil.server.call('run_bg_task_stage_list',self.text_box_num_stage.text, self.text_box_intitule.text)
                        self.timer_1.interval=0.5
                    
                    with anvil.server.no_loading_indicator:
                        self.task_trombi = anvil.server.call('run_bg_task_trombi',self.text_box_num_stage.text, self.text_box_intitule.text)
                        self.timer_2.interval=0.5
        else:
            alert("Stage non trouvé")
            return

    def date_picker_to_change(self, **event_args):
        """This method is called when the selected date changes"""
        self.button_validation.visible = True   
        date1 = self.date_picker_to.date
        date2 = self.date_picker_from.date
        if date1 < date2:
            alert("La date de fin est inférieure à la date de début !")
            self.date_picker_to.focus()
        
    def date_picker_from_change(self, **event_args):
        """This method is called when the selected date changes"""
        self.button_validation.visible = True   
        date1 = self.date_picker_to.date
        date2 = self.date_picker_from.date
        if date1 < date2:
            alert("La date de fin est inférieure à la date de début !")
            self.date_picker_to.focus()
    
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Je connais la forme appelante: en init : self.f = get_open_form()
        if str(self.f) != str(self):
            open_form(self.f)
        else:
            from ..Visu_stages import Visu_stages
            open_form("Visu_stages")
        
        
    def button_validation_click(self, **event_args):
        """This method is called when the button is clicked"""
        """ Tests avant validation """

        row = self.drop_down_code_stage.selected_value    # Récupération de la ligne stage sélectionnée
        if row is None:
            alert("Entrez le code du stage")
            return
        row2 = self.drop_down_lieux.selected_value         # Récupération du lieu sélectionné
        if row2 is None:
            alert("Entrez le lieu du stage")
            return

        if self.date_picker_to.date is None :           # dates vides ?
            alert("Entrez la date de fin du stage")
            return
        if self.date_picker_from.date is None :
            alert("Entrez la date de début du stage")
            return

        # Test si numero stage code existant pour permettre la modif
        stage=None
        stage = app_tables.stages.search(numero=int(self.text_box_num_stage.text))
        if len(stage) == 0:
            alert("Le numéro de stage n'existe pas !")
            self.button_annuler_click()

        # si chck box F_suivi validé: test si un dict de suivi existe pour ce stage 
        if self.check_box_allow_suivi.checked is True:
            if self.stage_row['suivi_dico1_q_ferm'] is None: # si pas de dict de form de satisf question ferm pour ce stage

                # lecture de table mère 'code_stage' pour verif si un dict template existant
                code_stage_row = app_tables.codes_stages.get(code=self.stage_row['code']['code'])
                if code_stage_row['suivi_stage_q_ferm_template'] is not None:
                    r=alert("voulez-vous copier le formulaire de suivi existant pour ce type de stage pour les stagiaires de ce stage ?", dismissible=False ,buttons=[("oui",True),("non",False)])
                    if r :   # Oui
                        # copie dans table stage pour ce stage
                        anvil.server.call("update_suivi_pour_un_stage",self.stage_row, code_stage_row['suivi_stage_q_ouv_template'], code_stage_row['suivi_stage_q_ferm_template'])
                else:
                    alert("Attention, créez d'abord un formulaire de suivi pour ce type de stage !")
                    self.check_box_allow_suivi.checked = False
        
        # si check box F_satisf validé: test si un dict de satisf existe pour ce stage 
        if self.check_box_allow_satisf.checked is True:
            if self.stage_row['satis_dico1_q_ferm'] is None: # si pas de dict de form de satisf question ferm pour ce stage
                
                # lecture de table mère 'code_stage' pour verif si un dict template existant
                code_stage_row = app_tables.codes_stages.get(code=self.stage_row['code']['code'])
                if code_stage_row['satisf_q_ferm_template'] is not None:
                    r=alert("voulez-vous copier le formulaire de satisfaction existant pour ce type de stage pour les stagiaires de ce stage ?", dismissible=False ,buttons=[("oui",True),("non",False)])
                    if r :   # Oui
                        # copie dans table stage pour ce stage
                        anvil.server.call("update_satisf_pour_un_stage",self.stage_row, code_stage_row['satisf_q_ouv_template'], code_stage_row['satisf_q_ferm_template'])
                else:
                    alert("Attention, créez d'abord un formulaire de satisfaction pour ce type de stage !")
                    self.check_box_allow_satisf.checked = False 

        # si check box F_com validé: test si un dict de com existe pour ce stage 
        if self.check_box_allow_com.checked is True:
            if self.stage_row['com_ferm'] is None: # si pas de dict de form de satisf question ferm pour ce stage
                # lecture de table mère 'code_stage' pour verif si un dict template existant
                code_stage_row = app_tables.codes_stages.get(code=self.stage_row['code']['code'])
                if code_stage_row['com_ferm'] is not {}:
                    r=alert("voulez-vous copier le formulaire de communication existant pour ce type de stage pour les stagiaires de ce stage ?", dismissible=False ,buttons=[("oui",True),("non",False)])
                    if r :   # Oui
                        # copie dans table stage pour ce stage
                        anvil.server.call("update_com_pour_un_stage",self.stage_row, code_stage_row['com_ouv'], code_stage_row['com_ferm'])
                else:
                    alert("Attention, créez d'abord un formulaire de communication pour ce type de stage !")
                    self.check_box_allow_com.checked = False 
        # ! modif du  num de stage possible !!!
        result = anvil.server.call("modif_stage", row,
                                                self.text_box_num_stage.text,  # num du stage  de la ligne  
                                                row2['lieu'],                                              
                                                self.date_picker_from.date,
                                                self.text_box_nb_stagiaires_deb.text,
                                                self.date_picker_to.date,
                                                self.text_box_nb_stagiaires_fin.text,
                                                self.text_box_nb_stagiaires_diplom.text,
                                                self.text_area_commentaires.text,
                                                self.check_box_allow_bg_task.checked,
                                                self.check_box_allow_satisf.checked,
                                                self.check_box_allow_suivi.checked,
                                                self.check_box_allow_com.checked,
                                                 )
        if result is True :
            alert("Stage enregisté !")
        else :
            alert("Stage non enregisté !")
        self.button_annuler_click()

   
    def drop_down_lieux_change(self, **event_args):
        """This method is called when an item is selected"""
        self.button_validation.visible = True
        
    def text_box_nb_stagiaires_deb_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.button_validation.visible = True

    def text_box_nb_stagiaires_fin_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.button_validation.visible = True

    def text_box_nb_stagiaires_diplom_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.button_validation.visible = True

    def text_area_commentaires_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.button_validation.visible = True
        
    def check_box_allow_bg_task_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_validation.visible = True   

    def check_box_allow_satisf_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_validation.visible = True

    def check_box_allow_suivi_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_validation.visible = True

    def check_box_allow_com_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_validation.visible = True

    def button_trombi_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_trombi import Visu_trombi
        open_form('Visu_trombi',self.text_box_num_stage.text, self.text_box_intitule.text, False)

    def button_trombi_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        stage_row = app_tables.stages.get(numero=int(self.num_stage))
        pdf = stage_row["trombi_media"]
        if pdf:
            anvil.media.download(pdf)
            alert("Trombinoscope téléchargé")
        else:
            alert("Pdf du trombi non trouvé")
       
    def button_list_pdf_stagiaires_click(self, **event_args):
        """This method is called when the button is clicked"""
        stage_row = app_tables.stages.get(numero=int(self.num_stage))
        pdf = stage_row['list_media']
        if pdf:
            anvil.media.download(pdf)
            alert("Liste téléchargée")
        else:
            alert("Liste du trombi non trouvée")

    def button_qr_code_display_click(self, **event_args):
        """This method is called when the button is clicked"""
        # False indique que ce n'est pas une invitation à log in normal
        # mais une invitation à s'inscrire au stage
        open_form('QrCode_display', False, self.text_box_num_stage.text)

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        self.column_panel_header.scroll_into_view()

    def button_visu_fiches_stagiaires_click(self, **event_args):
        """This method is called when the button is clicked"""
        global intitul
        open_form('Visu_liste_1_stage',str(self.num_stage), intitul, False)

    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        if self.task_list.is_completed():
            self.button_fiches_stagiaires.visible = True
            self.timer_1.interval=0
            anvil.server.call('task_killer',self.task_list)

            
    def timer_2_tick(self, **event_args):
        if self.task_trombi.is_completed():
            self.button_trombi_pdf.visible = True
            self.timer_2.interval=0
            anvil.server.call('task_killer',self.task_trombi)

    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        self.button_validation.visible = True   
        row = self.drop_down_code_stage.selected_value
        if row is None :
            alert("Vous devez sélectionner un stage !")
            self.drop_down_code_stage.focus()
            return
        self.text_box_intitule.text=row['intitulé']

    






        

    

    

    
    
  

    







                                    
