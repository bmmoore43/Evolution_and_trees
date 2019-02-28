##script used get a matrix for genes in particular domains (1= gene has domain, 0= gene does not have domain)
import os, sys

gene_file = open(sys.argv[1], 'r') #file with all genes in genome you are interested in, 1st col gene, 2nd col class
scanout_file = open(sys.argv[2], 'r') #scan out file such as all-enzymes-Athalina.out
#domain_file = open(sys.argv[3], 'r')# file with domains you are interested in ie. Athaliana_SM.domain_list.txt
sum_matrix = open(str(sys.argv[1])+".domain_matrix.txt","w")
output = open(str(sys.argv[1])+".gene-domain_list.txt","w")

# add all gene data
gene_list = []
Dg = {}
def add_ATgene_data(inp, D_gene):
    firstLine = inp.readline()
    for line in inp:
        L = line.strip().split("\t")
        gene = L[0]
        class1= L[1]
        D_gene[gene]= class1
        gene_list.append(gene)
    return(gene_list, D_gene)

gene_list, D_gene= add_ATgene_data(gene_file, Dg)
print (gene_list)

def clear_spaces(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","\t")
	return string
D = {}
D1 = {}
# add genes from a particular domain
def get_domaingene(inp, D, D1):
    for line in inp:
        if line.startswith('#'):
            pass
        else:
            line = clear_spaces(line)
            L = line.strip().split('\t')
            #print (L)
            if len(L) >= 4:
                dom_name = L[0]
                dom_num = L[1]
                domain = ",".join(L[0:2])
                gene = L[3]
                #if gene in AT_gene_list:
                if dom_name not in D:
                    D[dom_name] = [gene]
                else:
                    D[dom_name].append(gene)
                if gene not in D1:
                    D1[gene] = [domain]
                else:
                    D1[gene].append(domain)

            else:
                    pass
                
get_domaingene(scanout_file, D, D1)

print (D)

domain_list = D.keys()
print (domain_list)

title_str = "\t".join(domain_list)
sum_matrix.write('gene\tclass\t%s\n' %(title_str))

D2 = {}

for gene in D_gene:
    classx = D_gene[gene]
    gene_cl_list = [gene, classx]
    gene_cl = "\t".join(gene_cl_list)
    value_list = []
    for name in domain_list:
        if name in D.keys():
            gene_list2 = D[name]
            if gene in gene_list2:
                value = '1'
                value_list.append(value)
            else:
                value = '0'
                value_list.append(value)
       # else:
           # value_list.append('0')
    D2[gene_cl] = value_list
            
print (D2)               
for gene in D2:
    data_list= D2[gene]
    #for data in data_list:
    string= "\t".join(data_list)
    sum_matrix.write(gene + "\t" + "%s" % string + "\n")
sum_matrix.close()  

print (D1)
output.write('gene\tclass\tdomains\n')
for gene in D_gene:
    classx = D_gene[gene]
    gene_cl_list = [gene, classx]
    gene_cl = "\t".join(gene_cl_list)
    if gene in D1.keys():
        data_list2= D1[gene]
        string2= ";".join(data_list2)
        output.write(gene_cl + "\t" + "%s" % string2 + "\n")
output.close() 
scanout_file.close()
gene_file.close()      
    