import os
import subprocess


def docanalyze(path):
	#command= 'yara64 -w ' + os.environ.get('current_directory') +'\\rulescp\\maldocs\\Maldoc_PDF.yar '+path #change rulescp to rules
	#print(command)
	print("Running yara rules: \n")
	command = 'ls '+ os.environ.get('current_directory') +'\\rulescp\\maldocs'
	rules = subprocess.check_output(command, shell=True).decode().split('\r\n')
	
	while ('' in rules): # just some filtering
		rules.remove('')

	
	for rule in rules:
		command='yara64 -w ' + os.environ.get('current_directory') +'\\rulescp\\maldocs\\'+rule+' '+path #change rulescp to rules
		if (os.system(command)!=0):
			print(os.system(command))

	# get the index where it contains the malicious script
	
	
