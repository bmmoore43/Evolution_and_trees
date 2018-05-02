# IMPORT
import sys

# MAIN
# Filters an *.Evalue_#### filtered file [1] (i.e.
# this should be the last filtering step) and removes
# domains which only appear once

input_lines = open(sys.argv[1],"r").readlines()
occurence_limit = sys.argv[2]

domain_list = [l.strip().split(" ")[0] for l in input_lines]

outlines = []
for ln in input_lines:
    domain = ln.strip().split(" ")[0]
    
    if domain_list.count(domain) > occurence_limit:
        outlines.append(ln)

output = open(sys.argv[1] + ".Occurrence","w")
output.write("".join(outlines))
output.close()
   
