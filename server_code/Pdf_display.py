import anvil.server

@anvil.server.callable
def get_pdf_url(file):
    return file.get_url()