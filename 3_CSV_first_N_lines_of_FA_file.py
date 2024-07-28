###############################################################
#
#				To get a small sample,
#               Get first N lines of node CSV file
#
###############################################################


#Define number of lines:
N=2000001
#N=21

#Save to this file:
outfile = open("2M_CHR1.csv","w")
#outfile = open("test_20_nodes_CHR1.csv","w")


#Extract:
with open("REFGEN_CHR1.csv") as myfile:    
    head = [next(myfile) for x in range(N)]

#Write to file:
for line in head:
    outfile.write(line)

