###############################################################
#               VCF FILE
#               Input: original VCF file
#               Output: HEAD of VCF file
################################################################
import  re
import os #used with strip(os.linesep)
import gzip
import ray

@ray.remote
def split_vcf_header(BASE_PATH, file_to_be_splitted):
    # Create a folder to store generated files
    vcf_header_and_body_path = os.path.join(BASE_PATH, 'vcf_header_and_body')
    try:
        os.mkdir(vcf_header_and_body_path)
    except FileExistsError:
        print("Folder Already exists")

    #Save to this file:
    outfile = open(os.path.join(vcf_header_and_body_path, "vcf_head.vcf"), "w")

    #dummy flags
    bodyflag = 0
    dummyflag = 0

    ################################((start READING FILE))#######################################
    with gzip.open(os.path.join(BASE_PATH, file_to_be_splitted), 'r') as inputvcf:

        for line in inputvcf:
            d_line = line.decode('utf-8')
            #######((Find the lines starting with ##))###########################################
            if  re.findall('^#{2}', d_line):
                # print("header")
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


if __name__=='__main__':
    split_vcf_header('/Users/lawrence/Documents/Lawrence/data-api', 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz')