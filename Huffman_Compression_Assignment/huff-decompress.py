import pickle, sys, os
import array, time

#Check that user has provided the compressed file as input
if len(sys.argv) != 2:
	print("Usage: %s <infile.bin>" %sys.argv[0])
	sys.exit(0)

#Check that file passes exists
if not os.path.exists(sys.argv[1]): 
	print("[X] Input binary file does not exist")
	sys.exit(0)

#Check if symbol model exists
if not os.path.exists(os.path.splitext(sys.argv[1])[0]+"-symbol-model.pkl"):
	print("[X] Symbol model pickle file does not exist")
	sys.exit(0)

##Start decoding
start_time = time.time()
#Transform symbol model to dictionary
symbol_model = pickle.load(open(os.path.splitext(sys.argv[1])[0]+"-symbol-model.pkl", "rb"))
print("[\o/] Done loading symbol model\n[!] Extracting compressed data")

## Convert binary data to binary string
binary_array = array.array("B")
binary_array.frombytes(open(sys.argv[1], "rb").read())

#Use format to convert binary data to binary bytes with 0 padding if needed
string_data = ""
for binary_data in binary_array:
	string_data += format(binary_data, "08b")

file_data = ""
EOF = "۝"


print("[\o/] Done extracting compressed data\n[!] Decompressing...")
i = 0
end = False
#Loop until start_index is equal to or greater than the entire length of string data
while i < len(string_data):
	k = i
	#Loop until we find end index of binary string that exists in dictionary
	while True:
		#Check if binary string of start to end index exists in dictionary
		if string_data[i:k] in symbol_model:
			#Check if Huffman encoding is the Pseudo-EOF
			if symbol_model[string_data[i:k]] == EOF:
				end = True
				break
			#Append new decoded data to bugffer
			file_data += symbol_model[string_data[i:k]] + ""
			break
		k += 1
	if end: break
	i=k


print("[!] Time taking to decompress file: %.3fs" %(time.time() - start_time))
#Save data to decompressed file.
with open(os.path.splitext(sys.argv[1])[0]+"-decompressed.txt", "w") as decompress_file:
	decompress_file.write(file_data)
print("[\o/] Done decompressing and saved to file")