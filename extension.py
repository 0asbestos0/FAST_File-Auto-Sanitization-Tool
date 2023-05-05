def extension(path):

	filename=path.split("\\")[-1]
	print("filename: "+filename)
	
	def magicb(path):
		with open(path, 'rb') as f:
			first_four=f.read(4)
			print("The first four bytes are: "+ str(first_four))


	if "." in filename:
		print("The extension provided is "+filename.split(".")[-1])
		magicb(path)
	else:
		magicb(path)
