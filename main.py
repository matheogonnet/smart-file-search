import sys
import os

# Ajoutez le répertoire du projet au sys.path pour permettre l'importation des modules du projet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from searching_tool import FileSearchApp  # Importer FileSearchApp depuis le package searching_tool

if __name__ == "__main__":
    # Initialiser l'interface graphique de l'application
    root = ctk.CTk()
    app = FileSearchApp(root)
    app.list_all_files()
    root.mainloop()  # Lancer la boucle principale de l'interface graphique
