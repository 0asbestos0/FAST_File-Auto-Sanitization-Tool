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
import struct

# Function to read sectors from the file
def read_sectors(file, offset, sector_size):
    file.seek(offset)
    return file.read(sector_size)

# Function to parse the directory entry
def parse_directory_entry(entry_data):
    dir_name = entry_data[:64].decode('utf-16',errors='replace').rstrip('\x00')
    dir_type = struct.unpack('<H', entry_data[66:68])[0]
    return dir_name, dir_type

# Function to recursively traverse the directory tree
def traverse_directory(file, dir_offset, sector_size):
    print("inside traverse_directory")
    sectors = read_sectors(file, dir_offset, sector_size)
    entry_size = 128

    for i in range(0, len(sectors), entry_size):
        entry_data = sectors[i:i + entry_size]
        dir_name, dir_type = parse_directory_entry(entry_data)
        print(dir_name)
        print(dir_type)

        '''if dir_type == 2:
            # Storage (directory)
            print(f"Directory: {dir_name}")
            sub_dir_offset = struct.unpack('<I', entry_data[116:120])[0]
            traverse_directory(file, sub_dir_offset * sector_size, sector_size)
        elif dir_type == 1:
            # Stream
            print(f"Stream: {dir_name}")
        elif dir_type == 0:
            # Empty entry
            print("Continuing")
            continue
		'''
# Main function
def extract_directory_structure(doc_file_path):
    with open(doc_file_path, 'rb') as file:
        # Read sector size from the header at offset 30
        file.seek(30)
        sector_shift = struct.unpack('<H', file.read(2))[0]
        sector_size = 2 ** sector_shift
        print("sector_size: "+str(sector_size))
        # Read root directory offset from the header at offset 48
        file.seek(48)
        root_dir_offset = struct.unpack('<I', file.read(4))[0] * sector_size
        print('root_dir_offset: '+str(root_dir_offset))

        # Traverse the directory tree
        traverse_directory(file, root_dir_offset, sector_size)

# Example usage
doc_file_path = "C:\\Users\\husky\\Downloads\\dump.doc"
extract_directory_structure(doc_file_path)
