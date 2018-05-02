import os, sys

start_dir = sys.argv[1] #directory with protein fasta files
start_dir2 = sys.argv[2] #directory with divided fastas

for file in os.listdir(start_dir):
    if file.endswith("_goodProteins.fasta"):
        name = file.strip().split("_")
        file_name1 = name[0]
        print (file_name1)
        output = open(str(file_name1)+"_command_files_BLAST.sh", 'w')
        file1a = start_dir + "/" + file
        for file2 in os.listdir(start_dir2):
            if file2.startswith("goodProteins.fasta_"):
                if file2.endswith(".phr"):
                    pass
                elif file2.endswith(".pin"):
                    pass
                elif file2.endswith(".psd"):
                    pass
                elif file2.endswith(".psi"):
                    pass
                elif file2.endswith(".psq"):
                    pass
                else:
                    name2 = file2.strip().split("_")
                    file_name2 = name2[1]
                    file2a = start_dir2 + "/" + file2
                    output.write("module load BLAST; blastall -i %s -d %s -o %s-%s_results.txt -p blastp -m 8\n" % (file1a, file2a, file_name1, file_name2))
        output.close()
        