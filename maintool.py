import welcome
import extension
import pdfanalysis
import docanalysis
import doc_self_mine
import tmp

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
    "d0cf11e0":"DOC",
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
	#pdfanalysis.parsepdfobjs(path_to_file)
	pdfobjects = pdfanalysis.parsepdfobjs(path_to_file)
	
	suspdfobjects=pdfanalysis.susobjects(pdfobjects)
	print('The following PDF objects number are suspicious. Check each object individually and extract if needed')
	print(suspdfobjects)
	while True:
		choice=input('Enter which object number to extract (0 to exit): ')
		if choice=='0':
			break
		pdfanalysis.extract(path_to_file,int(choice))

	print('Disabling Active components if any and outputting cleaned file: ')
	pdfanalysis.disable(path_to_file)
	#add a method for extracting the embedded file
	#add method to find any hyperlinks in pdf
	#add method to find macros in pdf

elif(actualfiletype == 'DOC'):
	docanalysis.docanalyze(path_to_file)
	#docselfanalysis.selfanalyze(path_to_file)
	#doc_self_mine.func2(path_to_file)
	tmp.func(path_to_file)