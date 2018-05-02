# IMPORT
import sys
import random

# MAIN
# Reads a list of alignment files [1] and
# writes RAxML commands for each file

alignment_files = [l.strip() for l in open(sys.argv[1],"r").readlines()]

command_lines = []
for file in alignment_files:

        b_seed = random.randint(10000,99999)
        p_seed = random.randint(10000,99999)

        RAxML_command = "raxmlHPC-PTHREADS -T 7 -n " + file + ".RAxML -f a -x " + str(b_seed) + " -p " + str(p_seed) + " -N 100 -m PROTGAMMAJTT -# 100 -o Mpoly,Ppaten -s " + file + "\n"

        command_lines.append(RAxML_command)

output = open("RAxMLCommands-Select.cc","w")
output.write("".join(command_lines))
output.close()
