from ._anvil_designer import Visu_trombiTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras.PageBreak import PageBreak


# Visualisation du TROMBI sur un XY panel
class Visu_trombi(Visu_trombiTemplate):
    def __init__(self,num_stage, intitule, pdf_mode=False, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.num_stage = num_stage
        self.intitule = intitule
        self.pdf_mode = pdf_mode
        larg = 175 # largeur image en pixel
        inter = 4  # Interval entre image
       
        if self.pdf_mode == True:
            self.button_annuler.visible = False
            self.button_annuler2.visible = False
            
        #lecture du fichier père stages
        stage_row = app_tables.stages.get(numero=int(num_stage))    
        cod = stage_row["code"]['code']
        date = str(stage_row["date_debut"].strftime("%d/%m/%Y"))
        self.label_titre.text = "Trombi stagiaires, " + cod + " du " + date + ".   (Stage num " +num_stage+")"
        
        # extraction de la liste (fonction list())
        rows = list(app_tables.stagiaires_inscrits.search(
            tables.order_by("name", ascending=True),
            stage=stage_row
        ))     
        nb_stagiaires = len(rows)                      # nb de stagiaires
        print("nb-stagiaires", nb_stagiaires)

        """ ***************** BOUCLE sur nb stgiaires ds liste *************"""
        xx = 1   # position (x=1, y=1)
        yy = 1
        cpt_stagiaire = 0
        cpt_ligne = 1
        for row in rows :
            cpt_stagiaire += 1  # incrément compteur
       
            #lecture fichier users à partir du mail
            mel=row["user_email"]['email']
            stagiaire = app_tables.users.get(email=mel)    
            if stagiaire :
                #Photo
                table_pic = stagiaire['photo']
                """
                if orig_pic != None:
                    thumb_pic = anvil.image.generate_thumbnail(orig_pic, 160)
                else:
                    thumb_pic = None
                """
                self.im = Image(background="white", 
                                    display_mode="shrink_to_fit",
                                    height = larg,
                                    source = table_pic,
                                    spacing_below = None,
                                    horizontal_align = "center",
                                    border = "1px solid black",
                                    visible = True,
                                    tag = mel
                                    )
                #self.im.set_event_handler('mouse_down',self.im_mouse_down)            #POUR RENDRE L'IMAGE CLICKABLE, REVALIDER CETTE LIGNE
                try:  #au cas où prenom vide 
                    txt = stagiaire['nom'] + " " + stagiaire['prenom']
                except:
                    txt = stagiaire['nom']
                
                self.bt = Button(text=txt, tag = mel, spacing_above = None, background="", foreground="blue", bold=True, font_size = 11, enabled = True)
                self.bt.set_event_handler('click',self.bt_click)
                
                self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                self.xy_panel.add_component(self.bt, x=xx, y=yy+larg, width = larg)  #nom,prénom

                if cpt_stagiaire % 4 == 0 : # (modulo 4) si 4eme image de la ligne affichée, j'initialise à 1ere image et saute la ligne
                    if cpt_ligne == 4:      # si 4eme image de la 4eme ligne, page break
                        cpt_ligne == 0
                        self.add_component(PageBreak())      # si en création de pdf, je saute une page après 4 lignes
                    xx = 1
                    yy += 239
                    cpt_ligne += 1
                else :                      # pas 4eme image, je décalle à la prochaine image
                    xx = xx + larg + inter

                #print("ligne ", cpt_ligne) 
                #print("stagiaire", cpt_stagiaire)  
            else:
                """ si pas de stagiaire """
                print("stagiaire non trouvé par son mail")
        doc = fast_pdf.Visu_trombi()
        #display
        doc.preview()
                
    """ *************************************************************************************************************************************"""
    """ ******************************              Gestion des évenements click sur image ou nom, extraction grace au TAG de l'image ou nom """
    def bt_click(self, **event_args):
        """This method is called when the link is clicked"""
        """ contenu du dictionaire event_args 
        {'button': 1, 'keys': {'meta': False, 'shift': False, 'ctrl': False, 'alt': False}, 'sender': <anvil.Image object>, 'event_name': 'mouse_down'}"""
        #print(event_args) # c'est un dictionnaire contenant les infos de lévenement
        mel = event_args["sender"].tag   # j'extrai le tag du sender (l'image)
        from ..Saisie_info_apres_visu import Saisie_info_apres_visu
        open_form('Saisie_info_apres_visu', mel, self.num_stage, self.intitule, provenance="trombi")
  
    def im_mouse_down(self, x, y, **event_args):
        """This method is called when the mouse cursor enters this component"""
        """ contenu du dictionaire event_args 
        {'button': 1, 'keys': {'meta': False, 'shift': False, 'ctrl': False, 'alt': False}, 'sender': <anvil.Image object>, 'event_name': 'mouse_down'}"""
        #print(event_args) #c'est un dictionnaire contenant les infos de lévenement
        mel = event_args["sender"].tag   # j'extrai le tag du sender (l'image)
        #print("mail",mel)
        from ..Saisie_info_apres_trombi import Saisie_info_apres_trombi
        open_form('Saisie_info_apres_trombi', self.num_stage, self.intitule, mel, provenance="trombi")
    
    def button_retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')

    def button_retour2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_retour_click()

