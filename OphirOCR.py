#!/usr/bin/env python
#-*-coding:utf8-*-
import Tkinter, tkFileDialog, tkMessageBox, os, sys, tempfile, shutil, pipes, sys

WORDPROCESSOR="libreoffice --writer"
OCROPUS="ocroscript recognize"
CONVERT="convert"

try:
	file = sys.argv[1]
except:
	file=None

def chooseFile ():
	global file
	file = tkFileDialog.askopenfilename(title='Choose a file',filetypes=[("Images",(".png",".jpeg",".jpg",".tif","tiff",".pct"))])

def doOCR ():
	global file, langs, langsBox, etat
	language=langs[int(langsBox.curselection()[0])]
	if not file:
		tkMessageBox.showwarning("Missing file", "You must provide an image file...")
		return
	os.environ["tesslanguage"]=language

	print ("Crating temporary files")
	tempDIR = tempfile.mkdtemp(prefix="OphirOCR-")
	tempPNG = tempfile.mkstemp(prefix="OphirOCR-", suffix=".png", dir=tempDIR)[1] #Fichier PNG temporaire
	tempHTML = tempfile.mkstemp(prefix="OphirOCR-", suffix=".html", dir=tempDIR)[1] #Fichier qui contiendra le texte numérisé

	print ("Converting image to PNG")
	os.system(CONVERT+" "+pipes.quote(file)+" "+pipes.quote(tempPNG))
	
	print ("Removing temporary files")
	shutil.rmtree(tempDIR)

	print ("Launching OCR program")
	os.system("%s --tesslanguage=%s '%s' > '%s'"%(OCROPUS, language, tempPNG, tempHTML))

	print ("Launching word processor")
	os.system(WORDPROCESSOR+" "+tempHTML)

	print ("Quitting...")
	sys.exit()

root = Tkinter.Tk()
root.title("OphirOCR")
#root.wm_iconbitmap(default="icon.png")

Tkinter.Label(text="Image :").pack(fill=Tkinter.X)
button = Tkinter.Button()
button["text"]="Choose Image"
button["command"]=chooseFile
button.pack()

Tkinter.Label(text="Text language :").pack(fill=Tkinter.X)
langs = ("fra", "eng", "deu", "ita")
langsBox=Tkinter.Listbox(height=len(langs))
for lang in langs:
	langsBox.insert(Tkinter.END, lang)
langsBox.selection_set(0)
langsBox.pack(fill=Tkinter.BOTH, expand=True)

go=Tkinter.Button(root, text="Go!", command=doOCR)
go.pack(fill=Tkinter.BOTH)

root.mainloop()
