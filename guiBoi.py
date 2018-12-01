from tkinter import *
from tkinter import ttk

root = Tk()

Label(root, text = "Sponge Bob Title Card Meme Generator",width = 55).grid(row = 0, column = 0, columnspan=2, padx = 5, pady = 5)

Button(root, text = "Select Background File", width = 55).grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5)

Label(root, text = "Text: ", width = 10).grid(row = 3, column = 0, sticky = W, padx = 5, pady = 5)
Entry(root,width = 40).grid(row = 3, column = 1, sticky = E, padx = 5, pady = 5)

Button(root,text = "GENERATE",width = 55).grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5)

root.mainloop()
