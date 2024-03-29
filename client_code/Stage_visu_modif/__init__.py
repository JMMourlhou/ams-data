from ._anvil_designer import Stage_visu_modifTemplate
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from .. import French_zone
from anvil import open_form

global intitul
intitul=""

class Stage_visu_modif(Stage_visu_modifTemplate):
    def __init__(self, provenance="", num_stage=0, bg_task=True, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.provenance = provenance
        self.num_stage=num_stage
        self.bg_task = bg_task
        
        # Any code you write here will run before the form opens.
        if num_stage == 0:
            alert("Numéro de stage non trouvé")
            return
        
        # Drop down codes stages
        self.drop_down_code_stage.items = [(r['code'], r) for r in app_tables.codes_stages.search()]

        # Drop down codes lieux
        self.drop_down_lieux.items = [(r['lieu'], r) for r in app_tables.lieux.search()]
        #lecture du stage
        stage_row=app_tables.stages.get(numero=num_stage)
        #lecture des stagiaires inscrits
        liste_stagiaires = app_tables.stagiaires_inscrits.search(tables.order_by("name", ascending=True),
                                                                            stage=stage_row
                                                                           )
        if len(liste_stagiaires) > 0:                      # des stagiaires sont déjà inscrits ds stage
            self.repeating_panel_1.items = liste_stagiaires
        else:                                              # stage vide, je n'affiche pas les bt et la liste
            self.button_trombi.visible = False
            self.button_trombi_pdf.visible = False
            self.button_fiches_stagiaires.visible = False
        
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
            typ = stage_row['code']
            self.text_box_intitule.text = intit
            self.date_picker_from.date = stage_row['date_debut']
            self.text_box_nb_stagiaires_deb.text = stage_row['nb_stagiaires_deb']
            self.date_picker_to.date = stage_row['date_fin']
            self.text_box_nb_stagiaires_fin.text = stage_row['nb_stagiaires_fin']
            self.text_box_nb_stagiaires_diplom.text = stage_row['nb_stagiaires_diplomes']
            self.text_area_commentaires.text = stage_row['commentaires']
            self.drop_down_lieux.selected_value = stage_row['lieu']
            self.check_box_allow_bg_task.checked = stage_row['allow_bgt_generation']
            
            """ *************************************************************************"""
            """       Création de liste et trombi en back ground task si stagiaires ds stage     """
            """ ***********************************************************************"""            
            if self.check_box_allow_bg_task.checked == False or self.bg_task == False:     # ex: en retour de trombi, pas besoin de re-générer les listes
                students_rows = list(app_tables.stagiaires_inscrits.search(stage=stage_row))
                #alert(len(students_rows))
                if students_rows:    # stagiaires existants
                    with anvil.server.no_loading_indicator:
                        self.task_list = anvil.server.call('run_bg_task_stage_list',self.text_box_num_stage.text, self.text_box_intitule.text)
                        #alert(self.task_list.get_task_name())
                        #alert(self.task_list.get_id())
                    
                    with anvil.server.no_loading_indicator:
                        self.task_trombi = anvil.server.call('run_bg_task_trombi',self.text_box_num_stage.text, self.text_box_intitule.text)
                        #alert(self.task_trombi.get_id())
                        #alert(self.task_trombi.get_task_name())
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
        if self.provenance == "recherche":
            from ..Recherche_stagiaire import Recherche_stagiaire
            open_form('Recherche_stagiaire')
        if self.provenance == "visu_stages":
            from ..Visu_stages import Visu_stages
            open_form('Visu_stages')

    def button_validation_click(self, **event_args):
        """This method is called when the button is clicked"""
        """ Tests avant validation """

        row = self.drop_down_code_stage.selected_value    # Récupération de la ligne stage sélectionnée
        if row == None:
            alert("Entrez le code du stage")
            return
        row2 = self.drop_down_lieux.selected_value         # Récupération du lieu sélectionné
        if row2 == None:
            alert("Entrez le lieu du stage")
            return

        if self.date_picker_to.date == None :           # dates vides ?
            alert("Entrez la date de fin du stage")
            return
        if self.date_picker_from.date == None :
            alert("Entrez la date de début du stage")
            return

        # Test si numero stage code existant pour permettre la modif
        stage=None
        stage = app_tables.stages.search(numero=int(self.text_box_num_stage.text))
        if len(stage) == 0:
            alert("Le numéro de stage n'existe pas !")
            self.button_annuler_click()
        #pas de modif du type et num de stage
        result = anvil.server.call("modif_stage", row['code'],
                                                self.text_box_num_stage.text,  # num du stage  de la ligne  
                                                row2['lieu'],                                              
                                                self.date_picker_from.date,
                                                self.text_box_nb_stagiaires_deb.text,
                                                self.date_picker_to.date,
                                                self.text_box_nb_stagiaires_fin.text,
                                                self.text_box_nb_stagiaires_diplom.text,
                                                self.text_area_commentaires.text,
                                                self.check_box_allow_bg_task.checked
                                                 )
        if result == True :
            alert("Stage enregisté !")
            self.button_qr_code_display.visible = True
            self.button_validation.visible = False
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

    def button_trombi_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_trombi import Visu_trombi
        open_form('Visu_trombi',self.text_box_num_stage.text, self.text_box_intitule.text, False)

    def button_trombi_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        try:  # si les BG tasks de génération des listes trombi pdf / list pdf existent
            if self.task_trombi.is_completed():
                stage_row = app_tables.stages.get(numero=int(self.num_stage))
                pdf = stage_row['trombi_media']
                if pdf:
                    anvil.media.download(pdf)
                    alert("Trombinoscope téléchargé")
                else:
                    alert("Pdf du trombi non trouvé")
        except: #sinon, j'utise les existentes, créées en table stage, (revient de trombi ou stage_row['allow_bgt_generation']=False)
            stage_row = app_tables.stages.get(numero=int(self.num_stage))
            pdf = stage_row['trombi_media']
            if pdf:
                anvil.media.download(pdf)
                alert("Trombinoscope téléchargé")
            else:
                alert("Pdf du trombi non trouvé")
       
    def button_list_pdf_stagiaires_click(self, **event_args):
        """This method is called when the button is clicked"""
        try:  # si les BG tasks de génération des listes trombi pdf / list pdf existent 
            if self.task_list.is_completed():
                stage_row = app_tables.stages.get(numero=int(self.num_stage))
                pdf = stage_row['list_media']
                if pdf:
                    anvil.media.download(pdf)
                    alert("Liste téléchargée")
                else:
                    alert("Liste du trombi non trouvée")
        except:  #sinon, j'utise les existentes, créées en table stage, (revient de trombi ou stage_row['allow_bgt_generation']=False)
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

    

    

    
    
  

    







                                    
