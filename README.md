# Tree_building
Use for getting orthologs, protein domain families, building trees, or reconciling trees

## Mapping PFAM domains to protein sequences
1. Prep:
   To make use of PFAM domains, you will need:
   
   A database of PFAM domains (see ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/ and use the lastest release)

   A FASTA file of protein
   
   HMMER (available on Calculon2 and HPCC [module load hmmer])

   For examples of the database file (Pfam-A.hmm), protein FASTA file (Athaliana_167_protein_primaryTranscriptOnly.fa.mod) and finished run (Athal.PFAMScan.out), see 
   
        /mnt/home/panchyni/0_MainProjects/3_TranscriptionFactorEvolution/0_RawData/9_PFAM 
        
   on HPCC.

2. Run hmmscan using trusted cutoff (see HMMER user guide for explanation)

   To run hmmscan:
   
   options:
   --cut_tc = trusted cutoff
   --domtblout = output format
   
        module load hmmer; hmmscan --cut_tc --domtblout <output file- file.scan.out> <pfam file- Pfam-A.hmm> <protein fasta file>
        
   This generates one output, example:
   
        ~john3784/3-Solanaceae_project/domain_files/scan-out-Sol_files.pp/Solanum_lycopersicum_GCF_000188115.3_SL2.50_protein.scanout.noredun

3. Get a binary matrix from this output where each row is a gene and each column is a domain, 1 indicating given gene has the given domain, 0 indicating it does not:

        parse_domain-out_files_getmatrix.py [file with genes:Class] [domain.out file]
        
4. Get domains that you want to use - this script gets domains from hmm scan-out file for a list of genes
    
    1. from a list of genes get domains for those genes:
        
                python parse_outfile_getdomains.py [hmm-scan-out file] [gene list] [output]
        
    2. can get a list of each gene-domain pair, outputs all genes with that domain
    
                parse_outfile_getdomains2.py [hmm-scan-out file] [gene list] [output]


### Other HMMER options

1. HMMSearch: You can also run hmmsearch, useful if you want to look for a particular domain (database should include just that domain) or if you want to use your own e-value as a cutoff instead of trusted cutoff. Groups of genes with the same domain can be considered in the same gene family

   To do an hmm search, run the following command

        hmmsearch [PFAM database] [Protein FASTA] > [outfile]

    This will generate three outputs:

        outfile.out = The raw ouput, somewhat reminiscent of raw BLAST output
        outfile.perSeq.out = Tabular output indexed by protein sequence
        outfile.perDom.out = Tabular output sequence by domain 

2. Parsing Ouput: In general, how you parse the output will depend on what you want to do with the data (i.e. do want individual domains? groups of domain? domains filtered by a gene list). 

The following steps will filter the ouput for specific domains, e-value, and occurrenece, the divide a list of genes by domains and obtain a corresponding FASTA file of proteins.

   1. First, assemble a list of protein domains in a single column text file and run:
   
                python GetDomains.py [Domain List] [outfile.perSeq.out]
                
   2. This will create an oufile named "outfile.perSeq,out.Domains". Next, we filter for e-value:

                python FilterByEvalue.py [outfile.perSeq,out.Domain] [e-value]

   3. This will create an outfile named "outfile.perSeq,out.Domains.Evalue_[evalue]". Next, we filter by the number of occurences for each domains:
   
                python FilterByOccurence.py [outfile.perSeq,out.Domains.Evalue_[evalue]] 4

   Note: We use 4, because BayesTraits requires a minimum of 4 genes per family
This will create an outfile named "outfile.perSeq,out.Domains.Evalue_[evalue].Occurence". 

  4. Next, we split the genes into groups by domain:

                python SplitIntoGroups.py [outfile.perSeq,out.Domains.Evalue_[evalue].Occurence]

   This will create several files with the following format: [Domain].domain.group. 
   
  5. Next, create a list of *.domain.group files and get protein FASTA files for each

                ls *.domain.list > DomainFiles.txt
                python GetProteinSequences.py [Protein FASTA] DomainFiles.txt

With these group of proteins and associated protein sequence files, we can move on to making gene trees with RAxML


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
