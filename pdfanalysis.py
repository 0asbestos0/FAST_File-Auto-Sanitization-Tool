import os

def pdfanalyze(path):
	command= 'yara64 -w ' + os.environ.get('current_directory') +'\\rulescp\\maldocs\\Maldoc_PDF.yar '+path #change rulescp to rules
	#print(command)
	print(os.system(command))
	