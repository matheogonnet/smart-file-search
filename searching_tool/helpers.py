import os
import sys

def resource_path(relative_path):
    """
    Obtenir le chemin absolu vers une ressource, fonctionne pour le développement et pour PyInstaller.
    
    Parameters:
    relative_path (str): Le chemin relatif de la ressource.

    Returns:
    str: Le chemin absolu de la ressource.
    """
    try:
        # Pour PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Pour le développement
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
