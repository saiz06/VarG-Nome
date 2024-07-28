###############################################################
#               VCF FILE
#               Input: original VCF file
#               Output: BODY of VCF file
################################################################
import  re
import os #used with strip(os.linesep)
import gzip

#Save to this file:
outfile = open("vcf_body.vcf","w")

#dummy flags
headerflag = 0
dummyflag = 0

################################((start READING FILE))#######################################
with gzip.open('ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz', 'r') as inputvcf:

        for line in inputvcf:
                d_line = line.decode('utf-8')
                #######((Find the lines starting with ##))###########################################
                if  re.findall('^#{2}', d_line):
                        print("header")
                ##################################################################################################
                elif d_line == '\n':
                        dummyflag=0

                ##################################################################################################
                elif  re.findall('^#CHROM', d_line): #found definition of body
                        
                        headerflag = 0
                #################################################################################################
                else:
                       outfile.write(str(d_line))

