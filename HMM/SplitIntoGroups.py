# IMPORT
import sys

# MAIN
# Reads a fully filtered HMMScan file (*.Occurrence) [1]
# and breaks it down into groups via Domain membership

input_lines = open(sys.argv[1],"r").readlines()

domain_dict = {}
for ln in input_lines:
    split_ln = [l for l in ln.strip().split(" ") if l]
    domain = split_ln[0]
    gene = split_ln[3]

    if domain in domain_dict.keys():
        tmp = domain_dict[domain]
        tmp.append(gene)
        domain_dict[domain] = tmp
    else:
        domain_dict[domain] = [gene]


for key in domain_dict.keys():
    outfile = key + ".domain.group"
    
    genes = [n + "\n" for n in list(set(domain_dict[key]))]
    if len(genes) > 1:
        output = open(outfile,"w")
        output.write("".join(genes))
        output.close()
