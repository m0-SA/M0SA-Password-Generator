import secrets
import string
import pyperclip
import customtkinter 

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

#tkinter functions
def lengthLabelUpdate(lengthVal):
    value = int(slider.get())
    sliderLabel.configure(text = f"Length: {value}")

def copyPass():
    pyperclip.copy(passwordVar.get())
    copyConfirm.configure(text="Copied!")
    app.after(2000, lambda: copyConfirm.configure(text = ""))

# system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# main frame
app = customtkinter.CTk()
app.geometry("720x300")
app.resizable(False, False)
app.title("M0SA Password Generator")

# UI
title = customtkinter.CTkLabel(app, text = "Select Password Options", font = ("Arial", 32))
title.pack(padx = 10, pady = 10)

#options
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
