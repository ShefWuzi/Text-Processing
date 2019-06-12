"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
OPTIONS:
    -h : print this help message
    -b : use BINARY weights (default: count weighting)
    -s FILE : use stoplist file FILE
    -I PATT : identify input files using pattern PATT, 
              (otherwise uses files listed on command line)
------------------------------------------------------------
"""

import sys, re, getopt, glob

opts, args = getopt.getopt(sys.argv[1:],'hs:bI:')
opts = dict(opts)
filenames = args

##############################
# HELP option

if '-h' in opts:
    help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
    print(help,file=sys.stderr)
    sys.exit()

##############################
# Identify input files, when "-I" option used

if '-I' in opts:
    filenames = glob.glob(opts['-I'])

print('INPUT-FILES:', ' '.join(filenames))

##############################
# STOPLIST option

stops = set()
if '-s' in opts:
    with open(opts['-s'],'r') as stop_fs:
        for line in stop_fs :
            stops.add(line.strip())

##############################
# Tokenisation and Counting
def count_words(f):
    file_dict = {}
    with open(f, "r") as fh:
        for line in fh:
            tokens = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", line.lower())
            for t in tokens:
                if t in stops: continue
                if t in file_dict:
                    file_dict[t] = file_dict[t] + 1
                else:
                    file_dict[t] = 1
    return file_dict        

tokenisation_counting = []

#Loop through files
for f in filenames:
    tokenisation_counting.append({"filename":f, "words":count_words(f)})


#########################
#Comparison
def comparison(file_data1, file_data2):

    #file_data1 intersection file_data2
    fd1_fd2 = set(file_data1.keys()).intersection(file_data2.keys())

    #Eliminate possible duplicates

    return (len(fd1_fd2)/(len(file_data1) + len(file_data2) - len(fd1_fd2)))

def count_sensitive_comparison(file_data1, file_data2):

    fd1_fd2 = set(file_data1.keys()).union(file_data2.keys())
    min_w, max_w = 0, 0

    for w in fd1_fd2:
        if w not in file_data1:
            file_data1[w] = 0
        if w not in file_data2:
            file_data2[w] = 0
        min_w += min(file_data1[w], file_data2[w])
        max_w += max(file_data1[w], file_data2[w])
   
    return min_w/max_w

for z in range(0, len(tokenisation_counting)):
    for p in range(z+1, len(tokenisation_counting)):

        zf = tokenisation_counting[z]
        pf = tokenisation_counting[p]

        print("%s <> %s = %f" %(zf["filename"], pf["filename"], count_sensitive_comparison(zf["words"], pf["words"])))
