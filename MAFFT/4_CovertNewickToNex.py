# IMPORT
import sys
import os

# MAIN
# Reads a list of tree files
# in Newick format and converts
# them to NEXUS format

files = [f.strip() for f in open(sys.argv[1],"r").readlines()]

for f in files:
    os.system("python /mnt/home/panchyni/0_MainProjects/3_TranscriptionFactorEvolution/0_RawData/10_RAxML_FullLengthProtein/Newick_to_Nexus.py " + f)
