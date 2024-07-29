##############################################################
#
#               Read Reference FASTA
#               break to chromosomes
#               write node and relation session.py files
#
####################((B.O.D.Y))################################
import re
#import neoClass
#import timeit

#open FASTA file to read
file = open('hs37d5.fa', 'r+')
# file = open('ref100lines.fa', 'r+')
inputfasta = file.readlines()
file.close()



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



#variables used
##-*-*-*-*-*-*-*- variables definitions -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
pos=0
flag1stNuc = 0
RefGenome = "hs37d5"
label = "Reference"
chrX = set(("x","X"))
chrY = set(("y","Y"))
chr1to9 = set(("1","2","3","4","5","6","7","8","9"))
##
fastaPos = 0
chrno = 0
prevchrno = 0
#flagChr = 0
#setup = 'import neoClass\n\nfrom neo4j import GraphDatabase\n'
setup = 'from neo4j import GraphDatabase\n'
# connectToDB='\n\n#Connect to Database\ndriver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "sanna"))\n'
connectToDB='\n\n#Connect to Database\ndriver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", ""))\n'
# connectToDB='\n\n#Connect to Database\ndriver = GraphDatabase.driver("http://localhost:7474", auth=("neo4j", ""))\n'

# localhost:7474
startSession='\nwith driver.session() as session:\n'
exitSession = '\ndriver.close()'
defAddChrom = '\n#function for neo4j\ndef add_chromosome(tx, chrno):\n\ttx.run("MERGE (c:Chromosome {id: $number})",\n\t\tnumber=chrno)'
defAddNuc = '\n#function for neo4j\ndef add_nucleotide(tx, chrno, fastaPos, ref, fID):\n\ttx.run("MERGE (r:Reference {refID: $fID, ref: $ref, pos : $pos , chr: $chrn})",\n\t\tref=ref, chrn=chrno, fID=fID, pos=fastaPos)'


defAddAtRel = '\n#function for neo4j\ndef add_at_relation(tx, chrno, fID):\n\ttx.run("MATCH (r:Reference)"\n\t\t"WHERE (r.refID =  $fID) AND (r.chr = $chrn)"\n\t\t"MATCH (z:Chromosome)"\n\t\t"WHERE (z.id = $chrn)"\n\t\t"WITH (r), (z)"\n\t\t"MERGE (z)-[:AT]->(r)",\n\t\tchrn=chrno, fID = fID)'
defAddAdjToRel = '\n#function for neo4j\ndef add_adj_to_relation(tx, fID, chrno, endID):\n\ttx.run("MATCH (r1:Reference)"\n\t\t"WHERE (r1.refID =  $fID) AND (r1.chr = $chrn)"\n\t\t"MATCH (r2:Reference)"\n\t\t"WHERE (r2.refID = $endID) AND (r2.chr = $chrn)"\n\t\t"WITH (r1), (r2)"\n\t\t"MERGE (r1)-[:ADJ_TO]->(r2)",\n\t\tfID=fID, chrn=chrno, endID=endID)'


def openNodeFile(fileNodes):
    refCreateNode = open(fileNodes, "w")
    return refCreateNode

def closeNodeFile(fileNodes):
    fileNodes.close()

for line in inputfasta:
    if re.findall('>', line):
        g = re.findall('>(.+?)\s', line)
        chrno = str(g).strip('[\']')

        #Create new py file
        fileRelations = 'Chr' + chrno + '_Ref_Relations.py'
        prevFileRelations = 'Chr' + str(prevchrno) + '_Ref_Relations.py'

        #Create new py file
        fileNodes = 'Chr' + chrno + '_Ref_Nodes.py'
        prevFileNodes = 'Chr' + str(prevchrno) + '_Ref_Nodes.py'


        if prevchrno !=0:
            #RefCreateNodes = openNodeFile(prevFileNodes)
            if fileNodes != prevFileNodes and fileRelations != prevFileRelations:
                #RefCreateNodes.write('I want to close previous file session\n')
                RefCreateNodes.write(exitSession)
                #RefCreateNodes.write('I want to close previous file here\n')
                RefCreateNodes.close()

                RefCreateNodes = openNodeFile(fileNodes)
                #RefCreateNodes.write('I have opened a new file here\n')

                #RefCreateNodes.close()

            #elif fileRelations != prevFileRelations:
                # print('Nada\n')
                RefCreateRelations.write(exitSession)
                RefCreateRelations.close()

                RefCreateRelations = openNodeFile(fileRelations)

            else:
                print('Something went wrong\n')

        else:
            RefCreateNodes = openNodeFile(fileNodes)
            RefCreateRelations = openNodeFile(fileRelations)


         #For Add Nodes setup:
        RefCreateNodes.write(setup)
        #RefCreateNodes.write(connectToDB)
        RefCreateNodes.write(defAddChrom)
        RefCreateNodes.write(defAddNuc)
        RefCreateNodes.write(connectToDB)

        #For Add Relations setup:
        RefCreateRelations.write(setup)
        #RefCreateRelations.write(connectToDB)
        RefCreateRelations.write(defAddAtRel)
        RefCreateRelations.write(defAddAdjToRel)
        RefCreateRelations.write(connectToDB)

        #Start writing code:
        #RefCreateRelations.write('n = neoClass()\n')
        #RefCreateNodes.write('n = neoClass()\n')
        RefCreateNodes.write(startSession)
        RefCreateRelations.write(startSession)
        #RefCreateNodes.write('\tsession.write_transaction(n.add_chromosome, ')
        RefCreateNodes.write('\tsession.execute_write(add_chromosome, ')
        RefCreateNodes.write(repr(chrno))
        RefCreateNodes.write(')\n')

    else:
        prevchrno = chrno





