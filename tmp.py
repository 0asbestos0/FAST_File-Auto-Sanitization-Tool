'''bstr=b'1 0 obj\r\n<<\r\n /Type /Catalog\r\n /Outlines 2 0 R\r\n /Pages 3 0 R\r\n /Names << /EmbeddedFiles << /Names [(eicar-dropper.doc) 7 0 R] >> >>\r\n /OpenAction 9 0 R\r\n>>\r\nendobj'
#string=bstr.decode()
filtered=bstr.split(b'\r\n ')
for i in filtered:
	print(i.replace(b'\r\n',b''))


print("Number: "+filtered[0].decode()[0])
content=bstr[bstr.find(b'<'):bstr.rfind(b'>')].replace(b'\r\n',b'')
print("Content: "+str(content.decode('ascii')))'''


'''import struct

# Assuming 'directory_data' contains the directory data of the .doc file

def extract_directory_structure(data):
    directory_entry_offset = struct.unpack_from('<I', data, 0x4C)[0] * 0x200
    directory_data = data[directory_entry_offset:]

    entries = []
    i = 0

    while i < len(directory_data):
        entry_name_length = struct.unpack_from('<H', directory_data, i + 64)[0]
        entry_name_bytes = directory_data[i + 66:i + 66 + entry_name_length]
        entry_name = entry_name_bytes.decode('utf-16le', errors='replace')

        if i + 66 + entry_name_length + 2 >= len(directory_data):
            break

        entry_type = struct.unpack_from('<H', directory_data, i + 66 + entry_name_length)[0]

        # Append the directory entry details to the entries list
        entries.append((entry_name, entry_type))

        # Move to the next directory entry
        i += 66 + entry_name_length + 2

    return entries

# Usage example:
with open('C:\\Users\\husky\\Downloads\\dump.doc', 'rb') as file:
    doc_data = file.read()
    directory_structure = extract_directory_structure(doc_data)

for entry in directory_structure:
    entry_name, entry_type = entry
    print(f"Entry Name: {entry_name}, Entry Type: {entry_type}")
'''
'''import struct

# Assuming 'directory_data' contains the directory data of the .doc file

def extract_directory_structure(data):
    directory_entry_offset = struct.unpack_from('<I', data, 0x4C)[0] * 0x200
    directory_data = data[directory_entry_offset:]

    entries = []
    i = 0

    while i < len(directory_data):
        entry_name_length = struct.unpack_from('<H', directory_data, i + 64)[0]
        entry_name_bytes = directory_data[i + 66:i + 66 + entry_name_length]
        entry_name = entry_name_bytes.decode('utf-16le', errors='replace')

        if i + 66 + entry_name_length + 2 >= len(directory_data):
            break

        entry_type = struct.unpack_from('<H', directory_data, i + 66 + entry_name_length)[0]

        is_directory = entry_type == 0x0001

        # Append the directory entry details to the entries list, including the is_directory flag
        entries.append((entry_name, entry_type, is_directory))

        # Move to the next directory entry
        i += 66 + entry_name_length + 2

    return entries

# Usage example:
with open('C:\\Users\\husky\\Downloads\\dump.doc', 'rb') as file:
    doc_data = file.read()
    directory_structure = extract_directory_structure(doc_data)

for entry in directory_structure:
    entry_name, entry_type, is_directory = entry
    entry_type_str = "Directory" if is_directory else "File"
    print(f"Entry Name: {entry_name}, Entry Type: {entry_type_str}")'''


'''def extract_word_document(filename):
# Open the .doc file in binary mode
    with open(filename, 'rb') as file:
    # Read the entire file content
        content = file.read()

    # Find the start and end positions of the WordDocument stream
    start_marker = b'\x31\xBE'
    end_marker = b'\xA0\x46'

    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)

    if start_pos == -1 or end_pos == -1:
        print("WordDocument stream not found in the file.")
        return

    # Extract the WordDocument stream
    word_document = content[start_pos + 2:end_pos]

    # Write the extracted stream to a new file
    with open('WordDocument_stream.doc', 'wb') as output_file:
        output_file.write(word_document)

    print("WordDocument stream extracted successfully.")

# Usage example
extract_word_document('C:\\Users\\husky\\Downloads\\dump.doc')'''

'''def extract_word_document(filename):
    # Open the .doc file in binary mode
    with open(filename, 'rb') as file:
        # Read the entire file content
        content = file.read()

        # Find the start position of the WordDocument stream
        start_marker = b'\x57\x6F\x72\x64\x2E\x44\x6F\x63\x75\x6D\x65\x6E\x74'
        start_pos = content.find(start_marker)

        if start_pos == -1:
            print("WordDocument stream not found in the file. "+filename)
            return

        # Calculate the end position based on the start position
        end_pos = len(content)

        # Extract the WordDocument stream
        word_document = content[start_pos:end_pos]

        # Write the extracted stream to a new file
        with open('WordDocument_stream.doc', 'wb') as output_file:
            output_file.write(word_document)

        print("WordDocument stream extracted successfully.")

# Usage example
extract_word_document('C:\\Users\\husky\\Downloads\\dump.doc')'''

'''def extract_root_entry(filename):
    # Open the .doc file in binary mode
    with open(filename, 'rb') as file:
        # Read the entire file content
        content = file.read()

        # Find the start position of the root entry
        root_entry_start_marker = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'
        root_entry_start_pos = content.find(root_entry_start_marker)

        if root_entry_start_pos == -1:
            print("Root entry not found in the file.")
            return

        # Calculate the end position based on the start position
        root_entry_end_pos = root_entry_start_pos + 512

        # Extract the root entry
        root_entry = content[root_entry_start_pos:root_entry_end_pos]

        # Write the extracted root entry to a new file
        with open('root_entry.bin', 'wb') as output_file:
            output_file.write(root_entry)

        print("Root entry extracted successfully.")

# Usage example
extract_root_entry('C:\\Users\\husky\\Downloads\\dump.doc')'''

'''\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Open the .doc file in binary mode
with open('C:\\Users\\husky\\Downloads\\dump.doc', 'rb') as file:
    # Read the header (first 512 bytes)
    header = file.read(512)
    
    # Get the sector size from the header (offset 30-31)
    sector_size =2**(int.from_bytes(header[30:32], byteorder='little'))
    print("Sector Size: "+str(sector_size))
    # Calculate the file offset of the first sector
    first_sector_offset = 512
    
    # Define a helper function to calculate the file offset from a SecID
    def sec_pos(sec_id):
        return first_sector_offset + sec_id * sector_size
    
    # Extract the number of sectors used by the SAT from the header (offset 44-47)
    sat_sector_count = int.from_bytes(header[44:48], byteorder='little')
    print("SAT sector count: "+str(sat_sector_count))
    
    # Read the MSAT (first 109 SecIDs in the header)
    msat_sec_ids = []
    for i in range(0, 109, 4):
        sec_id = int.from_bytes(header[i:i+4], byteorder='little', signed=True)
        if sec_id != -2 and sec_id>=-4:
            msat_sec_ids.append(sec_id)
    
    print("msat_sec_ids1: "+str(msat_sec_ids))
    # Read the remaining MSAT SecIDs from the sectors
    msat_sec_id_offset = 76  # Offset to the first MSAT SecID in the header
    while msat_sec_ids[-1] != -2:
        print("inside while")
        # Calculate the file offset of the next MSAT sector
        next_msat_sec_offset = sec_pos(msat_sec_ids[-1])
        
        # Seek to the next MSAT sector and read its SecIDs
        file.seek(next_msat_sec_offset)
        msat_sec_ids.extend(
            [int.from_bytes(file.read(4), byteorder='little', signed=True) for _ in range(sector_size // 4)]
        )
    print("msat_sec_ids2: "+str(msat_sec_ids))
    # Build the SAT by reading sectors listed in the MSAT
    sat_sec_ids = []
    for msat_sec_id in msat_sec_ids:
        msat_sec_offset = sec_pos(msat_sec_id)
        file.seek(msat_sec_offset)
        sat_sec_ids.extend(
            [int.from_bytes(file.read(4), byteorder='little', signed=True) for _ in range(sector_size // 4)]
        )
    print("sat_sec_ids: "+str(sat_sec_ids))
    # Extract the directory structure from the SAT
    directory_sec_id = sat_sec_ids[0]  # Assuming the first SecID is for the directory
    directory_sec_offset = sec_pos(directory_sec_id)
    file.seek(directory_sec_offset)
    
    # Read the directory structure (you'll need to parse it based on the .doc file format)
    directory_data = file.read(sector_size)
    # Parse the directory structure and extract the relevant information
    
    # Display the extracted directory structure
    print(directory_data)
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\''''
'''import struct

def read_sectors(file, offset, sector_size):
    file.seek(offset)
    return file.read(sector_size)

def read_directory_sectors(file, sector_ids, sector_size):
    sectors = []
    for sector_id in sector_ids:
        sector_offset = 512 + sector_id * sector_size
        sector_data = read_sectors(file, sector_offset, sector_size)
        sectors.append(sector_data)
    return sectors

def traverse_sat(file, sat_sector_ids, sector_size):
    sat_sectors = read_directory_sectors(file, sat_sector_ids, sector_size)
    sector_chain = []
    for sat_sector in sat_sectors:
        for i in range(0, len(sat_sector), 4):
            sector_id = struct.unpack('<i', sat_sector[i:i+4])[0]
            sector_chain.append(sector_id)
    return sector_chain

def traverse_directory_chain(file, directory_sector_ids, sector_size):
    directory_sectors = read_directory_sectors(file, directory_sector_ids, sector_size)
    directory_data = b''.join(directory_sectors)
    return directory_data

def extract_directory_structure(doc_file_path):
    with open(doc_file_path, 'rb') as file:
        header = file.read(512)
        sector_size = 2 ** struct.unpack('<H', header[30:32])[0]

        msat_sector_ids = struct.unpack('<109i', header[76:512])
        sat_sector_chain = traverse_sat(file, msat_sector_ids, sector_size)

        directory_sector_chain = []
        for sat_sector_id in sat_sector_chain:
            if sat_sector_id == -2:
                break
            directory_sector_chain.append(sat_sector_id)

        print("directory_sector_chain: ")
        print(directory_sector_chain)

        directory_data = traverse_directory_chain(file, directory_sector_chain, sector_size)

        # Process the directory data as needed
        # Here, you can parse the directory entries or perform other operations
        print(directory_data.decode('utf-16-le',errors='replace'))

# Example usage
doc_file_path = 'C:\\Users\\husky\\Downloads\\dump.doc'
extract_directory_structure(doc_file_path)
'''

'''dirs=[b'\x01\x02\x03',b'\x01\x02\x03',b'\x01\x02\x03',b'\x01\x02\x03']
dirs2=[]
for d in dirs:
	dirs2.append(d[0:1]+b'\x04'+d[2:3])
	#print(d[2:3])
print(dirs2)'''

import struct
from docx import Document
import win32com.client as win32
import ExtractVba
import os
import subprocess

def docyara(path,args):
	#command= 'yara64 -w ' + os.environ.get('current_directory') +'\\rulescp\\maldocs\\Maldoc_PDF.yar '+path #change rulescp to rules
	#print(command)
	print("Running yara rules: \n")
	command = 'ls '+ os.environ.get('current_directory') +'\\rulescp\\maldocs'
	rules = subprocess.check_output(command, shell=True).decode().split('\r\n')
	
	while ('' in rules): # just some filtering
		rules.remove('')

	
	for rule in rules:
		command='yara64 -w ' + os.environ.get('current_directory') +'\\rulescp\\maldocs\\'+rule+' '+path #change rulescp to rules
		if args.manual:
			if (os.system(command)!=0):
				print(os.system(command))

def func(filename):
	
	with open(filename,'rb') as f:
		data=f.read()

	datacp=data 																	#Used to output disarmed file
	header=data[:512]

	uSectorShift=2**(int.from_bytes(data[30:32],byteorder='little'))
	uMiniSectorShift=2**(int.from_bytes(header[32:34],byteorder='little'))
	csectFAT=int.from_bytes(header[44:48],byteorder='little')
	sectDirStart=int.from_bytes(header[48:52],byteorder='little')
	ulMiniSectorCutoff=int.from_bytes(data[56:60],byteorder='little')
	sectMiniFatStart=struct.unpack('<i',header[60:64])[0]
	csectMiniFat=struct.unpack('<i',header[64:68])[0]
	sectFat=[]																		#First 109 FAT sector numbers
	for i in range(76,len(header),4):
		secID=struct.unpack('<i',header[i:i+4])[0]
		if secID!=-1:
			sectFat.append(secID)
	
	#FatSectors=[]																	#Valid Fat Sectors
	#for i in sectFat:
	#	if i!=-1:
	#		FatSectors.append(i)
	print('FAT Sectors:')
	print(sectFat)

	FatChain=[]
	for sectornumber in sectFat:
		sectordata=data[512*(sectornumber+1):512*(sectornumber+2)]
		for j in range(0,len(sectordata),4):
			FatChain.append(struct.unpack('<i',sectordata[j:j+4])[0])
	print('FatChain: ')
	print(FatChain)

	DirChain=traverseFat(FatChain,sectDirStart)
	#print('Directory chain: ')
	#print(DirChain)
	miniFatSectors=traverseFat(FatChain,sectMiniFatStart)
	print('MiniFat Sectors:')
	print(miniFatSectors)

	directory=parsedirectory(DirChain,data)
	print('Directory: ')
	for d in directory:
		print(d)

	secMiniStreamStart=directory[0].SectStart
	print('Starting sector of MiniStream:')
	print(secMiniStreamStart)

	MiniStreamChain=traverseFat(FatChain,secMiniStreamStart)
	print('MiniStream Sector chain: ')
	print(MiniStreamChain)
	
	miniFatchain=traverseMiniFat(miniFatSectors,data)
	print('Mini Fat Chain: ')
	print(miniFatchain)
	#suspeciousnames=['Macros','VBA']
	#print('Disarming file if it contains Macros or VBA.')
#	for d in directory:
#		#print(d.UL)
#		if d.Name == 'Macros':
#			#data=disarm(data, 'Macros')
#			disarm(filename)
#		elif d.Name == 'VBA':
#			continue
			#data=disarm(data, 'VBA')

	#if (data!=datacp):
#		print('Outputting the disarmed file:')
#		outputfilename=filename[:-4] + '(clean).doc'
#		with open(outputfilename,'wb') as f:
#			f.write(data)

def traverseMiniFat(miniFatSectors,data):
	miniFatdata=b''
	for sector in miniFatSectors:
		miniFatdata=miniFatdata + data[512*(sector+1):512*(sector+2)]

	miniFatchain=[]
	for i in range(0,len(miniFatdata),4):
		miniFatchain.append(struct.unpack('<i',miniFatdata[i:i+4])[0])
	return miniFatchain

def disarm(filename):
	with open(filename,'rb') as f:
		data=f.read()
	vbaFlag=ExtractVba.find_and_decompress(filename,data)
	print(vbaFlag)
	if vbaFlag==0: #Means Macros are found
		print('Found Macros, disarming the file')
		command=os.environ.get('current_directory')+'\\VBASanitizer.exe '+filename+' '+filename[:-4]+'(RemovedMacros)'+filename[-4:]
		print(command)
		os.system(command)


class Directory:
	def __init__(self, Name, Type, SidLeftSib, SidRightSib, SidChild, SectStart, Ulsize):
		self.Name=Name
		self.Type=Type
		self.SidLeftSib=SidLeftSib
		self.SidRightSib=SidRightSib
		self.SidChild=SidChild
		self.SectStart=SectStart
		self.Ulsize=Ulsize
	def __repr__(self):
		return f"Name: {self.Name}, Type: {self.Type}, Size: {self.Ulsize}, SectStart: {self.SectStart}"

def parsedirectory(DirChain,data):
	dirobjects=[]

	for DirSectNumber in DirChain:
		DirSectData=data[512*(DirSectNumber+1):512*(DirSectNumber+2)]
		for i in range(0,len(DirSectData),128):
			cb=DirSectData[i+64]
			cb=int.from_bytes(DirSectData[i+64:i+66],byteorder='little')
			Name=DirSectData[i:i+cb-2].decode('utf-16-le',errors='ignore').strip() #cb-2 to account for trainling nulll bytes
			Type=DirSectData[i+66]
			SidLeftSib=struct.unpack('<i',DirSectData[i+68:i+72])[0]
			SidRightSib=struct.unpack('<i',DirSectData[i+72:i+76])[0]
			SidChild=struct.unpack('<i',DirSectData[i+76:i+80])[0]
			SectStart=struct.unpack('<i',DirSectData[i+116:i+120])[0]
			Ulsize=struct.unpack('<i',DirSectData[i+120:i+124])[0]

			dirobjects.append(Directory(Name,Type,SidLeftSib,SidRightSib,SidChild,SectStart,Ulsize))
	return(dirobjects)

def traverseFat(FatChain,startSecID):
	chain=[]
	while startSecID!=-2:
		chain.append(startSecID)
		startSecID=FatChain[startSecID]


	return(chain)


#filename=input('Enter filename: ')
#func(filename)
#func2(filename)