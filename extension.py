import binascii
def actualextension(path):

	filename=path.split("\\")[-1]
	print("filename: "+filename)
	
	def magicb(path2):
		with open(path2, 'rb') as f:
			#first_four=f.read(4)
			#print("The first four bytes are: "+ str(first_four))
			#print(first_four)
			data = f.read(4)
			hex_mb = binascii.hexlify(data).decode('utf-8')
			print(f"Hexadecimal: {hex_mb}")
			return(str(hex_mb))



	if "." in filename:
		print("The extension provided is "+filename.split(".")[-1])
		return(magicb(path))
	else:
		return(magicb(path))
