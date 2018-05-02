##script used get a matrix for genes in particular domains (1= gene has domain, 0= gene does not have domain)
import os, sys

scanout_file = open(sys.argv[1], 'r') #scan out file such as all-enzymes-Athalina.out
AT_gene_file = open(sys.argv[2], 'r') #file with all genes in genome you are interested in
domain_file = open(sys.argv[3], 'r')# file with domains you are interested in ie. Athaliana_SM.domain_list.txt
sum_matrix = open(sys.argv[4],"w")

# add all gene data
AT_gene_list = []
def add_ATgene_data(inp):
    for line in inp:
        if line.startswith('AT'):
           L = line.strip().split("\t")
           gene = L[0]
           AT_gene_list.append(gene)

add_ATgene_data(AT_gene_file)
#print AT_gene_list 

def clear_spaces(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","\t")
	return string
D = {}

# add genes from a particular domain
def get_domaingene(inp, D):
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
                gene = L[3]
                #if gene in AT_gene_list:
                if dom_name not in D:
                    D[dom_name] = [gene]
                else:
                    D[dom_name].append(gene)

            else:
                    pass
                
get_domaingene(scanout_file, D)

print (D)

domain_list = []
def get_domains(inp):
    for line in inp:
        L = line.strip().split("\t")
        domain = L[0]
        domain_list.append(domain)
         
get_domains(domain_file)

title_str = "\t".join(domain_list)
sum_matrix.write('gene\t%s\n' %(title_str))

D2 = {}

for gene in AT_gene_list:
    value_list = []
    for name in domain_list:
        if name in D.keys():
            gene_list = D[name]
            if gene in gene_list:
                value = '1'
                value_list.append(value)
            else:
                value = '0'
                value_list.append(value)
       # else:
           # value_list.append('0')
    D2[gene] = value_list
            
print (D2)               
for gene in D2:
    data_list= D2[gene]
    #for data in data_list:
    string= "\t".join(data_list)
    sum_matrix.write(gene + "\t" + "%s" % string + "\n")
sum_matrix.close()            
    