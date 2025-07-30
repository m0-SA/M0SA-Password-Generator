import secrets
import string
import pyperclip
import customtkinter 
from CTkToolTip import *

# vars
passwordHistory = []
visibleHistory = False

# functions
def passwordGenerate():
    alphabet = string.ascii_lowercase
    if pUppercase.get():
        alphabet += string.ascii_uppercase
    if pDigits.get():
        alphabet += string.digits
    if pSymbols.get():
        alphabet += string.punctuation

    password = ''.join(secrets.choice(alphabet) for i in range(int(slider.get())))
    passwordVar.set(password)

    copyButton.configure(state = "normal")
    clearButton.configure(state = "normal")
    
    passwordHistory.append(password)
    updateHistory(password)

def copyPass():
    pyperclip.copy(passwordVar.get())
    copyConfirm.configure(text="Copied!")
    app.after(2000, lambda: copyConfirm.configure(text = ""))

def updateHistory(password):
    row = customtkinter.CTkFrame(historyPanel, fg_color="transparent")
    row.pack(fill = "x", pady = 3, padx = 5)

    display_pw = (password[:16] + "…") if len(password) > 16 else password
    label = customtkinter.CTkLabel(row, text=display_pw, anchor = "w", font = ("Arial", 16))
    label.pack(side = "left", fill = "x", expand = True)

    if len(password) > 16:
        CTkToolTip(label, message = password)

    btn = customtkinter.CTkButton(row, text = "Copy 📋", width = 40, height = 28, command = lambda p = password: pyperclip.copy(p))
    btn.pack(side = "right", padx = 5)

def clearHistory():
    passwordHistory.clear()
    for widget in historyPanel.winfo_children():
        widget.destroy()
    clearButton.configure(state = "disabled")

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1200x400")
app.title("Length Control with Live Sync")

# sidebar
sidebar = customtkinter.CTkFrame(app, width = 250)
sidebar.pack(side="right", fill="y", padx=5, pady=10)
historyPanel = customtkinter.CTkScrollableFrame(sidebar, width = 250, label_text = "Password History", label_font = ("Arial", 16, "bold"))
historyPanel.pack(fill = "both", expand = True, padx = 5)
clearButton = customtkinter.CTkButton(sidebar, text="Clear History", command=clearHistory, font = ("Arial" , 18), state = "disabled")
clearButton.pack(side = "bottom", fill ="both")
# title
title = customtkinter.CTkLabel(app, text = "Select Password Options", font = ("Arial", 32))
title.pack(padx = 10, pady = 10)

length_var = customtkinter.IntVar(value=12)

# === Frame for horizontal layout ===
length_frame = customtkinter.CTkFrame(app, fg_color="transparent")
length_frame.pack(pady=20, padx=20, fill="x")

# === Label
label = customtkinter.CTkLabel(length_frame, text="Length:", font=("Arial", 14))
label.pack(side="left", padx=(0, 10))

# === Slider (updates entry)
def on_slider_change(value):
    int_val = int(float(value))
    length_var.set(int_val)
    entry.delete(0, "end")
    entry.insert(0, str(int_val))

slider = customtkinter.CTkSlider(
    length_frame,
    from_=4,
    to=64,
    number_of_steps=60,
    command=on_slider_change,
    progress_color="purple"
)
slider.set(length_var.get())
slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

# === Entry (updates slider live)
def on_entry_keyrelease(event=None):
    val = entry.get().strip()
    if val.isdigit():
        num = int(val)
        clamped = max(4, min(64, num))
        slider.set(clamped)
        length_var.set(clamped)

entry = customtkinter.CTkEntry(length_frame, width=60, justify="center")
entry.insert(0, str(length_var.get()))
entry.pack(side="left")
entry.bind("<KeyRelease>", on_entry_keyrelease)

# options
checkBoxFrame = customtkinter.CTkFrame(app, fg_color = "transparent")
checkBoxFrame.pack(pady = (10, 10), padx = 20, fill = "x")
pUppercase = customtkinter.BooleanVar(value = True)
pDigits = customtkinter.BooleanVar(value = True)
pSymbols = customtkinter.BooleanVar(value = True)

customtkinter.CTkCheckBox(checkBoxFrame, text = "Include Uppercase Letters", variable = pUppercase, font = ("Arial", 16)).pack(side = "left",padx = 15)
customtkinter.CTkCheckBox(checkBoxFrame, text = "Include Digits (0-9)", variable = pDigits, font = ("Arial", 16)).pack(side = "left",padx = 15)
customtkinter.CTkCheckBox(checkBoxFrame, text = "Include Symbols (!@#$...)", variable = pSymbols, font = ("Arial", 16)).pack(side = "left", padx = 15)

# generate button
buttonsFrame = customtkinter.CTkFrame(app, fg_color = "transparent")
buttonsFrame.pack(pady = 10)
passwordVar = customtkinter.StringVar()

generateButton = customtkinter.CTkButton(buttonsFrame, text = "Generate Password",
                                         command = passwordGenerate,
                                         font = ("Arial" , 18)).pack(side = "left", pady = 10)

copyButton = customtkinter.CTkButton(buttonsFrame, text = "Copy 📋", 
                                     command = copyPass, 
                                     font = ("Arial" , 18),
                                     state = "disabled")
copyButton.pack(side = "left", padx = 10)

passwordLabel = customtkinter.CTkEntry(app, textvariable = passwordVar, font = ("Arial", 18), width = 700, justify = "center")
passwordLabel.configure(state = "readonly")
passwordLabel.pack(pady = 10)

copyConfirm = customtkinter.CTkLabel(app, text = "", font = ("Arial", 20), text_color = "green")
copyConfirm.pack()

app.mainloop()