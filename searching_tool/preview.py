import tkinter as tk
from tkinter import Text, Scrollbar, Toplevel
from PIL import Image, ImageTk
import fitz  # PyMuPDF
from docx import Document
import cv2
import io

#------------------------------------------------------------------------------------------------#

def preview_image(root, path):
    """ Prévisualiser une image. """
    preview_window = Toplevel(root)
    preview_window.title("Prévisualisation de l'image")
    preview_window.geometry("1200x1200")  # Taille plus grande pour la fenêtre de prévisualisation
    img = Image.open(path)
    img.thumbnail((1100, 1100))  # Ajuster la taille de l'image
    img = ImageTk.PhotoImage(img)
    lbl = tk.Label(preview_window, image=img)
    lbl.image = img
    lbl.pack(expand=True, fill=tk.BOTH)

#------------------------------------------------------------------------------------------------#

def preview_text(root, path):
    """ Prévisualiser un fichier texte. """
    preview_window = Toplevel(root)
    preview_window.title("Prévisualisation du texte")
    preview_window.geometry("1200x1200")  # Taille plus grande pour la fenêtre de prévisualisation
    text_widget = Text(preview_window, wrap='word', font=("Helvetica", 18))  # Police plus grande
    scrollbar = Scrollbar(preview_window, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    with open(path, 'r', encoding='utf-8') as file:
        text_widget.insert('1.0', file.read())

#------------------------------------------------------------------------------------------------#

def preview_pdf(root, path):
    """ Prévisualiser un fichier PDF. """
    preview_window = Toplevel(root)
    preview_window.title("Prévisualisation du PDF")
    preview_window.geometry("1200x1200")  # Taille plus grande pour la fenêtre de prévisualisation
    text_widget = Text(preview_window, wrap='word', font=("Helvetica", 18))  # Police plus grande
    scrollbar = Scrollbar(preview_window, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    with fitz.open(path) as doc:
        for page in doc:
            text_widget.insert('end', page.get_text())
            extract_and_display_images_from_page(page, text_widget)

#------------------------------------------------------------------------------------------------#

def preview_docx(root, path):
    """ Prévisualiser un fichier Word. """
    preview_window = Toplevel(root)
    preview_window.title("Prévisualisation du document Word")
    preview_window.geometry("1200x1200")  # Taille plus grande pour la fenêtre de prévisualisation
    text_widget = Text(preview_window, wrap='word', font=("Helvetica", 18))  # Police plus grande
    scrollbar = Scrollbar(preview_window, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    doc = Document(path)
    for para in doc.paragraphs:
        text_widget.insert('end', para.text + '\n')

#------------------------------------------------------------------------------------------------#

def preview_code(root, path):
    """ Prévisualiser un fichier de code source. """
    preview_window = Toplevel(root)
    preview_window.title("Prévisualisation du code")
    preview_window.geometry("1200x1200")  # Taille plus grande pour la fenêtre de prévisualisation
    text_widget = Text(preview_window, wrap='word', font=("Courier", 18))  # Police de type code plus grande
    scrollbar = Scrollbar(preview_window, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    with open(path, 'r', encoding='utf-8') as file:
        text_widget.insert('1.0', file.read())

#------------------------------------------------------------------------------------------------#

def preview_video(root, path):
    """ Prévisualiser un fichier vidéo. """
    preview_window = Toplevel(root)
    preview_window.title("Prévisualisation de la vidéo")
    preview_window.geometry("1200x1200")  # Taille plus grande pour la fenêtre de prévisualisation
    video_label = tk.Label(preview_window)
    video_label.pack(expand=True, fill=tk.BOTH)
    cap = cv2.VideoCapture(path)

    def show_frame():
        ret, frame = cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
            video_label.after(10, show_frame)
        else:
            cap.release()
            video_label.imgtk = None

    show_frame()

#------------------------------------------------------------------------------------------------#

def preview_generic(root, path):
    """ Prévisualiser un fichier générique. """
    preview_window = Toplevel(root)
    preview_window.title("Prévisualisation de fichier")
    preview_window.geometry("1200x1200")  # Taille plus grande pour la fenêtre de prévisualisation
    text_widget = Text(preview_window, wrap='word', font=("Helvetica", 18))  # Police plus grande
    scrollbar = Scrollbar(preview_window, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        text_widget.insert('1.0', file.read())

#------------------------------------------------------------------------------------------------#

def extract_and_display_images_from_page(page, text_widget):
    """ Extraire et afficher les images d'une page PDF. """
    images = page.get_images(full=True)
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = fitz.Pixmap(page.parent, xref)
        if base_image.alpha:
            base_image = fitz.Pixmap(fitz.csRGB, base_image)
        img = Image.open(io.BytesIO(base_image.tobytes()))
        img.thumbnail((300, 300))  # Ajuster la taille des images extraites
        img = ImageTk.PhotoImage(img)
        text_widget.image_create('end', image=img)
        text_widget.insert('end', '\n')

#------------------------------------------------------------------------------------------------#