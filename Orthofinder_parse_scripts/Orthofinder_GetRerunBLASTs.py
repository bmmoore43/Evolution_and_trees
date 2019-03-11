#make finished files txt document with BLASTs that are completed:
#ls Blast*.txt > finished_files.txt
import sys, os
start_dir = sys.argv[1]
finished_files = open(sys.argv[2], 'r')
cc= open("rerun_BLASTcc.sh", "w")

DB_list = []
species_list = []
for file in os.listdir(start_dir):
    if file.endswith(".phr"):
        filename = file.strip().split(".")[0]
        name2= filename.split("Species")[1]
        DB_list.append(name2)
    elif file == "SpeciesIDs.txt":
        speciesIDs = open("SpeciesIDs.txt", 'r')
        for line in speciesIDs:
            if line.startswith("#"):
                pass
            else:
               species= line.strip().split(":")[0]
               species_list.append(species)        

#print (DB_list, species_list)

blast_list=[]
for i in species_list:
    for x in DB_list:
        blast= "Blast%s_%s.txt" %(i, x)
        blast_list.append(blast)
        
print (blast_list, len(blast_list))

finished_list = []
for l in finished_files:
    blast = l.strip().split("\t")[0]
    finished_list.append(blast)

print (finished_list)

new_blast_list=[]
for y in blast_list:
    if y in finished_list:
        pass
        #print (y)
    else:
        new_blast_list.append(y)        
        
print (new_blast_list, len(new_blast_list))

for j in new_blast_list:
    species = j.split("t")[1].split("_")[0]
    #print (species)
    db = j.split("_")[1].split(".")[0]
    cc.write("blastp -outfmt 6 -evalue 0.001 -query %s/Species%s.fa -db %s/BlastDBSpecies%s -out %s/%s\n" %(start_dir, species, start_dir, db, start_dir, j))
    
cc.close()
finished_files.close()