import os
import sys
import zipfile
import tkinter as tk
from io import BytesIO
from urllib.request import urlopen
from distutils.version import LooseVersion
from PIL import Image, ImageTk
import github3
import shutil

__version__ = "5.0.0"  # Exemple de version

# Fonction pour extraire le contenu d'une archive zip en mémoire
def extract_zipfile(zip_bytes):
    with zipfile.ZipFile(BytesIO(zip_bytes)) as zfile:
        zfile.extractall("update")

# Vérification de la version de l'application
def check_version():
    # Récupération des informations du dépôt
    gh = github3.GitHub()
    repo = gh.repository("Prismaexe", "capybaraclickers")
    latest_release = repo.latest_release()
    # Récupération de la dernière version
    latest_version = LooseVersion(latest_release.tag_name)
    # Comparaison avec la version actuelle
    if latest_version > LooseVersion(__version__):
        # Téléchargement de l'archive zip de la dernière version
        zip_url = latest_release.zipball_url
        zip_bytes = urlopen(zip_url).read()
        # Extraction des fichiers de l'archive dans le dossier "update"
        extract_zipfile(zip_bytes)

# Vérification de la version de l'application au démarrage
check_version()

root = tk.Tk()
root.geometry("980x552")
root.title("Gay Clickerr")

image = Image.open("capybara.png")
resized_image = image.resize((50, 50))
photo = ImageTk.PhotoImage(resized_image)
label = tk.Label(image=photo)
label.pack(anchor="center")

try:
    with open("score.txt", "r") as file:
        counter_value = int(file.read())
except FileNotFoundError:
    counter_value = 0

counter = tk.IntVar()
counter.set(counter_value)

def increment_counter(event):
    counter.set(counter.get() + 1)
label.bind("<Button-1>", increment_counter)
counter_label = tk.Label(textvariable=counter)
counter_label.pack()

def save_counter():
    with open("score.txt", "w") as file:
        file.write(str(counter.get()))
    root.update()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", save_counter)

root.mainloop()

# Nettoyage du dossier "update" après la fermeture de l'application
shutil.rmtree("update")
