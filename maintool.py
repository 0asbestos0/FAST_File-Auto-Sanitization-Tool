import welcome
import extension
import pdfanalysis
import docanalysis
import doc_self_mine
import tmp
import argparse

import binascii
import os
import sys

def main(filename,args):
	
	os.environ['current_directory']=os.getcwd()
	
	welcome.welcome()
	path_to_file=args.filename
	
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
		tmp.docyara(path_to_file,args)			#Only runs YARA rules
		tmp.func(path_to_file)
		print("Checking if file contains Macros, extracting if found and disarming the file:")
		tmp.disarm(path_to_file)
	







def printhelp(): #Not working yet
	helpstr='''THIS IS THE HELP PAGE IN MAKING
		FLAGS:
		-d 			--directory 		Path to directory where all files to be analyzed is kept
		-f 			--filename 			Absolute path of one specific file
		--help 							Print this help
		--manual						MANUAL mode (For Experts)
		

		'''
	print(helpstr)
	return 0

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Checks and sanitizes various file types automatically")
	parser.add_argument("-d", "--directory", type=str, help="Path to a directory which contains all files to analyze")
	parser.add_argument("-f", "--filename", type=str, help="File name of a specific file to be analyzed")
	parser.add_argument("--manual", action="store_true", help="Manual mode (Promts user, Use only if you have knowledge about file formats)")
	args = parser.parse_args()
	
	#Introduce some checks because not all flags are compatible with other
	if (args.directory!=None and args.filename!=None):
		print('Inavlid set of arguments, Only one of Directory or filename must be specified')
		sys.exit()
	if (args.directory=None and args.filename=None):
		print('Inavlid set of arguments, Provide either a directory or a filename')
		sys.exit()
	
	print(args.directory)
	print(args.filename)
	print(args.manual)

	if args.filename!=None:
		main(args.filename,args)
		sys.exit()
	
	elif args.directory!=None:
		print('doing something')

