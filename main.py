import secrets
import string
import math
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

    updateEntropy()

    copyButton.configure(state = "normal")
    clearButton.configure(state = "normal")
    
    passwordHistory.append(password)
    updateHistory(password)

def estimateEntropy(length):
    poolSize = len(string.ascii_lowercase)
    if pUppercase.get():
        poolSize += len(string.ascii_uppercase)
    if pDigits.get():
        poolSize += len(string.digits)
    if pSymbols.get():
        poolSize += len(string.punctuation)

    return round(length * math.log2(poolSize), 2)

def entropyStrengthLabel(entropy):
    if entropy < 40:
        return "Weak", "red"
    elif entropy < 60:
        return "Moderate", "orange"
    elif entropy < 80:
        return "Strong", "yellow"
    else:
        return "Very Strong", "green"

def updateEntropy():
    entropy = estimateEntropy(slider.get())
    label, colour = entropyStrengthLabel(entropy)
    entropyLabel.configure(text = f"Password Strength: {label}!", text_color = colour)
    
def copyPass():
    pyperclip.copy(passwordVar.get())
    copyConfirm.configure(text="Copied!")
    app.after(2000, lambda: copyConfirm.configure(text = ""))

def updateHistory(password):
    row = customtkinter.CTkFrame(historyPanel, fg_color="transparent")
    row.pack(fill = "x", pady = 3, padx = 5)

    strengthColour = entropyLabel._text_color
    displayPW = (password[:24] + "…") if len(password) > 24 else password
    label = customtkinter.CTkLabel(row, text = displayPW, anchor = "w", font = ("Arial", 16), text_color = strengthColour)
    
    label.pack(side = "left", fill = "x", expand = True)

    if len(password) > 24:
        CTkToolTip(label, message = password, bg_color = strengthColour)

    btn = customtkinter.CTkButton(row, text = "Copy 📋", width = 40, height = 28, command = lambda p = password: pyperclip.copy(p))
    btn.pack(side = "right", padx = 5)

def clearHistory():
    passwordHistory.clear()
    for widget in historyPanel.winfo_children():
        widget.destroy()
    clearButton.configure(state = "disabled")

def entryChange(val):
    lengthEntry.delete(0, "end")
    lengthEntry.insert(0, str(val))

def onSliderChange(value):
    intVal = int(value)
    lengthVar.set(intVal)
    entryChange(intVal)

def onEntryKeyRelease(event=None):
    val = lengthEntry.get().strip()
    if val.isdigit():
        num = int(val)
        clamped = max(4, min(64, num))
        if num != clamped:
            entryChange(clamped)
        slider.set(clamped)
        lengthVar.set(clamped)
    else:
        slider.set(16)
        lengthVar.set(16)
        entryChange(16)

def adjustLength(delta):
    current = lengthVar.get()
    newValue = max(4, min(64, current + delta))
    lengthVar.set(newValue)
    slider.set(float(newValue))
    entryChange(newValue)

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
sidebar.pack(side = "right", fill = "y", padx = 5, pady = 10)
historyPanel = customtkinter.CTkScrollableFrame(sidebar, width = 350, label_text = "Password History", label_font = ("Arial", 16, "bold"))
historyPanel.pack(fill = "both", expand = True, padx = 5)
clearButton = customtkinter.CTkButton(sidebar, text="Clear History", command=clearHistory, font = ("Arial" , 18), state = "disabled")
clearButton.pack(side = "bottom", fill ="both")

# title
title = customtkinter.CTkLabel(app, text = "M0SA Password Generator", font = ("Arial", 32))
title.pack(padx = 10, pady = 10)

# slider
lengthVar = customtkinter.IntVar(value = 16)
sliderFrame = customtkinter.CTkFrame(app, fg_color = "transparent")
sliderFrame.pack(pady = (10, 10), padx = 20, fill = "x")

lengthLabel = customtkinter.CTkLabel(sliderFrame, text = "Length:", font = ("Arial", 20))
lengthLabel.pack(side = "left", pady = (0, 10), padx = 5)

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
                                 command = onSliderChange
                                 )
slider.set(lengthVar.get())
slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

lengthEntry = customtkinter.CTkEntry(sliderFrame, width = 60, justify = "center")
lengthEntry.insert(0, str(lengthVar.get()))
lengthEntry.pack(side = "left")
lengthEntry.bind("<KeyRelease>", onEntryKeyRelease)

# Inside UI setup (after entry)
minusButton = customtkinter.CTkButton(sliderFrame, text = "-", width = 30, command = lambda: adjustLength(-1), font = ("Arial", 24))
minusButton.pack(side = "left", padx = (5, 0))

plusButton = customtkinter.CTkButton(sliderFrame, text = "+", width = 30, command = lambda: adjustLength(1), font = ("Arial", 24))
plusButton.pack(side = "left", padx = (5, 0))

# options
checkBoxFrame = customtkinter.CTkFrame(app, fg_color = "transparent")
checkBoxFrame.pack(pady = 30, padx = 100, fill = "x")
pUppercase = customtkinter.BooleanVar(value = True)
pDigits = customtkinter.BooleanVar(value = True)
pSymbols = customtkinter.BooleanVar(value = True)

customtkinter.CTkCheckBox(checkBoxFrame, text = "Include Uppercase Letters", variable = pUppercase, font = ("Arial", 16)).pack(side = "left",padx = 15)
customtkinter.CTkCheckBox(checkBoxFrame, text = "Include Digits (0-9)", variable = pDigits, font = ("Arial", 16)).pack(side = "left",padx = 15)
customtkinter.CTkCheckBox(checkBoxFrame, text = "Include Symbols (!@#$...)", variable = pSymbols, font = ("Arial", 16)).pack(side = "left", padx = 15)

# generate button
buttonsFrame = customtkinter.CTkFrame(app, fg_color = "transparent")
buttonsFrame.pack(pady = 20)
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

# entropy

entropyLabel = customtkinter.CTkLabel(app, text = "Password Strength: ", font = ("Arial", 16, "bold"))
entropyLabel.pack(pady = 0)

# run loop
app.mainloop()
