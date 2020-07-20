from tkinter import *

root = Tk()
# set window size
root.geometry("1400x800")


def printName(event):
    print("works")


label_token = Label(root, text="Token", bg="red")
entry_token = Entry(root)
btn_token = Button(root, text="Run!")
btn_token.bind("<Button-1>", printName)

label_token.grid(row=1, column=0, sticky=E)
entry_token.grid(row=0, column=1, sticky=N)
btn_token.grid(row=0, column=2, sticky=E)


root.mainloop()
