###############################################################
#               VCF FILE
#               Input: original VCF file
#               Output: HEAD of VCF file
################################################################
import  re
import os #used with strip(os.linesep)
import gzip

#Save to this file:
outfile = open("vcf_head.vcf","w")

#dummy flags
bodyflag = 0
dummyflag = 0

################################((start READING FILE))#######################################
with gzip.open('ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz', 'r') as inputvcf:

        for line in inputvcf:
                d_line = line.decode('utf-8')
                #######((Find the lines starting with ##))###########################################
                if  re.findall('^#{2}', d_line):
                        #print("header")
			outfile.write(str(d_line))
                ##################################################################################################
                elif d_line == '\n':
                        dummyflag=0

                ##################################################################################################
                elif  re.findall('^#CHROM', d_line): #found definition of body
                        
                        bodyflag = 1
                #################################################################################################
                else:
                       #outfile.write(str(d_line))
			dummyflag=1

