#coding: utf-8
from tkinter import *

#Window
WINDOW = Tk()
WINDOW.title("Mimimimimimiiiii")
WINDOW.geometry("1300x600")

def Mimimi():

	txt = text.get("1.0", "end-1c")

	txt = txt.replace("a", "i")
	txt = txt.replace("e", "i")
	txt = txt.replace("o", "i")
	txt = txt.replace("u", "i")

	txt = txt.replace("á", "í")
	txt = txt.replace("é", "í")
	txt = txt.replace("ó", "í")
	txt = txt.replace("ú", "í")

	txt = txt.replace("à", "ì")
	txt = txt.replace("è", "ì")
	txt = txt.replace("ò", "ì")
	txt = txt.replace("ù", "ì")

	txt = txt.replace("ä", "ï")
	txt = txt.replace("ë", "ï")
	txt = txt.replace("ö", "ï")
	txt = txt.replace("ü", "ï")

	txt = txt.replace("â", "î")
	txt = txt.replace("ê", "î")
	txt = txt.replace("ô", "î")
	txt = txt.replace("û", "î")

	txt = txt.replace("A", "I")
	txt = txt.replace("E", "I")
	txt = txt.replace("O", "I")
	txt = txt.replace("U", "I")

	txt = txt.replace("Á", "Í")
	txt = txt.replace("É", "Í")
	txt = txt.replace("Ó", "Í")
	txt = txt.replace("Ú", "Í")

	txt = txt.replace("À", "Ì")
	txt = txt.replace("È", "Ì")
	txt = txt.replace("Ò", "Ì")
	txt = txt.replace("Ù", "Ì")

	txt = txt.replace("Ä", "Ï")
	txt = txt.replace("Ë", "Ï")
	txt = txt.replace("Ö", "Ï")
	txt = txt.replace("Ü", "Ï")

	txt = txt.replace("Â", "Î")
	txt = txt.replace("Ê", "Î")
	txt = txt.replace("Ô", "Î")
	txt = txt.replace("Û", "Î")

	text2.delete('1.0', END)
	text2.insert(END, txt)

def undo1():
	text.edit_undo()

title = Label(WINDOW, text="M  I  M  I  M  E  A  T  O  R", font = ("Emulogic", "30"))
subtitle = Label(WINDOW, text="¡¡Mimimea cualquier texto en un solo click!!", font = ("AR JULIAN", "24"))
rightSpace = Label(WINDOW, text=" ", font = ("Emulogic", "30"))
leftSpace = Label(WINDOW, text=" ", font = ("Emulogic", "30"))
downSpace = Label(WINDOW, text=" ", font = ("Emulogic", "30"))

text = Text(WINDOW, width = 45, font = ("Comic Sans MS", "14"))
text2 = Text(WINDOW, width = 45, font = ("Comic Sans MS", "14"))

scroll = Scrollbar(WINDOW)
scroll.config(command=text.yview)
scroll2 = Scrollbar(WINDOW)
scroll2.config(command=text2.yview)

text.config(yscrollcommand=scroll.set)
text2.config(yscrollcommand=scroll2.set)

mimimiButton = Button(WINDOW, text=">>\n>>\n>>\n\nM\nI\nM\nI\nM\nE\nA\nR\n\n>>\n>>\n>>", font = ("Emulogic", "16"), command=Mimimi)

title.pack(side=TOP, fill=X)
subtitle.pack(side=TOP, fill=X)
downSpace.pack(side=BOTTOM)

leftSpace.pack(side=LEFT, fill=BOTH)
text.pack(side=LEFT, fill=BOTH)
scroll.pack(side=LEFT, fill=Y)
mimimiButton.pack(side=LEFT, fill=BOTH, expand=True)
rightSpace.pack(side=RIGHT, fill=BOTH)
text2.pack(side=RIGHT, fill=BOTH)
scroll2.pack(side=RIGHT, fill=Y)

#Loop
WINDOW.mainloop()