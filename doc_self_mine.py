import struct
def func1():
	#docfilename='C:\\Users\\husky\\Desktop\\hi2.doc'
	docfilename='C:\\Users\\husky\\Downloads\\dump.doc'
	with open (docfilename,'rb') as file:
		data=file.read()	

	header=data[:512]
	sector_size=2**(int.from_bytes(data[30:32],byteorder='little'))
	nsectors=(len(data)/512)-1
	print("Number of Sectors: "+str(nsectors))	

	sec_ids_in_msat=[]
	msat=data[76:512]
	for i in range(0,len(msat),4):
		#print ("SecId: "+msat[i:i+4].decode('utf-16-le',errors='replace'))
		sec_ids_in_msat.append(struct.unpack('<i',msat[i:i+4])[0])
		#print ("SecId: "+str(sec_ids_in_msat[-1]))	

	choice=input("Dump MSAT? 1/0: ")
	if choice=='1':
		print(msat)	

	secid_dir_sec = int.from_bytes(data[48:52],byteorder='little')
	print('secid_dir_sec: '+str(secid_dir_sec))	

	sectors=[]
	for i in range(512, len(data), sector_size):
		sectors.append(data[i:i+512])	

	while True:
		choice=input("Which sector to print?: ")
		if choice == 'exit':
			break
		print(sectors[int(choice)].decode('utf-16-le',errors='replace'))	

	#for sec_id_in_msat in sec_ids_in_msat:
		#print('inside for')
	#	if sec_id_in_msat>0:
	#		print(sectors[sec_id_in_msat])	

	###########################
	# for my specific file directory entry is between 19968-20480,20480-20992,20992-21509
	print("////////////////////////////////////////////////")
	sat=data[19456:19968]	

	#for i in range(0,len(sat),4):
	#	print(struct.unpack('<i',sat[i:i+4])[0])	

	print("For my soecific file: ")
	directories=[data[19968:20480],data[20480:20992],data[20992:21509]]
	#directories=data[19968:]
	#for i in range(0,len(directories),128):
	#	dirname = directories[i:i+64]
	#	print(dirname.decode('utf-16-le',errors='replace'))
	for directory in directories:
		for i in range(0,len(directory),128):
			dir_name=directory[i:i+64].decode('utf-16-le',errors='replace')
			dir_type=directory[i+66]
			print("dir_name: "+str(dir_name))
			print("dir_type: "+str(dir_type))
			if dir_type==1 or dir_type==2:
				print('Left_DirID: '+str(struct.unpack('<i',directory[i+68:i+72])[0]))
				print('Rootnote_DirID: '+str(struct.unpack('<i',directory[i+76:i+80])[0]))
				print('Right_DirID: '+str(struct.unpack('<i',directory[i+72:i+76])[0]))
			print('/////////////////////////////////////////////////////////')

###########################
#print('Starting Directory sector: ')
#print(sectors[38].decode('utf-16-le',errors='replace'))


#for sector in sectors:
	#print(len(sector))
	#print(sector[:4])
	#print(struct.unpack('<i', sector[:4])[0])
def func2():
	docfilename='C:\\Users\\husky\\Downloads\\dump.doc'
	with open (docfilename,'rb') as file:
		data=file.read()	

	header=data[:512]
	sector_size=2**(int.from_bytes(data[30:32],byteorder='little'))
	nsectors=(len(data)/512)-1
	print("Total Number of Sectors: "+str(nsectors))
	csectfat=int.from_bytes(data[44:48],byteorder='little')
	print("Number of Sectors in FAT: "+str(csectfat))
	sectdirstart=int.from_bytes(data[48:52],byteorder='little')
	print("First sector in directoty chain: "+str(sectdirstart))

	sectfat=[]
	for i in range(76,len(header),4):
		sectfat.append(struct.unpack('<i',header[i:i+4])[0])
	print("FAT sectors: ")
	print(sectfat)

	sectors=[]
	for i in range(512,len(data),512):
		sectors.append(data[i:i+512])

	valid_fat_sectors=[]
	for i in sectfat:
		if i!= -1:
			valid_fat_sectors.append(i)

	fatsectors=[]
	for i in valid_fat_sectors:
		fatsectors.append(sectors[i])

	print("FAT sectors (Hex): ")
	print(fatsectors)

	fatsectors_decimal=[]
	for fatsector in fatsectors:
		for i in range(0,len(fatsector),4):
			fatsectors_decimal.append(struct.unpack('<i',fatsector[i:i+4])[0])

	print('FAT sectors (Dec): ')
	print(fatsectors_decimal)
	
	direntry=fatsectors_decimal[38]
	dirchain=[]
	dirchain.append(38)
	dirchain.append(direntry)
	while direntry!=-2:
		nextentry=fatsectors_decimal[direntry]
		dirchain.append(nextentry)
		direntry=nextentry

	print('Directory chain:')
	print(dirchain)

	directory=[]
	for sector in dirchain:
		if sector!=-2:
			directory.append(sectors[sector])


	print('Directory: ')
	print(directory)
	print('/////////////////////////////////////////////////////////')

	for dirsector in directory:
		for i in range(0,len(dirsector),128):
			dir_name=dirsector[i:i+64].decode('utf-16-le',errors='replace')
			dir_type=dirsector[i+66]
			print("dir_name: "+str(dir_name))
			print("dir_type: "+str(dir_type))
			if dir_type==1 or dir_type==2:
				print('Left_DirID: '+str(struct.unpack('<i',dirsector[i+68:i+72])[0]))
				print('Rootnote_DirID: '+str(struct.unpack('<i',dirsector[i+76:i+80])[0]))
				print('Right_DirID: '+str(struct.unpack('<i',dirsector[i+72:i+76])[0]))
			print('/////////////////////////////////////////////////////////')







func2()
