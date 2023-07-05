import os
import subprocess
import re
import maintool

def pdfanalyze(path,args):
	command= 'yara64 -w ' + os.environ.get('current_directory') +'\\rulescp\\maldocs\\Maldoc_PDF.yar '+ '\"' + path + '\"' #change rulescp to rules
	#print(command)
	print("Running yara rules: \n")
	maintool.log('info',args,'Running Yara Rules')
	output= subprocess.check_output(command, shell=True)
	
	if output!=None:
		output=output.decode().split('\r\n')
		maintool.log('warning',args,'Yara Results: ')
		for o in output:
			maintool.log('warning',args, o)
			print(o)
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


class pdfobjectdatatype:
	def __init__(self, objreference, content):
		self.objreference=objreference
		self.content=content

	def __repr__(self):		#used to print the string form of objects
		#return f"Object Reference Number: {self.objreference}, Content: {self.content}"
		return f"Object Reference Number: {self.objreference}"


def parsepdfobjs(path,args):
	pattern = rb'\d+\s\d+\sobj.*?endobj' #RegEx pattern for finding objects
	print("Parsing PDF-Objects: ")

	with open(path,'rb') as f:
		pdfbytesdata=f.read()

	pdfobjectsraw=re.findall(pattern, pdfbytesdata, re.DOTALL) # array that  stores the individial indirecto bjects in byted form
	if args.manual:
		choice=input("Would you like to print each PDF object to the terminal? 1/0: ")
	
		if choice=='1':
			maintool.log('info',args,'User Opted to print out each object to terminal')
			for pdfobject in pdfobjectsraw:
				print(pdfobject.replace(b'\r\n',b''))
		
	pdfobjects=[] #list that will return all the objects in the pdf
	for pdfobject in pdfobjectsraw: #iterating to create new objects corresponding to each indirect pdf object
		attr=getattributes(pdfobject)
		obj=pdfobjectdatatype(attr[0],attr[1])
		pdfobjects.append(obj)

	#choice=input("Would you like to print each object to the terminal? 1/0: ")
	#for pdfobject  in pdfobjects:
	#		print(pdfobject)
	#		print('/////////////////////////////////////////////////')
	return(pdfobjects)





def getattributes(pdfobject): #function to get the attributes in a cleaner way
	attr=[]
	filtered=pdfobject.split(b'\r\n ') #pdfobject is in bytes form
	#print("Number: "+filtered[0].decode()[0])
	attr.append(filtered[0].decode()[0])
	#content=bstr[bstr.find(b'<'):bstr.rfind(b'>')].replace(b'\r\n',b'')
	#print("Content: "+content.decode())
	attr.append(pdfobject[pdfobject.find(b'<'):pdfobject.rfind(b'>')].replace(b'\r\n',b'')) #Maybe incorrect, check once
	return(attr)


def susobjects(pdfobjects):
	keywords=[b'EmbeddedFiles',b'Filespec',b'Filter',b'EmbeddedFile']
	suspdfobjects=[]
	for pdfobject in pdfobjects:
		for keyword in keywords:
			if keyword in pdfobject.content:
				suspdfobjects.append(pdfobject.objreference)
				break

	return(suspdfobjects)

def extract(path,objreference):
	command='pdf-parser -f -o '+str(objreference)+' -d \"'+ path[:-4] +'(extracted obj '+str(objreference)+').bin\" '+path
	#print('Command: '+command)
	output = subprocess.check_output(command, shell=True)
	print(output)


def extract2(path, pdfobjects, objreference, args):
	if args.manual:						#If manual mode is enabled, extract the object in a binary file
		dfilename=path[:-4]+'(ExtractedObj_'+str(objreference)+').bin'

		obj=pdfobjects[objreference-1].split(b'\x0D\x0A')

		if b'/Filter' in obj:
			
			tmp=obj[obj.index(b'/Filter')+8:]			# 7 to accomodate 7 characters of /Filter and one space

			objfilter=tmp[:index(b'\x0D\x0A')]
			print(objfilter)

		#swith open(dfilename,'wb') as f:



def disable(path):
	command='pdfid -d \"'+path+'\"'
	print('Command: '+command)
	output = subprocess.check_output(command, shell=True)