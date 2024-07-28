################################################################
#
#		SPLIT FILE to individual .fa
#
####################((B.O.D.Y))################################
import  re
import os #used with strip(os.linesep)

#Save to these files
counter = open("fasta_chr_record_count.txt","w")

file_variable=""

file = open('hs37d5.fa', 'r+')
inputfasta = file.readlines()
file.close()

#fastaPos = 0
#chrno = 0
#flagChr = 0

#chrom_list = []

#read file line by line
################################((start READING FILE))#######################################
for line in inputfasta:

    #find start line
    if re.findall ('>', line):
        g = re.findall('>(.+?)\s',line)
        chrno = str(g).strip('[\']')

	
	fname = "Ref_Chr_"+chrno+".fa"
	file_variable = "Chr"+chrno
	file_variable = open(fname,"w")
	
	
	file_variable.write(line)
	
	
    else:
        line = line.rstrip()
	file_variable.write(line)



#        print (len(line))
#        #for c in line:
#            #print (c)
#            #fastaPos +=1
#            #if c is not "\n":
#	    	#print("total length: ")
#	    	#print len(line)
#               
#
