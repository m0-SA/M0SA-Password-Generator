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

def lengthLabelUpdate(lengthVal):
    value = int(slider.get())
    sliderLabel.configure(text = f"Length: {value}")

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


# system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# main frame
app = customtkinter.CTk()
app.geometry("1200x400")
app.resizable(False, False)
app.title("M0SA Password Generator")

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

# options
sliderFrame = customtkinter.CTkFrame(app, fg_color="transparent")
sliderFrame.pack(pady = (10, 10), padx = 20, fill = "x")

slider = customtkinter.CTkSlider(sliderFrame, 
                                 from_ = 4, 
                                 to = 64,
                                 width = 360,
                                 height = 20, 
                                 number_of_steps = 60, 
                                 progress_color = "purple", 
                                 fg_color = "white",
                                 button_color = "dark grey",
                                 button_hover_color = "grey",
                                 command = lengthLabelUpdate)
slider.set(16)
slider.pack(side ="right", expand = True, fill = "x", padx = (20,20), pady = (0,5))

sliderLabel = customtkinter.CTkLabel(sliderFrame, text = "Length: 16", font = ("Arial", 18))
sliderLabel.pack(pady=(0, 10))

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

# run loop
app.mainloop()
