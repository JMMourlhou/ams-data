from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ....import Pre_R_doc_name        # Pour générer un nouveau nom au document chargé
from ....Pre_Visu_img_Pdf import Pre_Visu_img_Pdf   #pour afficher un document avant de le télécharger

class ItemTemplate6(ItemTemplate6Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.test_img_just_loaded = False  # pour savoir si l'image vient d'être chargée (voir visu image)
        txt0 = "Pour le " + self.item['code_txt']+" de "  # le stage
        txt1 = self.item['nom']+"."+self.item['prenom'][0]+" : "
        txt2 = self.item['requis_txt']  # l'intitulé
        self.label_en_tete_pr.text = txt0 +txt1 + txt2
        
        if self.item['doc1'] is not None:
            self.image_1.source = self.item['thumb']              # DISPLAY L'image basse qualité
            self.button_visu.visible = True
            self.button_del.visible = True
        else:
            self.button_del.visible = False
        
        self.stage_num =   self.item['stage_num'] 
        self.item_requis = self.item['item_requis']
        self.email =       self.item['stagiaire_email']
    
    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            n = Notification("Attendre la fin du traitement pour prendre une autre photo !",
                 timeout=3)   # par défaut 2 secondes
            n.show()
            print("type fichier chargé par file loader: ", type(file))
            # nouveau nom doc SANS extension
            self.new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse 
            print("file just loaded, new file name: ",self.new_file_name)
            
            # Type du fichier loaded ?
            path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))

            # sauvegarde du 'file' image en jpg, resized 1000 x 800   ou   800x1000  plus thumnail 150 x 100   ou  100 x 150
            if file_extension == ".jpg" or file_extension == ".jpeg" or file_extension == ".bmp" or file_extension == ".gif" or file_extension == ".jif" or file_extension == ".png":   
                self.save_file(file, self.new_file_name, file_extension, False, "")
            if file_extension == ".pdf":      
                # génération du JPG à partir du pdf bg task en bg task
                self.task_pdf = anvil.server.call('pdf_into_jpg_bgtasked', file, self.new_file_name, self.item['stage_num'], self.item['stagiaire_email'])    
                self.timer_2.interval=0.5   
        self.file_loader_1.visible = False
            
    def button_visu_click(self, **event_args):
        """This method is called when the button is clicked"""
        # nouveau nom doc
        new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse
        # si doc type jpg ds table
        if self.image_1.source != "":
            self.button_visu.visible = True
            from ....Pre_Visu_img_Pdf import Pre_Visu_img_Pdf  # pour visu du doc
            if self.test_img_just_loaded:   # image vient d'etre chargée et self.item['doc1'] n'est pas à jour, re lecture avant affichage
                row = app_tables.pre_requis_stagiaire.get(stage_num=self.stage_num,
                                                          stagiaire_email=self.email,
                                                          item_requis=self.item_requis)
                if row:
                    open_form('Pre_Visu_img_Pdf', row['doc1'], new_file_name, self.stage_num, self.email, self.item_requis, origine="admin")
            else:  
                open_form('Pre_Visu_img_Pdf', self.item['doc1'], new_file_name, self.stage_num, self.email, self.item_requis, origine="admin")
                
    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        result = anvil.server.call('pr_stagiaire_del',self.item['stagiaire_email'], self.item['stage_num'], self.item['item_requis'], "efface" )  # mode effact du pr, pas de destruction
        if result:
            self.image_1.source = None
            self.button_visu.visible = False
            self.button_del.visible = False
        else:
            alert("Pré Requis non enlevé")

    def save_file(self, file, new_file_name, file_extension):
        # Sauvegarde du 'file' jpg
        # Avec loading_indicator, appel BG TASK
        self.test_img_just_loaded = True  # indique que l'image, donc self.item['doc1'], a changé
        self.task_img = anvil.server.call('run_bg_task_save_jpg', self.item, file, new_file_name, file_extension)    
        self.timer_1.interval=0.5

    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        if self.task_img.is_completed(): # lecture de l'image sauvée en BG task
            print("fin")
            row = app_tables.pre_requis_stagiaire.get(
                                                        stage_num=self.stage_num,
                                                        item_requis=self.item_requis,
                                                        stagiaire_email=self.email
                                                    )
            
            if row:
                self.image_1.source = row['thumb']
                self.button_visu.visible = True  
                self.button_del.visible = True
            else:
                alert("Row stagiaire non trouvé")
                self.button_visu.visible = False  
                self.button_del.visible = False
            self.timer_1.interval=0
            anvil.server.call('task_killer',self.task_img)

    def timer_2_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        if self.task_pdf.is_completed(): # lecture de l'image sauvée en BG task
            # lecture de la liste sauvée par bg task ds row du stagiaire_inscrit
            self.timer_2.interval=0
            anvil.server.call('task_killer',self.task_pdf)
            
            row = app_tables.stagiaires_inscrits.get(q.fetch_only("temp_pr_pdf_img"),
                                                      stage=self.item['stage_num'],
                                                      user_email=self.item['stagiaire_email']
                                                      )
            if row:
                
                # Venant d'une table et non d'un file loader, file est un lazy BlobMedia
                file=row['temp_pr_pdf_img']
                print("type fichier chargé de la table : ", type(file))
                self.image_1.source = file        # affichage de l'image anciennement pdf transformée en jpg 
                
                print(f'url: {file.url}')
                print(f'content_type: {file.content_type}')
                print(f'length: {file.length} bytes')
                # This will be `None` since this is a website, not a file
                print(f'name: {file.name}')
                # Only print the first 15 bytes
                print(f'raw bytes: {file.get_bytes()[:15]} ...')

                """  ---------------------------------------------------------------------------------------------------------------------------------------------
                TRANSFORMATION D'UN LAZY MEDIA (img qui vient d'une table) EN BLOB MEDIA (En sortie du file loader et transformable en SERVER side pour resize...)
                """
                media_object = anvil.URLMedia(file.url)
                # -----------------------------------------------------------------------------------------------------------------------------------------------
                self.save_file(media_object, self.new_file_name, ".jpg")
                #self.save_file(self.image_1.source, self.new_file_name, ".jpg", True, media_object)
                
            else:
                alert('timer_2_tick: row stagiaire inscrit non trouvée')
            
        