#        if prevchrno !=0:
#            #RefCreateNodes = openNodeFile(prevFileNodes)
#            if fileNodes != prevFileNodes and fileRelations != prevFileRelations:
#                #RefCreateNodes.write('I want to close previous file session\n')
#                RefCreateNodes.write(exitSession)
#                #RefCreateNodes.write('I want to close previous file here\n')
#                RefCreateNodes.close()
#
#                RefCreateNodes = openNodeFile(fileNodes)
#                #RefCreateNodes.write('I have opened a new file here\n')
#
#                #RefCreateNodes.close()
#
#            #elif fileRelations != prevFileRelations:
#                print('Nada\n')
#                RefCreateRelations.write(exitSession)
#                RefCreateRelations.close()
#
#                RefCreateRelations = openNodeFile(fileRelations)
#
#            else:
#                print('Something went wrong\n')





        line = line.rstrip()
        for c in line:
            fastaPos +=1

            if fastaPos == 1:
                #RefCreateNodes.write('\tsession.write_transaction(n.add_nucleotide, ') #chrno, fastaPos, ref, fID
                fID=getFastaId(chrno,fastaPos)
                # RefCreateNodes.write('\tsession.write_transaction(add_nucleotide, ')
                RefCreateNodes.write('\tsession.execute_write(add_nucleotide, ')                
                RefCreateNodes.write(repr(chrno))
                RefCreateNodes.write(', ')
                RefCreateNodes.write(repr(fastaPos))
                RefCreateNodes.write(', ')
                RefCreateNodes.write(repr(c))
                RefCreateNodes.write(', ')
                RefCreateNodes.write(repr(fID))
                RefCreateNodes.write(')\n')

                #RefCreateRelations.write('\tsession.write_transaction(n.add_at_relation, ')
                # RefCreateRelations.write('\tsession.write_transaction(add_at_relation, ')
                RefCreateRelations.write('\tsession.execute_write(add_at_relation, ')
                # RefCreateRelations.write(repr(fastaPos))
                # RefCreateRelations.write(', ')
                RefCreateRelations.write(repr(chrno))
                RefCreateRelations.write(', ')
                RefCreateRelations.write(repr(fID))
                RefCreateRelations.write(')\n')

            if fastaPos > 1:#we are excluding start node
                #RefCreateNodes.write('\tsession.write_transaction(n.add_nucleotide, ')
                fID=getFastaId(chrno,fastaPos)
                # RefCreateNodes.write('\tsession.write_transaction(add_nucleotide, ')
                RefCreateNodes.write('\tsession.execute_write(add_nucleotide, ')
                RefCreateNodes.write(repr(chrno))
                RefCreateNodes.write(', ')
                RefCreateNodes.write(repr(fastaPos))
                RefCreateNodes.write(', ')
                RefCreateNodes.write(repr(c))
                RefCreateNodes.write(', ')
                RefCreateNodes.write(repr(fID))
                RefCreateNodes.write(')\n')

                #RefCreateRelations.write('\tsession.write_transaction(n.add_at_relation, ')
                RefCreateRelations.write('\tsession.execute_write(add_at_relation, ')
                # RefCreateRelations.write(repr(fastaPos))
                # RefCreateRelations.write(', ')
                RefCreateRelations.write(repr(chrno))
                RefCreateRelations.write(', ')
                RefCreateRelations.write(repr(fID))
                RefCreateRelations.write(')\n')

                #RefCreateRelations.write('\tsession.write_transaction(n.add_adj_to_relation, ')
                prevpos=fastaPos-1
                startID=getFastaId(chrno,prevpos)
                RefCreateRelations.write('\tsession.execute_write(add_adj_to_relation, ')
                RefCreateRelations.write(repr(startID))
                RefCreateRelations.write(', ')
                RefCreateRelations.write(repr(chrno))
                RefCreateRelations.write(', ')
                RefCreateRelations.write(repr(fID))
                RefCreateRelations.write(')\n')




RefCreateNodes.close()
RefCreateRelations.close()
