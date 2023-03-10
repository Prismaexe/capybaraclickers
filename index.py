import requests
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

# Récupération de la dernière release sur GitHub
url = "https://api.github.com/repos/Prismaexe/capybaraclickers/releases/latest"
response = requests.get(url)
if response.status_code == 200:
    release_data = response.json()
    latest_version = release_data['tag_name']
    current_version = None
    try:
        with open('version.txt', 'r') as f:
            current_version = f.read().strip()
    except FileNotFoundError:
        pass
    if current_version != latest_version:
        # Mettre à jour l'application
        pass

root.mainloop()
