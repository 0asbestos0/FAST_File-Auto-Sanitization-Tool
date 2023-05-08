import os
import subprocess
import re

def pdfanalyze(path):
	command= 'yara64 -w ' + os.environ.get('current_directory') +'\\rulescp\\maldocs\\Maldoc_PDF.yar '+path #change rulescp to rules
	#print(command)
	print("Running yara rules: \n")
	print(os.system(command))
	print("\n")

	command='pdfid '+ path
	output = subprocess.check_output(command, shell=True)
	output=output.decode('utf-8').replace(' ','').split("\r\n")
	
	for element in output:
		if '/Encrypt' in element:
			if element[-1] !=0:
				print("This PDF contains "+element[-1]+" instances of encryption.")
			else:
				print("This PDF is not encrypted with a password")

		elif '/JavaScript' in element:
			if element[-1] !=0:
				print("This PDF contains "+element[-1]+" instances of Java script.")
			else:
				print("This PDF does not contain Javascript")
		elif '/EmbeddedFile' in element:
			if element[-1] !=0:
				print("This PDF has "+element[-1]+" embedded files.")
			else:
				print("This PDF does not contain embedded files")
		elif '/OpenAction' in element:
			if element[-1] !=0:
				print("This PDF contains "+element[-1]+" instances of the OpenAction function.")
			else:
				print("This PDF does not contain the OpenAction function")


#class pdfobjectdatatype:
#	def __init__:(self)


def parsepdfobjs(path):
	pattern = rb'\d+\s\d+\sobj.*?endobj' #RegEx pattern for finding objects
	print("Parsing PDF-Objects: ")

	with open(path,'rb') as f:
		pdfbytesdata=f.read()

	pdfobjects=re.findall(pattern, pdfbytesdata, re.DOTALL)

	for pdfobject  in pdfobjects:
		for i in pdfobject.split(b'\r\n '):
			print(i.replace(b'\r\n',b''))
		print('/////////////////////////////////////////////////')
		#print(type(pdfobject))
		#break
	
	