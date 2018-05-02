# IMPORT
import sys

# MAIN
# Reads a list of *.fasta files [1] and 
# writes a mafft command for it

fasta_files = open(sys.argv[1],"r").readlines()

outlines = []
for file in fasta_files:
    outlines.append("mafft " + file.strip() + " > " + file.strip() + ".mafft_align\n")
    
output = open("MafftCommands.cc","w")
output.write("".join(outlines))
output.close()
