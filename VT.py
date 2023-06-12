import hashlib
import vt
import time


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

		print(str(positives)+'/'+str(len(results))+' engines flagged it as MALICIOUS')
		client.close()

	api_key = input('Enter your API key: ')
	client = vt.Client(api_key)
	sha256hash= GetHash(filename)
	print('SHA-256 hash of file: '+str(sha256hash))

	file_report = client.get_object("/files/{}".format(sha256hash))
	print('Last analyzed VT Report: ')
	print(file_report.last_analysis_stats)
	
	if file_report is None:
		print("File not found in VirusTotal.")
		if args.manual:
			c=input('Would you like to scan the file in VirusTotal again? *T&C apply. 1/0: ')
			if c!='1':
				return
			rescan(filename,args)		
		return
	else:
		print(file_report)
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


	