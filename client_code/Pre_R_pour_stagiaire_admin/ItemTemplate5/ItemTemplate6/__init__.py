from ._anvil_designer import ItemTemplate6Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
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
        self.text_area_1.text = self.item['item_requis']['requis']
        self.image_1.source = self.item['thumb_doc1']              # DIPLAY L'image basse qualité (640 x 640)
        self.button_visu.tag = self.item['doc1']             # pour récupérer l'image source pour bt visu
        
        self.stage_num =   self.item['stage_num']
        self.item_requis = self.item['item_requis']
        self.email =       self.item['stagiaire_email']

    
    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file != None:  #pas d'annulation en ouvrant choix de fichier
            # nouveau nom doc
            new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse 
            print(new_file_name)
            # Type de fichier ?
            path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))
            print(file_extension)
            thumb_file = None
            if file_extension == ".jpg":
                thumb_file =  anvil.image.generate_thumbnail(file, 640)
                self.image_1.source = file
                new_file_name = new_file_name + ".jpg"
                # Sauvegarde du 'file' jpg et de son thumb nail
                result, liste_images = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file, file_extension, thumb_file, new_file_name) 
                if result == False:
                    alert("Fichier non sauvé") 
                
            """
            # si 'file' est pdf, je l'affiche au format jpg
            if self.file_extension == ".pdf":
                new_file_name = new_file_name
                liste_images = anvil.server.call('pdf_into_images', stage_num, item_requis, email, new_file_name)
                #extraction 1ere image de la liste (il peut y avoir plusieurs pages)
                file = liste_images[0]
                thumb_file =  anvil.image.generate_thumbnail(file, 640)
                # renvoi en écriture des images générées ds table
                file_extension = ".img"
                new_file_name = new_file_name + ".jpg"
                result = anvil.server.call('modify_pre_r_par_stagiaire', stage_num, item_requis, email, file, file_extension, thumb_file, new_file_name)
                if result == True:
                    alert("Fichier jpg sauvé") 
            """    
            
    
    def button_tele_pdf_click(self, **event_args):
        # finding the stagiaire's row et envoi du row au serveur
        pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = self.stage_num,
                                              stagiaire_email = self.email,
                                              item_requis = self.item_requis                                             
                                             )                                      
        if not pr_requis_row:
            alert("Erreur: stagiaire not found !")
        new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse 
        print(self.image_1.source)
        media_object = anvil.server.call("generate_pdf_from_jpg", self.image_1.source, new_file_name, self.stage_num, self.email, self.item_requis, pr_requis_row)
        anvil.media.download(media_object)    
        """
        if pr_requis_row['doc1']:     #img existe ds le row, je l'affiche ds Pre_visu_img_pdf
            from ....Pre_Visu_img_Pdf import Pre_Visu_img_Pdf  # pour générer un fichier pdf d'une image et la télecharger
            open_form('Pre_Visu_img_Pdf', pr_requis_row['doc1'], new_file_name, stage_num, email, item_requis)
        """

        def button_visu_click(self, **event_args):
            """This method is called when the button is clicked"""
            # nouveau nom doc
            new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse
            # si doc type jpg ds table
            if self.button_visu.tag != None:
                #self.image_1.source = self.item['doc1']              # DIPLAY L'image haute qualité
                from ....Pre_Visu_img_Pdf import Pre_Visu_img_Pdf  # pour visu du doc
                open_form('Pre_Visu_img_Pdf', self.item['doc1'], new_file_name, self.stage_num, self.email, self.item_requis)
        
    def image_1_mouse_down(self, x, y, button, keys, **event_args):
        """This method is called when the button is clicked"""      

        # nouveau nom doc
        new_file_name = Pre_R_doc_name.doc_name_creation(stage_num, item_requis, email)   # extension non incluse
        try:  # si Pdf 
            liste_images = anvil.server.call('pdf_into_images', stage_num, item_requis, email, new_file_name, "visu")
            alert("pdf")
            from ....Pre_Visu_PDF_into_IMG import Pre_Visu_PDF_into_IMG
            open_form('Pre_Visu_PDF_into_IMG', images=liste_images, add_border=True)
        except:  # si JPG
            #alert("jpg doc1")
            self.image_1.source = self.item['doc1']              # DIPLAY L'image haute qualité
            from ....Pre_Visu_img_Pdf import Pre_Visu_img_Pdf  # pour générer un fichier pdf d'une image et la télecharger
            open_form('Pre_Visu_img_Pdf', self.item['doc1'], new_file_name, "visu")





