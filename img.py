from PIL import Image
import maintool
import os

def imganalyze(path,args,actualfiletype):

	#def imgyara():
	#	print('doing yara')
	fname,ext=os.path.splitext(path)
		
	output_file=fname.rstrip('.')+'(cleaned).'+ext
	if args.report:
		maintool.log('info',args,'Sanitizing the image file by removing irrelevant information')
		maintool.log('info',args,'New file saved in destination: '+output_file)

	print('Sanitizing the image file by removing irrelevant information')
	if args.manual:
		c  = input('Would you like to sanitize this image file, by removing all the information not relevant to displaying the image?1/0: ')
		if c !='1':
			return
	with Image.open(path) as image:
       
		image = image.convert('RGB') # To handle PNG images
		data = image.tobytes()
		extracted_image = Image.frombytes(image.mode, image.size, data)

		

		extracted_image.save(output_file, format=actualfiletype)
