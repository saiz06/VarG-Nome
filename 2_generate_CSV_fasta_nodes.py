##################################################################################
#
#               Get CSV file of nodes from .fa
#				(needs to be done for every file separately)
#				Change filename at comment
#					1. read from file
#					2. output files (2 files)
#
##################################################################################
import re

##-*-*-*-*-*-*-*- variables definitions -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
pos=0
flag1stNuc = 0
RefGenome = "hs37d5"
label = "Reference"
chrX = set(("x","X"))
chrY = set(("y","Y"))
chr1to9 = set(("1","2","3","4","5","6","7","8","9"))

##-*-*-*-*-*-*-*- 2. output files -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#nodefile = open("REFGEN_CHR1.csv","w")
nodefile = open("nodes_fasta.csv","w")
nodefile.write("nucID:ID(Ref-ID),pos,RefGenome,chrom,ref,:LABEL\n")

relfile = open("rels_fasta.csv","w")
relfile.write(":START_ID(Ref-ID),:END_ID(Ref-ID)\n")

##-*-*-*-*-*-*-*- FUNTIONS -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#--(FASTA ID) - generator ----------------------------------------------------------
def getFastaId(CHROM,POS):
	fastaPos = int(POS)
	if CHROM in chrX:
		fastaID = "1"+"23"+str(fastaPos)
	elif CHROM in chrY:
		fastaID = "1"+"24"+str(fastaPos)
	elif CHROM in chr1to9:
		fastaID = "10"+str(CHROM)+str(fastaPos)
	else:
		fastaID = "1"+str(CHROM)+str(fastaPos)	
	return fastaID

#--(nodes) - write to file --------------------------------------------------------
def writeFastaNode(fID, pos, RefGenome,chrno,nucleotide,label):
	nodefile.write(str(fID))
	nodefile.write(",")
	nodefile.write(str(pos))
	nodefile.write(",")
	nodefile.write(RefGenome)
	nodefile.write(",")
	nodefile.write(chrno)
	nodefile.write(",")
	nodefile.write(nucleotide.upper())
	nodefile.write(",")
	nodefile.write("Ref")
	nodefile.write("\n")

#--(relationships) - write to file -------------------------------------------------
def writeFastaRel(endID, pos, chrno):
	prevPos = pos - 1
	startID = getFastaId(chrno,prevPos)
	relfile.write(str(startID))
	relfile.write(",")
	relfile.write(str(endID))
	relfile.write("\n")



#####################################################################################
##-*-*-*-*-*-*-*- MAIN -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
#####################################################################################
#1. read from this file:
#with open("Ref_Chr_1.fa") as myfile:
with open("sample.fa") as myfile:        
	for line in myfile:
		if re.findall('>', line):
			g = re.findall('>(.+?)\s', line)
			chrno = str(g).strip('[\']')
			pos = 0
			flag1stNuc = 1
		else:
			line = line.rstrip()
			for nucleotide in line:   
				if flag1stNuc == 1: #first nucleotdie	
					flag1stNuc = 0 #no longer 1st			       
					pos += 1
					fID = getFastaId(chrno,pos)					
					writeFastaNode(fID, pos, RefGenome, chrno, nucleotide, label)
					
				else:
					pos += 1
					fID = getFastaId(chrno,pos)					
					writeFastaNode(fID, pos, RefGenome, chrno, nucleotide, label)
					writeFastaRel(fID, pos, chrno)

