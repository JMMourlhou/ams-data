from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q

from .. import French_zone
from ..Saisie_info_de_base import Saisie_info_de_base
from ..Stage_creation import Stage_creation
from ..Visu_stages.RowTemplate3 import RowTemplate3
from anvil import open_form
import sign_in_for_AMS_Data

class Main(MainTemplate):
    def __init__(self, nb=1, stage_nb=0, **properties):  # msg pour afficher une alerte si mail erroné en pwreset par ex
        # Set Form properties and Data Bindings.
        
        
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        """
        self.bt_se_deconnecter.visible = False
        self.bt_user_mail.enabled = False
        self.column_panel_admin.visible = False
        """
        self.nb = nb
        """ Incrémentation de nb """
        self.nb = self.nb + 1
        if self.nb >= 99:  # retour de création de fiche renseignement, j'efface l'url pour arrêter la boucle
            h = {}

        """ cas 2: soit ouverture de l'app """
        """        ou retour par URL suite à PW reset ou confirm mail"""
        if self.nb == 2:
            self.column_panel_others.visible = False
            """ get_url_hash() gets the decoded hash (the part after the ‘#’ character) of the URL used to open this app.

                If the first character of the hash is a question mark (e.g., https://myapp.anvil.app/#?a=foo&b=bar),
                it will be interpreted as query-string-type parameters and returned as a dictionary
                (e.g., {'a': 'foo', 'b': 'bar'} ).

                get_url_hash() is available in Form code only.

                I don’t use extra arguments on forms loaded by the routing module.
                Using extra arguments kind of defeats the purpose of using the routing module.

                I pass all the arguments on the URL, then I use self.url_dict['items'].
                
                """

            h = {}
            h = anvil.get_url_hash()
            self.h = h
            # alert(f"h ds init d'AMS_Data: {h}")

            if len(h) != 0:  # a URL has openned this app
                # handling buttons display before going to module externe 'sign_in_for_AMS_Data'
                self.display_bt_mail()
                self.display_admin_or_other_buttons()
                
                # lien actif < à 3 mois ?
                # url_time_str=""
                url_time = h["t"]
                url_time_over = French_zone.time_over(url_time)
                if url_time_over:
                    alert("Ce lien n'est plus actif !")
                else:
                    # stage number in URL's Hash ? (le user vient-il de flacher le Qr code?)
                    # si oui je suis en sign in après flash du qr code par le stagiaire
                    if "stage" in h:
                        self.qr_code()
                        return
                    if h["a"] == "pwreset":
                        self.pwreset()
                        return
                    if h["a"] == "confirm":
                        self.confirm()
                        return
        # handling buttons display
        self.display_bt_mail()
        self.display_admin_or_other_buttons()
        
        # renseignements du user 
        user = anvil.users.get_user(q.fetch_only("prenom"))
        #self.user = anvil.users.get_user(q.fetch_only("prenom"))
        if not user:
            self.content_panel.clear()
        else:
            if user["prenom"] is None or user["prenom"] == "":
                self.column_panel_header.visible = False
                self.content_panel.add_component(Saisie_info_de_base(True), full_width_row=True)

    def pwreset(self, **event_args):
        # handling buttons display
        self.bt_user_mail.text = "Réinitialisation du mot de passe !"
        self.display_admin_or_other_buttons()
        self.bt_se_connecter.visible = False
        self.bt_sign_in.visible = False
        from sign_in_for_AMS_Data.url_from_mail_PW_reset import url_from_mail_PW_reset

        self.content_panel.clear()
        self.content_panel.add_component(
            url_from_mail_PW_reset(self.h["email"], self.h["api"]), full_width_row=True
        )
        return

    def confirm(self, **event_args):
        from sign_in_for_AMS_Data.url_from_mail_calls import url_from_mail_calls

        self.content_panel.clear()
        self.content_panel.add_component(
            url_from_mail_calls(self.h, num_stage=0), full_width_row=True
        )
        return

    def qr_code(self, **event_args):
        num_stage = self.h["stage"]            
        # alert(f"num stage test {num_stage}")
        if len(num_stage) != 0:
            self.bt_sign_in_click(self.h, num_stage)
            return

    """ ***********************************************************************************************"""
    """ ****************************** Gestions  BOUTONS et leurs clicks ******************************"""
    """ ***********************************************************************************************"""

    def display_bt_mail(self, **event_args):
        user = anvil.users.get_user(q.fetch_only("nom"))
        if user:
            self.bt_user_mail.text = user["email"]
            self.bt_se_connecter.visible = False
            self.bt_se_deconnecter.visible = True
        else:
            # Pas de USER
            self.bt_user_mail.text = "Non connecté"
            self.bt_user_mail.enabled = False
            self.bt_se_connecter.visible = True
            self.bt_sign_in.visible = True

            self.bt_se_deconnecter.visible = False

            self.column_panel_admin.visible = False
            self.column_panel_others.visible = False

              
    def bt_gestion_stages_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("Visu_stages")

    def bt_sign_in_click(self, h={}, num_stage=0, **event_args):  # h qd vient de sign in par qr code
        """This method is called when the button is clicked"""
        from sign_in_for_AMS_Data.SignupDialog_V2 import SignupDialog_V2
        self.bt_se_connecter.visible = False
        self.column_panel_bt_mail.visible = False
        """
        self.bt_sign_in.visible = False
        self.bt_gestion_stages.visible = False
        self.column_panel_admin.visible = False
        self.button_qcm.visible = False
        self.button_pre_requis.visible = False
        self.button_form_suivi_stage.visible = False
        self.button_form_satisf.visible = False
        """
        self.content_panel.clear()
        self.content_panel.add_component(
            SignupDialog_V2(h, num_stage), full_width_row=True
        )

    def bt_se_deconnecter_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.content_panel.clear()
        anvil.users.logout()  # logging out the user
        self.display_bt_mail()
        self.display_admin_or_other_buttons()

    def button_se_connecter_click(self, **event_args):
        """This method is called when the button is clicked"""
        """Will call the EXTERNAL MODULE DEPENDACY when the link is clicked"""
        self.bt_se_connecter.visible = False
        self.bt_sign_in.visible = False
        # import sign_in_for_AMS_Data
        from sign_in_for_AMS_Data.LoginDialog_V2 import LoginDialog_V2
        self.content_panel.clear()
        self.content_panel.add_component(LoginDialog_V2(), full_width_row=False)

    def button_qr_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("QrCode_display", True)

    def bt_user_mail_click(self, prem_util=False, **event_args):  # True=1ere utilisation
        """This method is called when the button is clicked"""
        self.content_panel.clear()
        self.bt_se_deconnecter.visible = False
        self.bt_sign_in.visible = False
        # Saisie_info_de_base(False) car pas la 1ere saisie de la fiche de renseignements
        user = anvil.users.get_user(q.fetch_only("email"))
        if not user:
            self.content_panel.clear()
        else:
            open_form("Saisie_info_apres_visu", user["email"])


    def button_qcm_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..QCM_visu_modif_ST_Main import QCM_visu_modif_ST_Main
        open_form("QCM_visu_modif_ST_Main")

    def button_create_recherche_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Recherche_stagiaire import Recherche_stagiaire
        open_form("Recherche_stagiaire")

    def button_pre_requis_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_R_pour_stagiaire import Pre_R_pour_stagiaire
        open_form("Pre_R_pour_stagiaire")

    def button_loop_click(self, **event_args):
        """This method is called when the button is clicked"""
        from .. import z_loop_on_tables
        result=z_loop_on_tables.loop_old_mails()
        alert(result)
        

    def Close_click(self, **event_args):
        """This method is called when the button is clicked"""
        import anvil.js
        from anvil.js.window import localStorage
        from anvil.js import window
        import anvil.users

        # Déconnecter l'utilisateur
        anvil.users.logout()
        # Afficher un message
        # alert("Vous êtes déconnecté.")
        window.close()

    # Extraction de fichier texte pour les qcm
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..QrCode_Generator import QrCode_Generator
        open_form("QrCode_Generator")

    def button_form_satisf_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Stage_form_satisfaction import Stage_form_satisfaction
        open_form("Stage_form_satisfaction")

    def button_satisf_result_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Stage_satisf_statistics import Stage_satisf_statistics
        open_form("Stage_satisf_statistics")

    def button_sign_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Signature import Signature
        open_form("Signature")


    def button_xls_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..XLS_reader import XLS_reader
        open_form("XLS_reader")

    def button_mail_histo_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Mail_to_old_stagiaires import Mail_to_old_stagiaires
        open_form("Mail_to_old_stagiaires")

    def button_rsz_img_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_R_Moulinette import Pre_R_Moulinette
        open_form("Pre_R_Moulinette")

    def button_size_pr_click(self, **event_args):
        """This method is called when the button is clicked"""
        result = anvil.server.call('size_jpg')
        if result:
            alert("fin")
        else:
            alert("pas de fin normale")


    def button_suivi_result_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Stage_suivi_results import Stage_suivi_results
        open_form("Stage_suivi_results")

    def button_form_suivi_stage_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Stage_form_suivi import Stage_form_suivi
        open_form("Stage_form_suivi")

    def display_admin_or_other_buttons(self, **event_args):
        user = anvil.users.get_user(q.fetch_only("nom"))
       
        if user:
            self.bt_sign_in.visible = False
            self.bt_user_mail.enabled = True
            self.button_qcm.visible = True
            self.button_pre_requis.visible = True
            self.label_role.text = user['role']   # affichage du role

            if user["role"] == "S":
                self.column_panel_others.visible = True
                
            if user["role"] == "A" :                              # 'A'dministrator  JM    TOUT
                self.column_panel_admin.visible = True
                self.column_panel_others.visible = True
                #self.bt_gestion_stages.visible = True
                self.flow_panel_admin_only.visible = True
                
                
            if user["role"] == "B":                               # Bureaux    Visu stages, recherches et modif
                self.flow_panel_admin_only.visible = False   # Tools stages de JM
                self.column_panel_others.visible = False     # BT des stagiaires
                self.column_panel_admin.visible = True       

            if user["role"] == "J":                               # Bureaux JC     TOUT sauf recherches
                self.column_panel_admin.visible = True
                self.flow_panel_admin_only.visible = False
                self.flow_panel_bureaux.visible = False
                self.flow_panel_visu.visible = True
                self.column_panel_others.visible = False          # pas BT des stagiaires
                self.flow_panel_visu.visible = True
                
            if user["role"] == "T":                               # Tuteurs MotoN:   Juste Saisie Formulaire de suivi et pré requis
                self.column_panel_others.visible = True
                self.button_qcm.visible = False
                self.button_form_satisf.visible = False
                

            if user["role"] == "F":                               # Formateurs: QCM, Pré requis, PREVOIR CREATION D'UN QCM 
                self.button_qcm.visible = True
                self.button_form_satisf.visible = False
                self.button_form_suivi_stage.visible = False

            
        else: #pas de user
            self.column_panel_bureaux.visible = False
            self.column_panel_admin.visible = False
            self.column_panel_others.visible = False
            

    def button_parametres_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Parametres import Parametres
        open_form("Parametres")
