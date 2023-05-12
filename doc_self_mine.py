import struct

docfilename='C:\\Users\\husky\\Downloads\\dump.doc'
with open (docfilename,'rb') as file:
	data=file.read()

header=data[:512]
sector_size=2**(int.from_bytes(data[30:32],byteorder='little'))

secid_dir_sec = int.from_bytes(data[48:52],byteorder='little')
print('secid_dir_sec: '+str(secid_dir_sec))

sectors=[]
for i in range(512, len(data), sector_size):
	sectors.append(data[i:i+512])

print('Starting Directory sector: ')
print(sectors[38].decode('utf-16-le',errors='replace'))


#for sector in sectors:
	#print(len(sector))
	#print(sector[:4])
	#print(struct.unpack('<i', sector[:4])[0])
