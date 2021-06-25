import sys, getopt, re, string

Ks_out = "Fpennsylvanica_Ks_test_ALL_KS.txt"
gff_ash_file = "Fpennsylvanica_v1.4_genes.gff"

circos_output = "Ash-vs-self-orthologs_corrected.circos.tsv"

###########################################
# create map of ash genes to scaffolds

ash_gene2scaf = {}
ash_gene2start = {}

inhandle = open(gff_ash_file)
for line in inhandle:
    if not line.startswith('#'):
        fields = line.split('\t')
        scaf = fields[0]
        type = fields[2]
        start = fields[3]
        end = fields[4]
        desc = fields[8]
        if type == 'gene':
            match = re.search("ID=(\S+?);", desc)
            gid = match.group(1) if match else None
            ash_gene2scaf[gid] = scaf
            ash_gene2start[gid] = start
            #print(gid)
inhandle.close()	

print(gid, ash_gene2start[gid])

###########################################
# produce the circos output file

inhandle = open(Ks_out)
outhandle = open(circos_output, "w")

for line in inhandle:
    if not line.startswith('#'):
        fields = line.split('\t')
        if float(fields[3]) <= 0.25:
            ash_gene_1 = fields[1]
            ash_gene_2 = fields[2]
            if ash_gene_1 in ash_gene2scaf: 
                ash_chr_1 = ash_gene2scaf[ash_gene_1.rstrip()]
                chr_color = ash_chr_1.lower()
                chr_color = re.sub('chr0', 'chr', chr_color)
                ash_chr_1 = re.sub('Chr','Fp_', ash_chr_1)
                ash_chr_1 = re.sub('_0','_', ash_chr_1)
                ash_start_1 = ash_gene2start[ash_gene_1.rstrip()]
                ash_stop_1 = int(ash_start_1) + 1000

                ash_chr_2 = ash_gene2scaf[ash_gene_2.rstrip()]
                ash_chr_2 = re.sub('Chr','Fp_', ash_chr_2)
                ash_chr_2 = re.sub('_0','_', ash_chr_2)
                ash_start_2 = ash_gene2start[ash_gene_2.rstrip()]
                ash_stop_2 = int(ash_start_2) + 1000

                if ash_chr_1 != ash_chr_2:
                    out_list = [ash_chr_1, ash_start_1, str(ash_stop_1), ash_chr_2, ash_start_2, str(ash_stop_2), 'color=' + chr_color + '\n']
                    outhandle.write("\t".join(out_list))

inhandle.close()
outhandle.close()
