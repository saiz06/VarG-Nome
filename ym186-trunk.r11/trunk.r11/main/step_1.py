##################################################################################
#
#               Get CSV file of nodes from .fa
#				(needs to be done for every file separately)
#				Change filename at comment
#					1. read from file 
#							->> change ("sample.fa") to your file ("your_file.fa")
#					2. output files (2 files)
#							->> change ("nodes_fasta_sample.csv","w") to ("nodes_fasta_your_file.csv","w")
#							->> change ("rels_fasta_sample.csv","w") to ("rels_fasta_your_file.csv","w")
#
##################################################################################
import re
import os
import ray

##-*-*-*-*-*-*-*- FUNTIONS -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#--(FASTA ID) - generator ----------------------------------------------------------
def getFastaId(CHROM,POS):
	chrX = set(("x","X"))
	chrY = set(("y","Y"))
	chr1to9 = set(("1","2","3","4","5","6","7","8","9"))
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
def writeFastaNode(fID, pos, RefGenome,chrno,nucleotide,label,fa,nodes_rel_chromes_path):
	nodefile = open(os.path.join(nodes_rel_chromes_path, f"nodes_fasta_{fa}.csv"),"w")
	nodefile.write("nucID,pos,RefGenome,chrom,ref,LABEL\n")
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
def writeFastaRel(endID, pos, chrno, fa, edges_path):
	prevPos = pos - 1
	startID = getFastaId(chrno,prevPos)
	relfile = open(os.path.join(edges_path, f"rels_fasta_{fa}.csv"),"w")
	relfile.write("START_ID(Ref-ID),END_ID(Ref-ID)\n")
	relfile.write(str(startID))
	relfile.write(",")
	relfile.write(str(endID))
	relfile.write("\n")



#####################################################################################
##-*-*-*-*-*-*-*- MAIN -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
#####################################################################################
#1. read from this file:
@ray.remote
def nodes_rels_of_chromosomes(BASE_PATH, RefGenome):
	label = "Reference"
	# Create a new folder to store generated chromosomes nodes and relationships CSV
	nodes_rel_chromes_path = os.path.join(BASE_PATH, f'{RefGenome}'.split('.')[0]+f'nodes')
	edges_rel_chromes_path = os.path.join(BASE_PATH, f'{RefGenome}'.split('.')[0]+f'edges')
	try:
		os.mkdir(nodes_rel_chromes_path)
		os.mkdir(edges_rel_chromes_path)
	except FileExistsError:
		print("Folders Already exists")

	# Reference existing foler for fas generated in extractFASTA file
	fas_folder_path = os.path.join(BASE_PATH, f'{RefGenome}'.split('.')[0]+f'_fas')

	# Loop through each of the files in the folder
	for fa in os.listdir(fas_folder_path):
		with open(os.path.join(fas_folder_path, fa)) as myfile:        
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
							writeFastaNode(fID, pos, f'{RefGenome}'.split('.')[0], chrno, nucleotide, label, fa, nodes_rel_chromes_path)
							
						else:
							pos += 1
							fID = getFastaId(chrno,pos)					
							writeFastaNode(fID, pos, f'{RefGenome}'.split('.')[0], chrno, nucleotide, label, fa, nodes_rel_chromes_path)
							writeFastaRel(fID, pos, chrno, fa, edges_rel_chromes_path)



if __name__=='__main__':
    nodes_rels_of_chromosomes('/Users/lawrence/Documents/Lawrence/data-api', 'hs37d5.fa')