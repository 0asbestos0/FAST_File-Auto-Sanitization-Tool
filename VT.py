import hashlib
import vt
import time
import maintool

def GetHash(filename):
	sha256_hash = hashlib.sha256()
	with open(filename, 'rb') as file:
		for chunk in iter(lambda: file.read(4096), b''):
			sha256_hash.update(chunk)

	sha256_hex = sha256_hash.hexdigest()
	return sha256_hex





def scan(filename,args):
	
	def rescan(filename,args):
		with open(filename, 'rb') as f:
			analysis = client.scan_file(f)
		
		while True:
			analysis = client.get_object("/analyses/{}", analysis.id)
			print(analysis.status)
			if analysis.status == "completed":
				break
			time.sleep(30)
		
		results=[]
		for val in analysis.results.values():
			results.append(val['result'])
		
		positives=0
		for result in results:
			if result!=None:
				positives=positives+1

		flagged=str(positives)+'/'+str(len(results))
		print(flagged+' engines flagged it as MALICIOUS')
		maintool.log('warning',args,'User didnot opt for file rescan with Virus Total')
		
		client.close()

	api_key = input('Enter your API key: ')
	
	maintool.log('info',args,'User selected the Virus Total Flag')
	maintool.log('info',args,'User Provided API key: '+api_key)

	
	#Add try catch in case the API key was wrong

	client = vt.Client(api_key)
	sha256hash= GetHash(filename)
	
	print('SHA-256 hash of file: '+str(sha256hash))
	maintool.log('info',args,'SHA256 hash of file: '+sha256hash)

	file_report = client.get_object("/files/{}".format(sha256hash))
	print('Last analyzed VT Report: ')
	print(file_report.last_analysis_stats)

	maintool.log('info',args,'File was last analyzed on '+file_report.last_analysis_date+' and the report is: ' +file_report.last_analysis_stats)
	
	if file_report is None:
		
		print("File not found in VirusTotal.")
		maintool.log('info',args,'File was not found in Virus Total')

		if args.manual:
			c=input('Would you like to scan the file in VirusTotal again? *T&C apply. 1/0: ')
			if c!='1':
			
				maintool.log('info',args,'User did not opt for file rescan with Virus Total')
				return
			
			maintool.log('info',args,'User opted for file rescan with Virus Total')
			rescan(filename,args)		
		return
	else:
		print(file_report)
		maintool.log('info',args,'Virus Total File report: ')
		#print("File Name: {}".format(file_report.attributes['names'][0]))
#		print("File Type: {}".format(file_report.attributes['type_description']))
#		print("File Size: {} bytes".format(file_report.attributes['size']))
#		print("First Seen: {}".format(file_report.attributes['first_submission_date']))
#		print("Last Seen: {}".format(file_report.attributes['last_analysis_date']))
#		print("Number of Positive Scans: {}".format(file_report.attributes['last_analysis_stats']['malicious']))
#		print("Number of Total Scans: {}".format(file_report.attributes['last_analysis_stats']['total']))

		if args.manual:
			c=input('Would you like to scan the file in VirusTotal again? *T&C apply. 1/0: ')
			if c!='1':
				return
			rescan(filename,args)


	