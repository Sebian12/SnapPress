import customtkinter as ctk

b_mode = "light"

def theme(mode):
    global b_mode
    if (mode == "light"):
        b_mode = "dark"
        ctk.set_appearance_mode(b_mode)
    else:
        b_mode = "light"
        ctk.set_appearance_mode(b_mode)

def open_settings():
    settings_window = ctk.CTkToplevel()
    settings_window.title("Settings")
    settings_window.geometry("300x375")

    settings_window.attributes("-topmost", True)

    ctk.CTkSwitch(settings_window,text="Dark mode", command=lambda: theme(b_mode)).pack(side="top", fill="x", padx=10, pady=10)

    return settings_window
