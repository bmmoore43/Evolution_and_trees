# Tree_building
Use for getting orthologs, building trees, or reconciling trees

## Reconciling gene trees by building new species tree

1. Choose orthogroup that has a gene ratio of 1:1:1:1.. for each species. From Orthofinder, this is labeled "SingleCopyOrthogroups". You 
will need to get the genes for each group from Orthogroups.txt file.

2. Get protein sequences using a fasta file with all species used and a file with the [orthogroup: each gene] in each row.

        python GetProteinSequences_forGenelist.py <combined fasta file> <orthogroup file>
        
3. Use MAFFT to get the alignment for each group

    1. put all fasta files of domains in a folder, then get list of fasta files
    
            ls [folder]/*.fasta > FamilyFASTAFiles.txt
    
    2. run command for maftt
    if trying to merge unknown symbols use --anysymbol command, otherwise do not put any command
    
        mafft --anysymbol <fasta file> > <output.mafft_align>
    
    Use command script if multiple fasta files:
    
        python 0_WriteMAFFTCommand.py FamilyFASTAFiles.txt
        module load MAFFT
        nohup sh MafftCommands.cc &
    
    Submit command file via qsub:
    
        python ~john3784/Github/parse_scripts/qsub_hpc.py -f submit -c MafftCommands.cc -n 100 -w 239 -m 10 -mo MAFFT -wd <working directory>
    
4. Once you have alignments, combine all genes from the same species into the same alignment. You can rename the gene name for the species 
it represents.

5. Now run RAxML on the combined alignment. 

    1. Make a list of all your alignment files. Note: raxml does not like / character in input files.
    
            ls *align > FamilyAlignFiles.txt 
            
    2. write files to a Raxml command line. Note, since this uses a seed function, you should keep the command lines if you want to be 
    able to rerun the same tree. This command specifies outgroup (-o) and bootstrapping (-#).
    
        python 1a_WriteRAxMLCommands_bootstr_outgroup.py FamilyAlignFiles.txt
        
    3. Qsub command file, note: need -wd to switch to the work directory with files
    
            python ~shius/codes/qsub_hpc.py -f submit -c RAxMLCommands.cc -wd <directory with Mafft alignments> -n 100 -w 240 -m 10 -mo RAxML
            
6. Input new species tree to Orthofinder

    Output will be a species tree labeled as "RAxML_bipartitionsBranchLabels.--.mafft_align.RAxML". Make sure the names of the species tree match the original names of the fasta files used in orthofinder. 
    
    1. Make Orthofinder command line:
    
            /mnt/home/john3784/Github/OrthoFinder/OrthoFinder-2.1.2/orthofinder -ft <../WorkingDirectory/Orthologues_--/> -s <RAxML_speciestree.txt> -t 8
            
    2. Qsub command file in Orthofinder folder
    
            python ~/Github/parse_scripts/qsub_hpc.py -f submit -c commandfile.sh -u john3784 -m 20 -w 2160 -mo OrthoFinder/2016 -p 8
