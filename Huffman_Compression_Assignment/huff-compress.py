import sys, os, argparse, time
import re, pickle, array

symbol_model = {}
dictionary_model = {}

#Huffman code tree node
class HuffmanNode:
    def __init__(self, probability, symbol=None):
        self.symbol = symbol 
        self.left_tree = None
        self.right_tree = None
        self.probability = probability
        self.binaryCode = None

#Tree traversal - Using Depth-first search algorithm
def assignBinaryCode(node, code=""):

    #Check if node has left node/subtree
    if node.left_tree != None:
        if node.left_tree.binaryCode == None:
            assignBinaryCode(node.left_tree, code+"0")
        else:
            node.left_tree.binaryCode = "0"

    #Append to symbol and dictionary model if end node contains symbol - valid for assigning binary coding
    if node.left_tree == None and node.symbol != None:
        symbol_model[code] = node.symbol
        dictionary_model[node.symbol] = code

    #Check if node has right node/subtree
    if node.right_tree != None:
        if node.right_tree.binaryCode == None:
            assignBinaryCode(node.right_tree, code+"1")
        else:
            node.right_tree.binaryCode = "1"

    #Append to symbol and dictionary model if end node contains symbol - valid for assigning binary coding
    if node.right_tree == None and node.symbol != None:
        symbol_model[code] = node.symbol
        dictionary_model[node.symbol] = code

    return node

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("infile", help="infile to compress")
parser.add_argument("-s", "--symbolmodel", help="specify character- or word-based Huffman encoding -- default is character",
                    choices=["char","word"])
args = parser.parse_args()

#Check that user has assigned symbol model else crash
if not args.symbolmodel:
    print("** ERROR: You must include the symbol model type ***")
    sys.exit(0)

#Check that file exists
if not os.path.exists(args.infile):
    print("[:O] File: %s does not exist" %args.infile, file=sys.stderr)
    sys.exit()

#Assign regex based on symbol type [char/word]
if args.symbolmodel == "char":
    tokenRE = re.compile("[\w\W]")
elif args.symbolmodel == "word":
    tokenRE = re.compile("[\w]+|[\W]")

start_time = time.time()
#Compute frequency of tokens/symbols
zero_model = {}
EOF = "۝"
file_data = []
with open(args.infile, "r", encoding="utf=8") as infile:
    for line in infile:
        tokens = tokenRE.findall(line)
        for token in tokens:
            zero_model[token] = zero_model.get(token, 0) + 1
            file_data.append(token)

#Include Pseudo-EOF
zero_model[EOF] = 1

#Compute probability of every symbol
text_len = sum(zero_model.values())
zero_model = {key:(value/text_len) for key, value in zero_model.items()}

print("[\o/] Done creating zero model\n[!] Creating Huffman Code Tree")

## Build huffman code tree
#Create list of nodes
leaf_nodes = [HuffmanNode(value, key) for key, value in zero_model.items()]
leaf_nodes = sorted(leaf_nodes, key=lambda x: x.probability, reverse=True)

#Build Huffman code tree - without binary assignment 
while len(leaf_nodes) > 1:
    left = leaf_nodes.pop()
    right = leaf_nodes.pop()

    new_node = HuffmanNode(probability=(left.probability + right.probability))
    new_node.left_tree = left
    new_node.right_tree = right

    #For now, let's just resort
    leaf_nodes.append(new_node)
    leaf_nodes = sorted(leaf_nodes, key=lambda x: x.probability, reverse=True)

#Traverse tree - use final node left after creating tree (root node of huffman tree)
tree = leaf_nodes[0]
tree = assignBinaryCode(tree)

print("[\o/] Done creating symbol model\n[!] Compressing input file")
print("[!] Time taken to build tree: %.3fs" %(time.time() - start_time))

#Save symbol model as pickle
pickle.dump(symbol_model, open(os.path.splitext(args.infile)[0]+"-symbol-model.pkl", "wb"))

start_time = time.time()
## Compress infile with symbol model
#Create array to hold values of C-type unsigned integers
binary_array = array.array("B")


symbol_data = ""
for fd in file_data:
    symbol_data += dictionary_model[fd]

if len(symbol_data) % 8 != 0:
    symbol_data += dictionary_model[EOF]
    symbol_data += "0"*(8 - (len(binary_array) % 8))

for i in range(0, len(symbol_data), 8):
    binary_array.append(int(symbol_data[i:i+8], 2))

print("[!] Time taken to encode input file: %.3fs" %(time.time() - start_time))
binary_array.tofile(open(os.path.splitext(args.infile)[0]+".bin", "wb"))

print("[\o/] Done compressing file")