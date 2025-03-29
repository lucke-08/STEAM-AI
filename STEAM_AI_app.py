import subprocess
import importlib.util
import sys

dependencies = {
    "asyncio": "3.4.3",
    "webbrowser": "3.12.3",
    "pymupdf": "1.24.5",
    "colorama": "0.4.6",
    "customtkinter": "5.2.2",
    "openai": "1.30.5",
    "requests": "2.32.3",
    "Pillow": "10.3.0"
}

def is_installed(package_name):
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_dependency(dependency, version=None):
    if version:
        subprocess.run([sys.executable, "-m", "pip", "install", f"{dependency}=={version}"])
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", dependency])

for dependency, version in dependencies.items():
    if not is_installed(dependency):
        print(f"Installing {dependency}...")
        try:
            install_dependency(dependency, version)
            print(f"{dependency} installed successfully!\n")
        except Exception as e:
            print(f"Error installing {dependency}:\n{e}")

try:
    import webbrowser
    import customtkinter
    from openai import OpenAI
    import threading
    import fitz
    import requests
    from colorama import Fore, Back, Style, Cursor
    from PIL import Image, ImageTk
    from io import BytesIO
except ImportError as e:
    print(f"Error importing a library:\n{e}")

n_msg = 0

def FumettoAreaBot(msg):
    global n_msg
    n_msg += 1
    
    Frame = customtkinter.CTkFrame(scrollable_frame, fg_color="#f4f6f8", corner_radius=8)
    Frame.grid(row=n_msg, column=0, sticky="w", padx=10, pady=5)

    Label = customtkinter.CTkLabel(Frame, text=msg, wraplength=350, anchor="w", justify="left", text_color="#000000")
    Label.pack(padx=10, pady=5)
    
    scroll_to_bottom()

def FumettoAreaUser(msg):
    global n_msg
    n_msg += 1

    Frame = customtkinter.CTkFrame(scrollable_frame, fg_color="#00363d", corner_radius=8)
    Frame.grid(row=n_msg, column=0, sticky="e", padx=10, pady=5)

    Label = customtkinter.CTkLabel(Frame, text=msg, wraplength=350, anchor="e", justify="right", text_color="#ffffff")
    Label.pack(padx=10, pady=5)
    
    scroll_to_bottom()

def scroll_to_bottom():
    scrollable_frame.update_idletasks()
    canvas = scrollable_frame._parent_canvas
    canvas.yview_moveto(1.0)


chat_history = []

def send_message_to_server():
    user_message = entry.get()
    if not user_message:
        return

    FumettoAreaUser(user_message)
    chat_history.append({"role": "user", "content": user_message})
    entry.delete("0", "end")

    full_response = ""

    payload = {
        "messages": chat_history
    }

    response = requests.post("https://SteamAI.pythonanywhere.com/send_message_to_bot", json=payload)

    if response.status_code == 200:
        full_response = response.json().get("response", "")
    else:
        full_response = "Errore nella risposta al server."

    FumettoAreaBot(full_response)
    chat_history.append({"role": "assistant", "content": full_response})

def wikibuttoncmd():
    webbrowser.open_new_tab("https://sites.google.com/view/steam-development/wiki")
def sitebuttoncmd():
    webbrowser.open_new_tab("https://sites.google.com/view/steam-development/web-chat")
def sendbuttoncmd():
    threading.Thread(target=send_message_to_server).start()
def send(event):
    threading.Thread(target=send_message_to_server).start()

app = customtkinter.CTk()
app.title("STEAM AI | powered by STEAM Development & OpenAI")
app.geometry("500x500")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
customtkinter.set_appearance_mode("dark")


pil_steamlogoext = Image.open(BytesIO(requests.get("https://SteamAI.pythonanywhere.com/static/steam_ai_logo.png").content))
resized_steamlogoext = pil_steamlogoext.resize((250, 104)) #1263 x 523
steamlogoext = customtkinter.CTkImage(light_image=resized_steamlogoext,dark_image=resized_steamlogoext,size=(75,30))

pil_manuale = Image.open(BytesIO(requests.get("https://SteamAI.pythonanywhere.com/static/manual_icon.png").content))
resized_manuale = pil_manuale.resize((50, 50)) #1263 x 523
manuale = customtkinter.CTkImage(light_image=resized_manuale,dark_image=resized_manuale)

pil_webico = Image.open(BytesIO(requests.get("https://cdn-icons-png.freepik.com/256/1006/1006771.png").content))
resized_webico = pil_webico.resize((50, 50)) #1263 x 523
webico = customtkinter.CTkImage(light_image=resized_webico,dark_image=resized_webico)


header = customtkinter.CTkFrame(master=app, fg_color="transparent")
header.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
header.grid_columnconfigure(0, weight=1)
header.grid_columnconfigure(1, weight=1)
header.grid_columnconfigure(2, weight=1)

sitebutton = customtkinter.CTkButton(header, text="Web chat", command=sitebuttoncmd, width=35, height=35, image=webico)
sitebutton.grid(row=0, column=0, sticky="nsw", padx=(10,3), pady=10)

label = customtkinter.CTkLabel(header, text="", image=steamlogoext)
label.grid(row=0, column=1, sticky="nsew", pady=10, padx=0)

wikibutton = customtkinter.CTkButton(header, text="Manuale", image=manuale, command=wikibuttoncmd, width=35, height=35)
wikibutton.grid(row=0, column=2, sticky="nse", padx=(3,10), pady=10)


scrollable_frame = customtkinter.CTkScrollableFrame(app)
scrollable_frame.grid(row=1, column=0, sticky="nsew")
scrollable_frame.grid_columnconfigure(0, weight=1)


bottom = customtkinter.CTkFrame(master=app, fg_color="transparent")
bottom.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
bottom.grid_columnconfigure(0, weight=1)

entry = customtkinter.CTkEntry(bottom, placeholder_text="Scrivi un messaggio allo STEAM BOT", border_color= "#4e5f69")
entry.grid(row=0, column=0, sticky="ew", padx=(10,2), pady=0)

disclaimer = customtkinter.CTkLabel(bottom, text="La STEAM AI potrebbe commettere errori siccome basata su Groq / Llama 3\nL'istituzione non è responsabile in caso di risposte errata", text_color="#B4B4B4")
disclaimer.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=3)

sendbutton = customtkinter.CTkButton(bottom, text="Invia", command=sendbuttoncmd, width=60)
sendbutton.grid(row=0, column=1, sticky="ew", padx=(2,10), pady=0)


entry.bind("<Return>", send)

FumettoAreaBot("Ciao. Hai una domanda? Sono qui per aiutare. Non esitare a chiedere.")

app.mainloop()
