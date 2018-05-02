import os, sys

start_dir = sys.argv[1] #directory with protein fasta files
start_file = sys.argv[2] #file with species you want to do all pairwise to, should not end in _prefix,
#should be in the same directory as other species
#use -wd in qsub file for working directory

out = open(start_dir +'/Blast_against_Slyc.sh','w')
file1a = start_dir + "/" + start_file
for files in os.listdir(start_dir):
    print (files)
    if files.endswith('_prefix'):
           file2a = start_dir + "/" + files 
           out.write('module load BLAST; blastall -p blastp -d ' + file2a + ' -i ' + file1a +' -o ' + files[0:3] + '_Slyc.blastp -m 8\n')

