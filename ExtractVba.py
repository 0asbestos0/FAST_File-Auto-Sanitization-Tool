from bitstring import BitArray











CompressedContainer=b'\x01\x16\x01\x00'					#Array of bytes holding compressed data
if CompressedContainer[0]!=1:
	print('ERROR')
	#print(CompressedContainer[0])
Chunks=[]
for i in range(1,len(CompressedContainer)):
	header=CompressedContainer[i:i+2]
	print(header)
	#CompressedChunkSize=BitArray(hex=header)
	bits = ''.join(format(byte, '08b') for byte in header)
	print(int(bits[:12],2))
	#CompressedChunkSize=2**(int(bits[:12]))
	#print(CompressedChunkSize)
	break
