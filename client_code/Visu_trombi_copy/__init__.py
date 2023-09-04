from ._anvil_designer import Visu_trombi_copyTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Visu_trombi_copy(Visu_trombi_copyTemplate):
    def __init__(self,num_stage, intitule, pdf_mode=False, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.num_stage = num_stage
        self.intitule = intitule
        self.pdf_mode = pdf_mode
        if self.pdf_mode == True:
            #self.button_annuler.visible = False
            #self.button_pdf.visible = False
            pass

        #lecture du fichier père stages
        stage_row = app_tables.stages.get(numero=int(num_stage))

        # extraction de la liste (fonction list())
        rows = list(app_tables.stagiaires_inscrits.search(
            tables.order_by("name", ascending=True),
            stage=stage_row
        ))
        nb_stagiaires = len(rows)                      # nb de stagiaires

        alert("point0")
        #xy_panel = XYPanel(width=400, height=400, background='red', role='outlined-card', visible=True)
        btn = Button(text="Click me!", background="white", foreground="black")
        self.xy_panel.add_component(btn, x=1, y=1)
        im1 = Image(background="white", source="_/theme/Logo%20AMS.JPG") 
        self.xy_panel.add_component(im1, x=10, y=100)
        
        cpt_stagiaire = 0
        cpt_ligne = 0

       
        #lecture fichier users à partir du mail
        row=rows[0]
        mel=row["user_email"]['email']
        stagiaire = app_tables.users.get(email=mel)
        if stagiaire :
            alert(stagiaire['nom'])
            #Photo
            orig_pic = stagiaire['photo']
            if orig_pic != None:
                thumb_pic = anvil.image.generate_thumbnail(orig_pic, 160)

                im1 = Image(background="white",
                                display_mode="shrink_to_fit",
                                width = 160,
                                height = 160,
                                source = thumb_pic,
                                horizontal_align = "center",
                                visible = True
                            )
                alert("test")
                self.xy_panel.add_component(im1, x=10, y=100)