# IMPORT
import sys

# MAIN
# Reads a list of PFAM Domains [1] and parses
# HMMScan output [2] using this list

PFAM_Domain = open(sys.argv[1],"r").readlines()

PFAM_Domain_list = [l.strip() for l in PFAM_Domain]

HMMScan_lines = [l for l in open(sys.argv[2],"r").readlines() if not l.startswith("#")]

print HMMScan_lines[0].split(" ")
outlines = []
for ln in HMMScan_lines:
    split_ln = [l for l in ln.strip().split(" ")]
    if split_ln[0] in PFAM_Domain_list:
        outlines.append(ln)

output = open(sys.argv[2] + ".Domains","w")
output.write("".join(outlines))
output.close()
