def deleteObj(objs, filename):												#objs must be a list
	with open(filename,'rb') as f:
		o2data=f.read()

	odata=o2data

	for obj in objs:
		if obj ==1:
			continue
		index_c_obj=find_nth_occurrence(odata,b'obj',2*obj-1)-4
		ndata=b''
		ndata=ndata+odata[:index_c_obj] 			#+10 to account for 6 digits of 'endobj' and 4 digits of '0D 0A 0D 0A'seperator
		#print(ndata)
		#Now we add 0s to the object we want to delete
		index_next_obj=find_nth_occurrence(odata,b'obj',2*obj+1)-4
	
		size = index_next_obj - index_c_obj
	
		ndata=ndata+b'\x00'*size
	
		ndata=ndata+ odata[index_next_obj:]
		odata=ndata
	
	print(ndata)

	nfilename=filename[:-4]+'Deleted_Obj_'+str(obj)+filename[-4:]
	with open(nfilename,'wb') as f:
		f.write(ndata)


def find_nth_occurrence(byte_string, target_substring, n):
	count = 0
	index = -1
	while count < n:
		try:
			index = byte_string.index(target_substring, index + 1)
			count += 1
		except ValueError:
			break
	return index

def flatedecode():
	with open('C:\\Users\\husky\\Downloads\\malpdf.pdf','rb') as f:
		data=f.read()
	
	compressed_data=data[992:9944]
	decompressed=zlib.decompress(compressed_data)
	
	with open('C:\\Users\\husky\\Downloads\\dumpprogram.bin','wb') as f:
		f.write(decompressed)
	
	print('Done')

#filename=input('Enter filename')
#deleteObj([9],filename)