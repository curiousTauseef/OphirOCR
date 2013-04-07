from wax import *

#!/usr/bin/env python
#-*-coding:utf8-*-
import os, sys, tempfile, shutil, pipes, sys
langs = ("fra", "eng", "deu", "ita", "vie")
		
WORDPROCESSOR="libreoffice --writer"
OCROPUS="ocroscript recognize"
CONVERT="convert"

class MainFrame(Frame):
    def Body(self):
        self.AddComponent(Button(self, "Choose file...", self.ChooseFile), align='center',border=1)
        self.AddComponent(Label(self, "Text language:"), expand='h', border=1)
        self.AddComponent(ListBox(self, choices=langs), expand='h', border=2)
        self.AddComponent(Button(self, "Go !"), expand='both',border=1)
        self.Pack()

    def ChooseFile(self, event):
		    dlg = FileDialog(self, open=1)
		    try:
		        result = dlg.ShowModal()
		        if result == 'ok':
		            self.filename = dlg.GetPaths()[0]
		    finally:
		        dlg.Destroy()

	def doOCR ():
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


app = Application(MainFrame, title="OphirOCR", direction="vertical")
app.MainLoop()
