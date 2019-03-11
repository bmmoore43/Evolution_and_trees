### parse orthofinder, get orthologues for each gene

import sys, os, pandas


inp= open(sys.argv[1], 'r')
output= open(sys.argv[1]+'.ortholist.txt', 'w')

header= inp.readline()
D={}
for line in inp:
    new_list= []
    L=line.strip().split('\t')
    SLyc= L[1].split(",")
    Ath= L[2].split(",")
    for gene1 in Ath:
        gene1= gene1.split("Ath_")[1]
        new_list.append(gene1)
    for gene in SLyc:
        gene= gene.split("Sly_")[1]
        if gene not in D:
            D[gene]= new_list
        else:
            D[gene].append(new_list)
            

print (D)

output.write("gene\tortholog\n")
for key in D:
    datalist= D[key]
    datastr= "\t".join(datalist)
    output.write('%s\t%s\n' % (key, datastr))
        