import os, sys
command_file = open(sys.argv[1], 'r')
output = open("command_files_fasttree.sh", 'w')

align_list = []
for line in command_file:
    L= line.strip().split(" ")
    align_file = L[16]
    print (align_file)
    align_list.append(align_file)
    output.write("module load fasttree; FastTree %s > %s_treefile\n" % (align_file, align_file))
    
print (align_list)
output.close()