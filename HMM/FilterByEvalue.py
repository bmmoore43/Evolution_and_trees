# IMPORT
import sys

# MAIN
# Reads the processed *.TFSequences [1] and filters the 
# results by a e-value threshold [2] 

input_lines = open(sys.argv[1],"r").readlines()
e_value = float(sys.argv[2])

outlines = []
for ln in input_lines:
    split_ln = [l for l in ln.strip().split(" ") if l]
    if float(split_ln[6]) < e_value:
        outlines.append(ln)

output = open(sys.argv[1] + ".Evalue_"+str(e_value),"w")  
output.write("".join(outlines))
output.close()
