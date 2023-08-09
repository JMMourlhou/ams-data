import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *   # to load the alert 
from anvil import open_form


""" This is the startup module.
x représente le nb d'appel du module
Il permet de tester si Fitnesse'd est appelé par une URL en cas de sign in ou pw reset 
je l'incrémente à l'ouverture de home_form
"""
def starting_app(x=1):
    open_form('Main',x) 
    
# quand ouverture normale de l'app ou par URL
starting_app(1)
#alert(x,title="ouverture normale ou par URL module1 Fitness'd")
