# IMPORT
import sys
import os

# MAIN
# Reads a list of RAxML "Best Tree" files [1],
# writes and runs the retree program from
# PHYLIP

# Requires the PHYLIP module be loaded on HPCC

tree_files = [l.strip() for l in open(sys.argv[1],"r").readlines()]

for f in tree_files:
    
    # Write command file
    control_file = f + ".retree_ctl"
    output_file = f+".rooted"
    output = open(control_file,"w")
    output.write("Y\n")
    output.write(f+"\n")
    output.write("M\n")
    output.write("X\n")
    output.write("Y\n")
    output.write("F\n")
    output.write(output_file+"\n")
    output.write("R\n")
    output.close()

    os.system("retree < " + control_file + "\n")

    source = [l.strip() for l in open(output_file,"r").readlines()]
    outline = "".join(source)+"\n"
    output = open(output_file + ".newick","w")
    output.write(outline)
    output.close()
