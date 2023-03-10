import os
import requests
from github import Github

# Récupération du nom de l'utilisateur Github et du nom du repository
GITHUB_USER = "Prismaexe"
GITHUB_REPO = "capybaraclickers"

# Connexion à l'API Github
g = Github()

# Récupération des informations sur la dernière release
repo = g.get_user(GITHUB_USER).get_repo(GITHUB_REPO)
latest_release = repo.get_latest_release()

# Récupération du numéro de version de la dernière release
latest_version = latest_release.tag_name

# Récupération du numéro de version de l'application
with open('version.txt', 'r') as f:
    current_version = f.read().strip()

# Comparaison des deux versions
if current_version != latest_version:
    # Téléchargement du fichier de la dernière release
    release_file = latest_release.get_assets()[0]
    download_url = release_file.browser_download_url
    response = requests.get(download_url)

    # Enregistrement du fichier téléchargé
    with open(release_file.name, 'wb') as f:
        f.write(response.content)

    # Mise à jour de l'application
    os.system(f'mv {release_file.name} app/')
    with open('version.txt', 'w') as f:
        f.write(latest_version)

import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("980x552")
root.title("Capybara Clicker")

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
