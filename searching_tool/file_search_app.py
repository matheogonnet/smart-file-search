import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
from PIL import Image
import customtkinter as ctk  # Import de customtkinter pour l'interface graphique personnalisée
from pathlib import Path
from .helpers import resource_path
from .preview import (preview_image, preview_text, preview_pdf, preview_docx, preview_code, preview_video, preview_generic)

#------------------------------------------------------------------------------------------------#

class FileSearchApp:
    """ Classe principale de l'application de recherche de fichiers et de dossiers.
    
    Attributes: 
    - root (tk.Tk): La fenêtre principale de l'application.
    - search_directory (str): Le répertoire de recherche actuel.
    - search_type (tk.StringVar): Le type de recherche (fichier ou dossier).
    - file_type (tk.StringVar): Le type de fichier à rechercher.
    - selected_extensions (dict): Les extensions de fichiers sélectionnées pour chaque type de fichier.
    - extension_vars (dict): Les variables de contrôle pour les extensions de fichiers.
    - extension_menus (dict): Les menus déroulants pour les extensions de fichiers.
    - preview_window (tk.Toplevel): La fenêtre de prévisualisation actuelle.
    
    Methods:
    - __init__(root): Initialiser l'application de recherche de fichiers et de dossiers.
    - setup_ui(): Configuration des composants de l'interface utilisateur.
    - setup_bindings(): Configuration des bindings d'événements.
    - close_menu(event): Fermer tous les menus contextuels ouverts.
    - on_key_release(event): Action déclenchée lors de la saisie dans le champ de recherche.
    - select_directory(): Ouvrir une boîte de dialogue pour sélectionner le répertoire de recherche.
    - update_current_dir_label(): Mettre à jour l'étiquette du répertoire actuel.
    - search_files(search_term): Rechercher des fichiers ou des dossiers correspondant au terme de recherche.
    - list_all_files(): Lister tous les fichiers et dossiers dans le répertoire de recherche.
    - get_selected_extensions(file_type): Obtenir les extensions de fichiers sélectionnées pour le type de fichier donné.
    - display_result(name, full_path, index): Afficher un résultat de recherche dans l'arbre de résultats.
    - open_selected_item(event): Ouvrir l'élément sélectionné.
    - reset_filters(): Réinitialiser tous les filtres de recherche.
    - show_help(): Afficher l'aide de l'application.
    - on_closing(): Fermer l'application proprement.
    - show_extensions_menu(selected_file_type): Afficher le menu des extensions de fichier pour le type de fichier sélectionné.
    - toggle_extension(file_type, extension, var): Activer ou désactiver une extension de fichier dans le menu des extensions.
    - search_content_in_file(file, root, search_term): Rechercher un terme dans le contenu des fichiers.
    - preview_selected_item(event): Prévisualiser l'élément sélectionné.
    - open_preview_window(path): Ouvrir la fenêtre de prévisualisation pour le fichier sélectionné.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Recherche de Fichiers et Dossiers Modernisée")
        self.root.geometry("1000x600")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Initialisation des variables
        self.search_directory = str(Path.home() / "Documents")  # Répertoire de départ : dossier "Documents" de l'utilisateur
        self.search_type = tk.StringVar(value="fichier")
        self.file_type = tk.StringVar(value="Tous")
        self.selected_extensions = {
            "Documents": [".pdf", ".docx", ".txt"],
            "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
            "Vidéos": [".mp4", ".avi", ".mkv", ".mov"],
            "Code": [".py", ".cpp", ".c", ".java", ".js", ".html", ".css"],
            "Tableurs": [".xls", ".xlsx", ".csv"],
            "PowerPoint": [".ppt", ".pptx"]
        }
        self.extension_vars = {}
        self.extension_menus = {}
        self.preview_window = None

        # Configuration de l'interface utilisateur et des bindings
        self.setup_ui()
        self.setup_bindings()

    #------------------------------------------------------------------------------------------------#
    
    def setup_ui(self):
        """ Configuration des composants de l'interface utilisateur. """
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configuration du cadre principal
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.rowconfigure(4, weight=1)
        self.frame.columnconfigure((0, 1, 2, 3), weight=1)

        # Étiquette pour le répertoire actuel
        self.current_dir_label = ctk.CTkLabel(self.frame, text="Répertoire actuel : " + os.path.basename(self.search_directory), anchor='center')
        self.current_dir_label.grid(row=0, column=1, pady=5, padx=10, sticky='ew')

        # Bouton pour sélectionner le répertoire
        self.select_dir_button = ctk.CTkButton(self.frame, text="Sélectionner Répertoire", command=self.select_directory, fg_color="#D3D3D3", hover_color="#C0C0C0", text_color="black")
        self.select_dir_button.grid(row=1, column=1, pady=5, padx=10, sticky='ew')

        # Champ de saisie pour la recherche
        self.search_entry = ctk.CTkEntry(self.frame, width=400, placeholder_text="Recherche")
        self.search_entry.grid(row=2, column=1, pady=(30, 12), padx=10, sticky='ew')

        # Boutons radio pour sélectionner le type de recherche (fichier ou dossier)
        self.radio_fichier = ctk.CTkRadioButton(self.frame, text="Fichier", variable=self.search_type, value="fichier")
        self.radio_fichier.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.radio_dossier = ctk.CTkRadioButton(self.frame, text="Dossier", variable=self.search_type, value="dossier")
        self.radio_dossier.grid(row=3, column=2, padx=5, pady=5, sticky='e')

        # Menu déroulant pour sélectionner le type de fichier
        self.file_type_selector = ctk.CTkOptionMenu(self.frame, values=["Tous", "Documents", "Images", "Vidéos", "Code", "Tableurs", "PowerPoint"], variable=self.file_type, command=self.show_extensions_menu)
        self.file_type_selector.grid(row=3, column=1, pady=12, padx=10, sticky='ew')

        # Bouton pour réinitialiser les filtres
        self.reset_button = ctk.CTkButton(self.frame, text="Réinitialiser", command=self.reset_filters, text_color="black")
        self.reset_button.grid(row=3, column=3, pady=12, padx=10, sticky='ew')

        # Arbre de résultats pour afficher les fichiers trouvés
        self.result_tree = ttk.Treeview(self.frame, columns=("Name", "Path"), show='headings', height=15)
        self.result_tree.heading("Name", text="Nom")
        self.result_tree.heading("Path", text="Chemin")
        self.result_tree.column("Name", width=300, anchor="w")
        self.result_tree.column("Path", width=500, anchor="w")
        self.result_tree.grid(row=4, column=0, columnspan=4, pady=12, padx=10, sticky='nsew')

        # Style de l'arbre de résultats
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 20), rowheight=30)
        style.configure("Treeview.Heading", font=("Helvetica", 22, "bold"))

        # Configuration du bouton d'aide avec une icône
        self.help_icon_image = Image.open(resource_path("images/image.png")).resize((20, 20), Image.LANCZOS)
        self.help_icon = ctk.CTkImage(light_image=self.help_icon_image, dark_image=self.help_icon_image, size=(20, 20))
        self.help_button = ctk.CTkButton(self.root, text="Aide", image=self.help_icon, compound="left", command=self.show_help, fg_color="#FFA500", hover_color="#FF8C00", text_color="black")
        self.help_button.place(relx=1.0, rely=0.0, x=-10, y=10, anchor='ne')

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    #------------------------------------------------------------------------------------------------#

    def setup_bindings(self):
        """ Configuration des bindings d'événements. """
        self.search_entry.bind("<KeyRelease>", self.on_key_release)
        self.result_tree.bind("<Double-1>", self.open_selected_item)
        self.result_tree.bind("<ButtonRelease-1>", self.preview_selected_item)
        self.root.bind("<Button-1>", self.close_menu)
    
    #------------------------------------------------------------------------------------------------#

    def close_menu(self, event):
        """ Fermer tous les menus contextuels ouverts. """
        for menu in self.extension_menus.values():
            menu.unpost()
    
    #------------------------------------------------------------------------------------------------#

    def on_key_release(self, event):
        """ Action déclenchée lors de la saisie dans le champ de recherche. """
        self.result_tree.delete(*self.result_tree.get_children())
        search_term = self.search_entry.get().strip()
        if search_term:
            self.search_files(search_term)
        else:
            self.list_all_files()

    #------------------------------------------------------------------------------------------------#

    def select_directory(self):
        """ Ouvrir une boîte de dialogue pour sélectionner le répertoire de recherche. """
        selected_directory = filedialog.askdirectory(initialdir=self.search_directory)
        if selected_directory:
            self.search_directory = selected_directory
            self.update_current_dir_label()
            messagebox.showinfo("Répertoire sélectionné", f"Répertoire de recherche : {self.search_directory}")

    #------------------------------------------------------------------------------------------------#

    def update_current_dir_label(self):
        """ Mettre à jour l'étiquette du répertoire actuel. """
        self.current_dir_label.configure(text="Répertoire actuel : " + os.path.basename(self.search_directory))

    #------------------------------------------------------------------------------------------------#

    def search_files(self, search_term):
        """ Rechercher des fichiers ou des dossiers correspondant au terme de recherche. """
        search_type = self.search_type.get()
        file_type = self.file_type.get()
        extensions = self.get_selected_extensions(file_type)

        search_term_lower = search_term.lower()
        search_pattern = re.compile(re.escape(search_term_lower))

        exact_matches = []
        partial_matches = []

        for root, dirs, files in os.walk(self.search_directory):
            if search_type == "fichier":
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        if file.lower() == search_term_lower:
                            exact_matches.append((file, os.path.join(root, file)))
                        elif search_pattern.search(file.lower()):
                            partial_matches.append((file, os.path.join(root, file)))
                        elif self.search_content_in_file(file, root, search_term):
                            partial_matches.append((file, os.path.join(root, file)))
            elif search_type == "dossier":
                for dir in dirs:
                    if search_pattern.search(dir.lower()):
                        partial_matches.append((dir, os.path.join(root, dir)))

        results = sorted(exact_matches + partial_matches, key=lambda x: x[0].lower())
        for i, (name, path) in enumerate(results):
            self.display_result(name, path, i)

    #------------------------------------------------------------------------------------------------#

    def list_all_files(self):
        """ Lister tous les fichiers et dossiers dans le répertoire de recherche. """
        search_type = self.search_type.get()
        file_type = self.file_type.get()
        extensions = self.get_selected_extensions(file_type)

        all_files = []

        for root, dirs, files in os.walk(self.search_directory):
            if search_type == "fichier":
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        all_files.append((file, os.path.join(root, file)))
            elif search_type == "dossier":
                for dir in dirs:
                    all_files.append((dir, os.path.join(root, dir)))

        sorted_files = sorted(all_files, key=lambda x: x[0].lower())
        for i, (name, path) in enumerate(sorted_files):
            self.display_result(name, path, i)

    #------------------------------------------------------------------------------------------------#

    def get_selected_extensions(self, file_type):
        """ Obtenir les extensions de fichiers sélectionnées pour le type de fichier donné. """
        if file_type == "Tous":
            return [ext for exts in self.selected_extensions.values() for ext in exts]
        return [ext for ext, var in self.extension_vars.get(file_type, {}).items() if var.get() == 1]

    #------------------------------------------------------------------------------------------------#

    def display_result(self, name, full_path, index):
        """ Afficher un résultat de recherche dans l'arbre de résultats. """
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        self.result_tree.insert('', 'end', values=(name, full_path), tags=(tag,))

    #------------------------------------------------------------------------------------------------#

    def open_selected_item(self, event):
        """ Ouvrir l'élément sélectionné. """
        selected_item = self.result_tree.focus()
        values = self.result_tree.item(selected_item, 'values')
        path = values[1]
        os.startfile(path)

    #------------------------------------------------------------------------------------------------#

    def reset_filters(self):
        """ Réinitialiser tous les filtres de recherche. """
        self.search_entry.delete(0, tk.END)
        self.search_type.set("fichier")
        self.file_type.set("Tous")
        self.extension_vars.clear()
        for menu in self.extension_menus.values():
            menu.unpost()
        self.extension_menus.clear()
        self.result_tree.delete(*self.result_tree.get_children())
        self.list_all_files()

    #------------------------------------------------------------------------------------------------#

    def show_help(self):
        """ Afficher l'aide de l'application. """
        messagebox.showinfo("Aide", "- Utilisez la barre de recherche pour trouver des fichiers ou dossiers.\n\n"
                                    "- Filtrez et affinez votre recherche en sélectionnant un type de fichier.\n\n"
                                    "- Cliquez sur le bouton de réinitialisation pour effacer tous les filtres.\n\n"
                                    "- Cliquez sur le bouton de sélection de répertoire pour changer de répertoire de recherche.\n\n"
                                    "- Cliquez une fois pour avoir un aperçu du fichier.\n\n"
                                    "- Double-cliquez sur un résultat pour l'ouvrir.")

    #------------------------------------------------------------------------------------------------#

    def on_closing(self):
        """ Fermer l'application proprement. """
        self.root.destroy()
        os._exit(0)

    #------------------------------------------------------------------------------------------------#

    def show_extensions_menu(self, selected_file_type):
        """ Afficher le menu des extensions de fichier pour le type de fichier sélectionné. """
        if selected_file_type == "Tous":
            return
        if selected_file_type not in self.extension_menus:
            menu = Menu(self.root, tearoff=0, font=("Helvetica", 15))
            self.extension_vars[selected_file_type] = {}
            for ext in self.selected_extensions[selected_file_type]:
                var = tk.IntVar(value=1)
                self.extension_vars[selected_file_type][ext] = var
                menu.add_checkbutton(label=ext, variable=var, onvalue=1, offvalue=0, command=lambda e=ext, v=var: self.toggle_extension(selected_file_type, e, v))
            self.extension_menus[selected_file_type] = menu

        self.extension_menus[selected_file_type].post(self.file_type_selector.winfo_rootx(), self.file_type_selector.winfo_rooty() + self.file_type_selector.winfo_height())

    #------------------------------------------------------------------------------------------------#

    def toggle_extension(self, file_type, extension, var):
        """ Activer ou désactiver une extension de fichier dans le menu des extensions. """
        if var.get() == 1:
            self.selected_extensions[file_type].append(extension)
        else:
            self.selected_extensions[file_type].remove(extension)
        self.extension_menus[file_type].unpost()
        self.show_extensions_menu(file_type)

    #------------------------------------------------------------------------------------------------#

    def search_content_in_file(self, file, root, search_term):
        """ Rechercher un terme dans le contenu des fichiers. """
        file_path = os.path.join(root, file)
        try:
            if file.lower().endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return search_term.lower() in f.read().lower()
            elif file.lower().endswith('.pdf'):
                with fitz.open(file_path) as doc:
                    for page in doc:
                        if search_term.lower() in page.get_text().lower():
                            return True
            elif file.lower().endswith('.docx'):
                doc = Document(file_path)
                for para in doc.paragraphs:
                    if search_term.lower() in para.text.lower():
                        return True
        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path}: {str(e).encode('utf-8', errors='ignore')}")
        return False

    #------------------------------------------------------------------------------------------------#

    def preview_selected_item(self, event):
        """ Prévisualiser l'élément sélectionné. """
        if self.preview_window:
            self.preview_window.destroy()
        selected_item = self.result_tree.focus()
        values = self.result_tree.item(selected_item, 'values')
        path = values[1]
        self.open_preview_window(path)

    #------------------------------------------------------------------------------------------------#

    def open_preview_window(self, path):
        """ Ouvrir la fenêtre de prévisualisation pour le fichier sélectionné. """
        if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            preview_image(self.root, path)
        elif path.lower().endswith('.txt'):
            preview_text(self.root, path)
        elif path.lower().endswith('.pdf'):
            preview_pdf(self.root, path)
        elif path.lower().endswith('.docx'):
            preview_docx(self.root, path)
        elif any(path.lower().endswith(ext) for ext in ('.py', '.cpp', '.c', '.java', '.js', '.html', '.css')):
            preview_code(self.root, path)
        elif path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            preview_video(self.root, path)
        else:
            preview_generic(self.root, path)

#------------------------------------------------------------------------------------------------#