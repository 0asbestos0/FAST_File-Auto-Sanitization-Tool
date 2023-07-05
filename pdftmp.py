import zlib

def flatedecode():
	with open('C:\\Users\\husky\\Downloads\\malpdf.pdf','rb') as f:
		data=f.read()
	
	compressed_data=data[992:9944]
	decompressed=zlib.decompress(compressed_data)
	
	with open('C:\\Users\\husky\\Downloads\\dumpprogram.bin','wb') as f:
		f.write(decompressed)
	
	print('Done')
	
def ascii