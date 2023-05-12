import struct



#def selfanalyze(path):
def main():


# Open the .doc file as a binary file
	with open('C:\\Users\\husky\\Downloads\\dump.doc', 'rb') as f:
	    data = f.read()
	
#	 Read the file signature from the header
	file_signature = data[:8]
	expected_signature = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'
	
	if file_signature != expected_signature:
	    print('Invalid .doc file format')
	    exit()
	
#	 Get the location of the first block
	first_block_offset = struct.unpack_from('<I', data, 0x30)[0]
	
#	 Get the block offsets from the FAT section
	fat_start_offset = first_block_offset * 0x200
	fat_data = data[fat_start_offset:fat_start_offset + 4096]
	
	block_offsets = []
	for i in range(0, len(fat_data), 4):
	    block_offset = struct.unpack_from('<I', fat_data, i)[0] * 0x200
	    if block_offset != 0:
	        block_offsets.append(block_offset)
	
#	 Get the start offset of the directory section
	directory_entry_offset = struct.unpack_from('<I', data, 0x4C)[0] * 0x200
	directory_entry_size = struct.unpack_from('<I', data, 0x50)[0]
	
	directory_data = data[directory_entry_offset:directory_entry_offset + directory_entry_size]
	
	entries = []
	for i in range(0, len(directory_data), 128):
		entry_name_bytes = directory_data[i:i+32]
		try:
			entry_name = entry_name_bytes.decode('utf-16-le').rstrip('\x00')
		except UnicodeDecodeError:
			entry_name = entry_name_bytes.decode('utf-16-le', errors='replace').rstrip('\x00')
		entry_type = struct.unpack_from('<H', directory_data, i + 66)[0]
		entry_location = struct.unpack_from('<I', directory_data, i + 116)[0]
		entry_size = struct.unpack_from('<I', directory_data, i + 120)[0]
		entries.append((entry_name, entry_type, entry_location, entry_size))
	
#	 Get the main document stream entry
	doc_stream_entry = next((entry for entry in entries if entry[1] == 1), None)
	
	if doc_stream_entry is not None:
	    doc_stream_start = doc_stream_entry[2] * 0x200
	    doc_stream_size = doc_stream_entry[3]
	    
	    doc_stream_data = data[doc_stream_start:doc_stream_start + doc_stream_size]
	    print(doc_stream_data)  # Process the document stream as needed
	else:
	    print("No main document stream entry found in the directory.")
	

def func2():
	import struct

	# Open the .doc file as a binary file
	with open('C:\\Users\\husky\\Downloads\\dump.doc', 'rb') as f:
	    data = f.read()

	# Read the file signature from the header
	file_signature = data[:8]
	expected_signature = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'

	if file_signature != expected_signature:
	    print('Invalid .doc file format')
	    exit()

# Get the start offset of the directory section
	directory_entry_offset = struct.unpack_from('<I', data, 0x4C)[0] * 0x200 #0x200 is 512 in decimal which is typical length of sectors, '<' means little endian, 'I' means unsigned integer
	directory_entry_size = struct.unpack_from('<I', data, 0x50)[0]
	print("Directory entry offset: "+str(directory_entry_offset))
	print("Directory entry size: "+str(directory_entry_size))

	directory_data = data[directory_entry_offset:directory_entry_offset + directory_entry_size]

	print("Directory data:"+ str(directory_data.decode(errors='replace')))

	entries = []
	for i in range(0, len(directory_data), 128): #128 is the size of directory
		entry_name_bytes = directory_data[i:i+64]
		try:
			entry_name = entry_name_bytes.decode('utf-16-le').rstrip('\x00')
		except UnicodeDecodeError:
			entry_name = entry_name_bytes.decode('utf-16-le', errors='replace').rstrip('\x00')
		entry_type = struct.unpack_from('<H', directory_data, i + 66)[0]
		entry_location = struct.unpack_from('<I', directory_data, i + 116)[0]
		entry_size = struct.unpack_from('<I', directory_data, i + 120)[0]
		entries.append((entry_name, entry_type, entry_location, entry_size))

	# Print the directory structure
	for entry in entries:
		choice = input("Print next entry?: 1/0 ")
		if choice!='1':
			print("continueing")
			break

		entry_name, entry_type, entry_location, entry_size = entry
		print(f"Name: {entry_name}")
		print(f"Type: {entry_type}")
		print(f"Location: {entry_location}")
		print(f"Size: {entry_size}")
		print()

	for entry in entries:
		entry_name, entry_type, entry_location, entry_size = entry
		if entry_type==1:
			print(f"Entry Name: {entry_name}, is a directory")


if __name__ == '__main__':
	#main()
	func2()

