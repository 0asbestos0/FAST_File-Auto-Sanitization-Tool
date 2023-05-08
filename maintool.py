import welcome
import extension
import pdfanalysis

import binascii
import os


os.environ['current_directory']=os.getcwd()

welcome.welcome()
path_to_file=input("Enter the absolute path to the file: ")
print("Path: "+path_to_file)
mb=extension.actualextension(path_to_file)


print("mb: "+str(mb))
magic_bytes = {
    "25504446": "PDF",
    "ffd8ffe0": "JPEG",
    "89504e47": "PNG",
    "75737461": "TAR",
    "47494638": "GIF",
    "49492a00": "TIFF",
    "4d4d002a": "TIFF",
    "504b0304": "ZIP",
    "52617221": "RAR",
    "1f8b0800": "GZ"
}

if mb in magic_bytes.keys():
	actualfiletype=magic_bytes[mb]
	print("actual filetype: "+actualfiletype)
elif str(mb)[0:4] == '4d5a':
	print("actual filetype: EXE")

else:
	print("Cannot process this filetype yet")


if actualfiletype == "PDF":
	pdfanalysis.pdfanalyze(path_to_file)
	pdfanalysis.parsepdfobjs(path_to_file)
	#pdfobjects = pdfanalysis.parsepdfobjs(path_to_file)

	#pdfanalysis.analyzepdfobjs(pdfobjects)



