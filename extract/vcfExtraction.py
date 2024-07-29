###############################################################
#               VCF FILE
#               Input: original VCF file
#               Output: HEADER & BODY of VCF file, then 
#               split the body based on chromosome
################################################################
import  re
 #used with strip(os.linesep)
import gzip

import os
import subprocess

script_directory = '/home/sanna/demo/extract'
output_directory = script_directory

#step 1: extract header
scriptExtractHead = '5_get_VCF_head.py'
# outputFileStep01 = 'vcf_head.vcf'

#step 2: extract body
scriptExtractBody = '6_get_VCF_body.py'
# outputFileStep01 = 'vcf_body.vcf'

#step 3: split body based on chromosome numbers
scriptSplitBody = '7_separate_vcf_body.py'
# outputFileStep01 = 'vcf_head.vcf'




# Run the scripts to separate the VCF header and body,
#then split the body based on chromosome number
filepathstep1 = os.path.join(script_directory, scriptExtractHead)
# output_directory = os.path.join(script_directory, outputFileStep01)
# print(filepath)

filepathstep2 = os.path.join(script_directory, scriptExtractBody)
# output_directory = os.path.join(script_directory, outputFileStep02)


filepathstep3 = os.path.join(script_directory, scriptSplitBody)
# output_directory = os.path.join(script_directory, outputFileStep03)

# print(output_directory)

subprocess.run(['python3', filepathstep1, output_directory ])
subprocess.run(['python3', filepathstep2, output_directory ])
subprocess.run(['python3', filepathstep3, output_directory ])



