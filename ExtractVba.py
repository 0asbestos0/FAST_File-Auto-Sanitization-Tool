
#
#
#
#
#
#
#
#

#CompressedContainer=b'\x01\x16\x01\x00'					#Array of bytes holding compressed data
#DecompressedBuffer=b''#

#if CompressedContainer[0]!=1:
#	print('ERROR')
#	#print(CompressedContainer[0])
#Chunks=[]
#for i in range(1,len(CompressedContainer)):
#	header=CompressedContainer[i:i+2]#

#	CompressedChunkSize=ExtractCompressedChunkSize#

#	Chunks.append(CompressedContainer[i:i+CompressedChunkSize])
#	i=i+CompressedChunkSize#?????????????????????????????#

#for Chunk in Chunks:
#	DecompressChunk(Chunk)#

#def ExtractCompressedChunkSize(header):
#	bits = ''.join(format(byte, '08b') for byte in header)
#	return(int(bits[:12],2)+3)				#First 12 bits represent the number of bytes minus 3#

#def ExtractCompressedChunkFlag(header):
#	bits = ''.join(format(byte, '08b') for byte in header)
#	return(int(bits[-1]))#

#def DecompressChunk(Chunk):
#	header=Chunk[0:2]
#	CompressedSize=ExtractCompressedChunkSize(header)
#	CompressedFlag=ExtractCompressedChunkFlag(header)
#	if CompressedFlag ==1:
#		DecompressingArrayOfTokenSequence(chunk)
#	else:
#		DecompressingARawChunk(Chunk)#

#def DecompressingARawChunk(Chunk):
#	CompressedChunkData=Chunk[2:4098] #?????????????????USe len(Chunk)??
#	DecompressedBuffer=DecompressedBuffer+CompressedChunkData#

#def DecompresssingArrayOfTokenSequence(Chunk):
#	CompressedChunkData=[] # Array of Token Sequences
#	for j in range(2,len(Chunk)):
#		FlagByte=format(Chunk[j],'08b')
#		FlagByte=FlagByte[::-1]											#MSB denotes last token
#		nbytes=FlagByte.count('1')*2 + FlagByte.count('0')*1			#FlabByte 1 means CopyToken(2 Bytes) and 0 means LiteralToken(1 Byte)
#		CompressedChunkData.append(Chunk[j:j+nbytes+1])					# +1 to compensate for the header#
#

#	for TokenSequence in CompressedChunkData:
#		DecompressingATokenSequence(TokenSequence)#

#def DecompressingATokenSequence(TokenSequence):
#	Tokens=[]
#	FlagByte=format(TokenSequence[0],'08b')
#	FlagByte=[::-1]														# Reversing FlagByte
#	fb=0
#	for i in range(1,len(TokenSequence)):
#		if FlagByte[fb]==0:
#			Tokens.append(TokenSequence[i])		
#			i=i+1
#		else:
#			Tokens.append(TokenSequence[i:i+2])
#			i=i+2
#	for index in range(len(Tokens)):
#		DecompressingAToken(Tokens[index],index,FlagByte)#

#def DecompressingAToken(Token,index,FlabByte):
#	if FlagByte[index]==0:												#Literal token
#		DecompressedBuffer=DecompressedBuffer+Token
#	else:																#Copy Token
#		Offset, Length = UnpackCopyToken(Token)
#		CopySource= len(DecompressedBuffer)-Offset
#		ByteCopy(CopySource,Length)#
#

#def UnpackCopyToken(Token):
#	LengthMask, OffsetMask, BitCount=CopyTokenHelp(Token)
#	Length= Token & LengthMask
#	temp1 = Token & OffsetMask
#	temp2 = 16 - BitCount
#	Offset = (temp1 >> temp2) +1
#	return(Offset,Length)#
#

#def CopyTokenHelp(Token): #
#

#def ByteCopy(CopySource,ByteCount):
#	bytecpy=DecompressedBuffer[CopySource:CopySource+ByteCount]
#	DecompressedBuffer=DecompressedBuffer+bytecpy#
#

#	
#	
import math
import maintool
def P23Ord(value):
    if type(value) == int:
        return value
    else:
        return ord(value)
def ParseTokenSequence(data):
    flags = P23Ord(data[0])
    data = data[1:]
    result = []
    for mask in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]:
        if len(data) > 0:
            if flags & mask:
                result.append(data[0:2])
                data = data[2:]
            else:
                result.append(data[0])
                data = data[1:]
    return result, data
def OffsetBits(data):
    numberOfBits = int(math.ceil(math.log(len(data), 2)))
    if numberOfBits < 4:
        numberOfBits = 4
    elif numberOfBits > 12:
        numberOfBits = 12
    return numberOfBits

def DecompressChunk(compressedChunk):
    if len(compressedChunk) < 2:
        return None, None
    header = P23Ord(compressedChunk[0]) + P23Ord(compressedChunk[1]) * 0x100
    size = (header & 0x0FFF) + 3
    flagCompressed = header & 0x8000
    data = compressedChunk[2:2 + size - 2]

    if flagCompressed == 0:
        return data.decode(errors='ignore'), compressedChunk[size:]

    decompressedChunk = ''
    while len(data) != 0:
        tokens, data = ParseTokenSequence(data)
        for token in tokens:
            if type(token) == int:
                decompressedChunk += chr(token)
            elif len(token) == 1:
                decompressedChunk += token
            else:
                if decompressedChunk == '':
                    return None, None
                numberOfOffsetBits = OffsetBits(decompressedChunk)
                copyToken = P23Ord(token[0]) + P23Ord(token[1]) * 0x100
                offset = 1 + (copyToken >> (16 - numberOfOffsetBits))
                length = 3 + (((copyToken << numberOfOffsetBits) & 0xFFFF) >> numberOfOffsetBits)
                copy = decompressedChunk[-offset:]
                copy = copy[0:length]
                lengthCopy = len(copy)
                while length > lengthCopy: #a#
                    if length - lengthCopy >= lengthCopy:
                        copy += copy[0:lengthCopy]
                        length -= lengthCopy
                    else:
                        copy += copy[0:length - lengthCopy]
                        length -= length - lengthCopy
                decompressedChunk += copy
    return decompressedChunk, compressedChunk[size:]


def find_pattern_offsets(data, pattern):
    offsets = []
    pattern_length = len(pattern)
    data_length = len(data)

    for i in range(data_length - pattern_length + 1):
        if data[i:i+pattern_length] == pattern:
            offsets.append(i)

    return offsets


def find_and_decompress(filename,data,args):
    pattern=b'\x00Attribut\x00e '
    offsets= find_pattern_offsets(data, pattern)
    print('offsets:')
    print(offsets)    
    
    if len(offsets)>0:
        if args.manual:
            c=input("Macros found, should i print all the decompressed Macros? 1/0")

            if c=='1':
                if args.report:
                    maintool.log('info',args,'User opted to print Macros on the terminal')
                print('/////////////////////////////////////////////////////')
                print('/////////////////////////////////////////////////////')
                for offset in offsets:
                    DecompressedChunk=DecompressChunk(data[offset-2:])
                    print(DecompressedChunk[0])
                    print('/////////////////////////////////////////////////////')
                    print('/////////////////////////////////////////////////////')

        return(0)
    else:
        return(1)