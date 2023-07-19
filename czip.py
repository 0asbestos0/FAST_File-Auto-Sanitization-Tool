import zipfile
import os
import re

def analyze(path,args):
	
	#step1 check if docx file
	with zipfile.ZipFile(path) as zf:
		file_list = zf.namelist()

	req_file_list=['[Content_Types].xml', 'docProps/', 'docProps/app.xml', 'docProps/core.xml', '_rels/', '_rels/.rels', 'word/', 'word/styles.xml', 'word/document.xml']

	if not all(file in file_list for file in req_file_list):
		print('Not a docx file.\n Cannot process this file')
		#return
	
	print('Looks like it is a docx file. ')
	extracted_directory=docx(path, args)
	analyzedocx(path,extracted_directory,args)


def docx(path,args):
	d_name = os.path.dirname(path)
	f_name = os.path.basename(path)
	new_directory = os.path.join(d_name, "extracted_" + os.path.splitext(f_name)[0])

	with zipfile.ZipFile(path, 'r') as zip_ref:
		zip_ref.extractall(new_directory)

	print('Extracted the docx file.')
	return(new_directory)

def analyzedocx(path,extracted_directory,args):
	ips=[]
	urls=[]
	unknown_urls=[]
	allowed_urls=['http://www.w3.org/', 'http://schemas.microsoft.com/', 'http://schemas.openxmlformats.org/', 'http://purl.org/']

	def content_analyze(file_path):
		ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
		url_pattern = re.compile(r"https?://\S+")

		with open(file_path,'r', encoding='utf-8') as f:
			data= f.read()
		
		ip_addresses = ip_pattern.findall(data)
		url=url_pattern.findall(data)

		if ip_addresses:
			for ip_address in ip_addresses:
				ips.append((ip_address,file_path))
		if url:
			for u in url:
				urls.append((u,file_path))

		

	for root, _, files in os.walk(extracted_directory):
		for file in files:
			file_path = os.path.join(root, file)
			content_analyze(file_path)

	

	print('IP addresses found: ')
	for ip in ips:
		print(ip[0])
	print('URLs found: ')
	for url in urls:
		print(url[0])

	counter=0
	for url in urls:
		for allowed_url in allowed_urls:
			if allowed_url in url[0]:
				counter+=1
		
		if counter==0:
			unknown_urls.append(url)
		counter=0
	print('Unknown URLs found: ')
	for unknown_url in unknown_urls:
		print(unknown_url)


	for unknown_url in unknown_urls:
		sanitizeurl(unknown_url)

	print('Unknown URLs replaced with 127.0.0.1')
	print('Rezipping the whole file: ')
	rezip(extracted_directory ,path)

	#Some cleaning Up to do.

def rezip(extracted_directory,archive_name):
	print('Extracted Directory:')
	print(extracted_directory)

	print('Archive name:')
	print(archive_name)

	with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
		for root, _, files in os.walk(extracted_directory):
			for file in files:
				file_path = os.path.join(root, file)
				arcname = os.path.relpath(file_path, extracted_directory)

				print('arcname:')
				print(arcname)

				zipf.write(file_path, arcname)

def sanitizeurl(unknown_url):
	with open(unknown_url[1],'r')as f:
		data=f.read()

	data=data.replace(unknown_url[0],'http://127.0.0.1/')

	with open(unknown_url[1],'w')as f:
		f.write(data)

