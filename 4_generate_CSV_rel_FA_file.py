###############################################################
#
#               Get CSV file of startPos and endPos for
#               creating (n)-[:NEXT]->(m) relationship
#				Change filename at 
#					1. output filename
#
###############################################################

#variables definitions
pos=1

#1. output filename
#outfile = open("NEXT_rel_CHR1.csv","w")
#outfile = open("20M_rel_CHR1.csv","w")
#outfile = open("CHR1_rel.csv","w")
#outfile.write("startPos,endPos\n")
outfile = open("samplefasta_rel.csv","w")
outfile.write(":START_ID(Ref-ID),:END_ID(Ref-ID)\n")

#while pos <2000000:
while pos <31:
	startPos = pos
	pos +=1
	endPos = pos

	outfile.write(str(startPos))
	outfile.write(",")
	outfile.write(str(endPos))
	outfile.write("\n")

