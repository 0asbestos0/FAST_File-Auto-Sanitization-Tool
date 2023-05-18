import struct

def func2(docfilename):
	#docfilename='C:\\Users\\husky\\Downloads\\dump.doc'
	with open (docfilename,'rb') as file:
		data=file.read()	

	header=data[:512] #512 bytes of header
	sector_size=2**(int.from_bytes(header[30:32],byteorder='little'))	#size of each sector
	nsectors=(len(data)/512)-1 #total number of sectors
	
	print("Total Number of Sectors: "+str(nsectors))
	
	csectfat=int.from_bytes(header[44:48],byteorder='little') #number of sectors in FAT (allocated for FAT)
	print("Number of Sectors in FAT: "+str(csectfat))

	sectdirstart=int.from_bytes(header[48:52],byteorder='little') #First sector in directory chain
	print("First sector in directoty chain: "+str(sectdirstart))

	ulMiniSectorShift=2**(int.from_bytes(data[32:36],byteorder='little')) #size of mini streams
	print('Size of mini Sectors: '+str(ulMiniSectorShift))

	#sectMiniFatStart=int.from_bytes(header[60:64],byteorder='little')
	sectMiniFatStart=struct.unpack('<i',header[60:64])[0]
	print('First sector in mini-FAT chain: '+str(sectMiniFatStart))

	csectMiniFat=struct.unpack('<i',header[64:68])[0]
	print('Number of sectors in mini-FAT chain: '+str(csectMiniFat))

	ulMiniSectorCutoff=int.from_bytes(data[56:60],byteorder='little')
	print('Max size of ministreams: '+str(ulMiniSectorCutoff))

	sectfat=[]
	for i in range(76,len(header),4):
		sectfat.append(struct.unpack('<i',header[i:i+4])[0])
	#print("FAT sectors: ")
	#print(sectfat)

	sectors=[]
	for i in range(512,len(data),512):
		sectors.append(data[i:i+512])

	valid_fat_sectors=[] #this hold only the sector numbers
	for i in sectfat:
		if i!= -1:
			valid_fat_sectors.append(i)

	fatsectors=[] #this holds the actual bytes of the sectors
	for i in valid_fat_sectors:
		fatsectors.append(sectors[i])

	#print("FAT sectors (Hex): ")
	#print(fatsectors)

	fatsectors_decimal=[]
	for fatsector in fatsectors:
		for i in range(0,len(fatsector),4):
			fatsectors_decimal.append(struct.unpack('<i',fatsector[i:i+4])[0])

	#print('FAT sectors (Dec): ')
	#print(fatsectors_decimal)
	
	#direntry=fatsectors_decimal[38]
	dirchain=[]
	dirchain.append(sectdirstart)
	direntry=sectdirstart
	while direntry!=-2:
		nextentry=fatsectors_decimal[direntry]
		dirchain.append(nextentry)
		direntry=nextentry

	print('Directory chain:')
	print(dirchain)

	minifatchain=[]
	minifatchain.append(sectMiniFatStart)
	minifatentry=sectMiniFatStart
	while minifatentry!=-2:
		nextminifatentry=fatsectors_decimal[minifatentry]
		minifatchain.append(nextminifatentry)
		minifatentry=nextminifatentry
	print('Minifat Chain: ')
	print(minifatchain)

	DISABLEDIRECTORY=b'\x00'

	directory=[]
	for sector in dirchain:
		if sector!=-2:
			directory.append(sectors[sector])

	editeddirectory=[]
	
	minifat=[]
	for sector in minifatchain:
		if sector!=-2:
			for i in range(0,len(sectors[sector]),ulMiniSectorShift):
				minifat.append(sectors[sector][i:i+ulMiniSectorShift])
	
	choice=input("Do you want to see each Minifat entry?1/0: ")
	if choice=='1':	
		for i in minifat:
			print(i.decode('utf-16-le',errors='replace'))

	sectMiniStreamStart=struct.unpack('<i',directory[0][116:120])[0]
	print('Starting sector of MiniStream: '+str(sectMiniStreamStart))
	sizeMiniStream=struct.unpack('<i',directory[0][120:124])[0]
	print('Size of MiniStream: '+str(sizeMiniStream))


	choice=input("Do you want to see each directory entry?1/0: ") #check the fact that directories with directory type 0 should also be printed in case payload was present but not activated. 
	if choice=='1':
		print('Directory: ')
		#print(directory)
		print('/////////////////////////////////////////////////////////')
	
		for dirsector in directory:
			for i in range(0,len(dirsector),128): #128 bytes is the typical size of directory entries
				dir_name=dirsector[i:i+64].decode('utf-16-le',errors='replace')
				dir_type=dirsector[i+66]
				#add dir_id?
				if dir_type>0:
					print("dir_name: "+str(dir_name))
					print("dir_type: "+str(dir_type))
				if dir_type==1 or dir_type==2:
					print('Left_DirID: '+str(struct.unpack('<i',dirsector[i+68:i+72])[0]))
					print('Rootnote_DirID: '+str(struct.unpack('<i',dirsector[i+76:i+80])[0]))
					print('Right_DirID: '+str(struct.unpack('<i',dirsector[i+72:i+76])[0]))
				if dir_type==2:
					ulSize=struct.unpack('<i',dirsector[120:124])[0]
					print('Size of stream: '+str(ulSize))
					print('Starting sector of stream: '+str(struct.unpack('<i',dirsector[116:120])[0]))
					#if ulSize>ulMiniSectorCutoff:
						#print(This stream exists in )
				if str(dir_name)=='Macros' or str(dir_name)=='VBA':
					print('Disabling Macros ')
					editeddirectory.append(dirsector[:66]+DISABLEDIRECTORY+dirsector[67:])
					#disableMacros()
				else:
					editeddirectory.append(dirsector)

				print('/////////////////////////////////////////////////////////')
	

	if editeddirectory!=directory:
		print('Directory has been changed, disarmed file has been written: ')
		writefilename=docfilename.split('.doc')[0] + '(Disarmed)'+'.doc'
		#editeddata=data[]

#def disableMacros(data,offset)

#filename=input('Enter filename: ')
#func2(filename)
