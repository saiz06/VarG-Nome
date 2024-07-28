###############################################################
#               VCF FILE
#               Input: original VCF file
#               Output: BODY of VCF file
################################################################
import  re
import os #used with strip(os.linesep)
import gzip
import ray

@ray.remote
def split_vcf_body(BASE_PATH, file_to_be_splitted):
        vcf_header_and_body_path = os.path.join(BASE_PATH, 'vcf_header_and_body')
        try:
                os.mkdir(vcf_header_and_body_path)
        except FileExistsError:
                print("Folder Already exists")
                
        #Save to this file:
        outfile = open(os.path.join(vcf_header_and_body_path, "vcf_body.vcf"),"w")

        #dummy flags
        headerflag = 0
        dummyflag = 0

        ################################((start READING FILE))#######################################
        with gzip.open(os.path.join(BASE_PATH, file_to_be_splitted), 'r') as inputvcf:

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

if __name__=='__main__':
    split_vcf_body('/Users/lawrence/Documents/Lawrence/data-api', 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz')