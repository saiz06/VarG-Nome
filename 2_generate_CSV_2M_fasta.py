###############################################################
#
#               Get CSV file of first N lines from .fa
#
###############################################################
import re

#variables definitions
pos=0
RefGenome = "hs37d5"

#save to this file:
outfile = open("Tmp_CHR1.csv","w")
#outfile = open("REFGEN_CHR1.csv","w")
#outfile.write("RefGenome,Chromosome,Position,Nucleotide\n")
outfile.write("Position:ID(Ref-ID),RefGenome,Chromosome,Nucleotide,:LABEL\n")

#read from this file:
with open("first_N_lines.fa") as myfile:    
    for line in myfile:
        if re.findall('>', line):
                    g = re.findall('>(.+?)\s', line)
                    chrno = str(g).strip('[\']')
        else:
            line = line.rstrip()
            for nucleotide in line:            
                pos += 1
                outfile.write(str(pos))
                outfile.write(",")
                outfile.write(RefGenome)
                outfile.write(",")
                outfile.write(chrno)
                outfile.write(",")
                outfile.write(nucleotide.upper())
                outfile.write(",")
                outfile.write("Ref")
                outfile.write("\n")
#print(str(pos))

