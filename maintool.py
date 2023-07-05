import welcome
import extension
import pdfanalysis
import docanalysis
import doc_self_mine
import VT
import tmp
import img

import argparse
import logging
import binascii
import os
import subprocess
import sys

def log(flag,args,message):
	if args.report:
		if flag == 'debug':	
			logging.debug(message)
		if flag == 'info':
			logging.info(message)
		if flag == 'warning':
			logging.warning(message)
		if flag == 'error':
			logging.error(message)
		if flag == 'critical':
			logging.critical(message)
	
def main(filename,args):
	
	os.environ['current_directory']=os.path.dirname(os.path.abspath( __file__ ))
	path_to_file=filename

	if args.report:
		logging.basicConfig(filename= os.environ.get('current_directory')+'\\Reports\\'+path_to_file.split("\\")[-1]+'REPORT.log', level=logging.INFO,format='%(asctime)s [+] %(levelname)s - %(message)s')

	#log('info',args,'Arguments provided for scan: '+args)

	print("Path: "+path_to_file)
	log('info',args,'File to be scanned: '+path_to_file)

	mb=extension.actualextension(path_to_file)
	
	print("mb: "+str(mb))
	log('info',args,'Magic Bytes of file: '+str(mb))

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
		print("Actual filetype inferred from Magic Bytes: "+actualfiletype)
	
	else:
		print("Cannot process this filetype yet")
		log('info',args,'Cannot process this filetype yet')
		exit()

	
	if args.vt:
		VT.scan(path_to_file,args)

	if actualfiletype == "PDF":
		pdfanalysis.pdfanalyze(path_to_file,args)						#Only runs YARA rules
		#pdfanalysis.parsepdfobjs(path_to_file)
		pdfobjects = pdfanalysis.parsepdfobjs(path_to_file,args)
		
		suspdfobjects=pdfanalysis.susobjects(pdfobjects)
		if args.manual:
			print('The following PDF objects number are suspicious. Check each object individually and extract if needed')
			print(suspdfobjects)
			log('warning',args,'Follwing PDF objects are suspecious: ' +  ' '.join(suspdfobjects))

			while True:
				choice=input('Enter which object number to extract (0 to exit): ')
				if choice=='0':
					break
				maintool.log('info',args,'User extracted object number: '+str(choices))
				pdfanalysis.extract(path_to_file,int(choice))
		else:
			for suspdfobject in suspdfobjects:
				#pdfanalysis.extract(path_to_file,int(suspdfobject))
				pdfanalysis.extract2(path_to_file, pdfobjects, int(suspdfobject), args)

	
		print('Disabling JS and Auto Launch if any and outputting cleaned file: ')
		log('info',args,'Disabling JS and Auto Launch if any and outputting cleaned file: ')
		pdfanalysis.disable(path_to_file)
		#add a method for extracting the embedded file
		#add method to find any hyperlinks in pdf
		#add method to find macros in pdf
	
	elif(actualfiletype == 'DOC'):
		tmp.docyara(path_to_file,args)			#Only runs YARA rules
		tmp.func(path_to_file,args)				#For manual (Self) parsing
		print("Checking if file contains Macros, extracting if found and disarming the file:")
		log('info',args,'Checking if file contains Macros, extracting if found and disarming the file')
		tmp.disarm(path_to_file,args)			#Prints Decompressed Macros and disarms the file

	elif(actualfiletype == 'JPEG' or actualfiletype == 'PNG'):
		img.imganalyze(path_to_file,args,actualfiletype)





def printguide():
	helpstr='''THIS IS THE HELP PAGE IN MAKING\nThis tool analyzes Various file tyeps of maliciousness.\nSupported filetypes:\n\n\t.doc \t.xls \t.ppt\n \t.docx	.docm 	.xlsx 	.pptx\n\t.pdf\n\nFLAGS:\n\t-d\t\t--directory\t\tPath to directory where all files to be analyzed is kept (Not compatible with manual mode)\n\t-f\t\t--filename\t\t"Absolute" path of one specific file\n\t--help\t\t\t\t\tPrint the default help\n\t--manual\t\t\t\tMANUAL mode (For Experts)\n\t--guide\t\t\t\t\tPrint this guide'''
	print(helpstr)

def dirmode(args):
	#fnames=[]
	fnames = subprocess.check_output('ls '+str(args.directory), shell=True).decode().strip('\r\n').split('\r\n')
	for i in range(len(fnames)):
		fnames[i]=args.directory+'\\'+fnames[i]

	print(fnames)
	

	for fname in fnames:
		main(fname,args)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Checks and sanitizes various file types automatically")
	parser.add_argument("-d", "--directory", type=str, help="Path to a directory which contains all files to analyze. Not compatible with manual mode")
	parser.add_argument("-f", "--filename", type=str, help="File name of a specific file to be analyzed")
	parser.add_argument("-m", "--manual", action="store_true", help="Manual mode (Promts user, Use only if you have knowledge about file formats)")
	parser.add_argument("-vt", "-virustotal", action="store_true", help="If there is internet, it also uses VirusTotal. *T&C Apply. Not compatible with directory flag")
	parser.add_argument("--guide", action="store_true", help="Explains how to use the tool")
	parser.add_argument("-r", "--report", action="store_true", help="Generte a report")
	args = parser.parse_args()

	if args.guide:
		printguide()
		sys.exit()
	
	#Introduce some checks because not all flags are compatible with other
	print(args)
	if (args.directory!=None and args.filename!=None):
		print('Inavlid set of arguments, Only one of Directory or filename must be specified')
		sys.exit()
	if (args.directory!=None and args.vt==True):
		print('Inavlid set of arguments, Directory flag is not compatible with VirusTotal as of now')
		sys.exit()
	if (args.directory==None and args.filename==None):
		print('Inavlid set of arguments, Provide either a directory or a filename')
		sys.exit()
	if (args.directory!=None and args.manual==True):
		print('Inavlid set of arguments, Manual mode cannot be run if directory is specified')
		sys.exit()

	welcome.welcome()

	if args.filename!=None:
		main(args.filename,args)
		sys.exit()
	
	elif args.directory!=None:
		#print('doing something')
		args.directory=args.directory.strip('\\').strip('/')
		dirmode(args)

