# IMPORT
import sys

# MAIN
# Reads a ".fasta" file [1] in a dictionary then 
# reads the list of ".domain.group" files [2]
# and generates a ".fasta" file for each group

fasta_lines = open(sys.argv[1],"r").readlines()

fasta_dict = {}
name = "na"
sequence = "na"
for ln in fasta_lines:
    if ln.startswith(">"):
        fasta_dict[name] = sequence
        name = ln.strip(">").strip("\n").split(" ")[0] # Shorten names to first word if multiple words are present
        sequence = ""
    else:
        sequence = sequence + ln.strip("\n")


inp= open(sys.argv[2],"r")

for l in inp:
    output_lines = []
    genes = l.strip().split("\t")
    orthogr= genes[0]
    for g in genes[1:]:
        print (g)
        g= g.split(" ")[0]
        print (g)
        if g in fasta_dict.keys():
            output_lines.append(">" + g + "\n")
            output_lines.append(fasta_dict[g] + "\n")

    output_file = str(orthogr) + ".fasta"
    output = open(output_file,"w")
    output.write("".join(output_lines))
    output.close()

