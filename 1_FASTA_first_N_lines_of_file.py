###############################################################
#
#               Get first N lines of FASTA file
#
###############################################################


#Define number of lines:
N=250000

#Save to this file:
outfile = open("first_N_lines.fa","w")


#Extract:
with open("Chr1.fa") as myfile:    
    head = [next(myfile) for x in range(N)]

#Write to file:
for line in head:
    outfile.write(line)

