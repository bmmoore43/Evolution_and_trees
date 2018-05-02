# IMPORT
import sys
import os

# MAIN
# Reads *bestTree* files in the current folder and 
# extract the names of finished runs

os.system("ls *bestTree* > bestTree.tmp")

inlines = [l.strip() for l in open("bestTree.tmp","r").readlines()]

finished_groups = [".".join(name.split(".")[1:6]) for name in inlines]

for group in finished_groups:
    print group
