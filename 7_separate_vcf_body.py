###############################################################
#               VCF FILE
#               input: VCF body file generated from get_VCF_body.py
#               output: VCF body separated for each CHR
#
####################((B.O.D.Y))################################
import re
import os #used with strip(os.linesep)
import gzip


#Save to these files:
counter = open("vcf_chr_record_count.txt","w")

file_variable=""
prev_chr=""
chrom_list = []#contains names of chr
chrom_file_list = [] #contains names of files to be created
var_counter = 0
#print("counter is 0")

#flag 
new_chr_flag = 0
first_line_flag = 0
end_of_file_flag = 0

with open('vcf_body.vcf', 'r+') as inputvcf:
#with open('sample.txt', 'r+') as inputvcf:
        for line in inputvcf:
		chrom_var = line.split()[0]
		
		if not chrom_list:#empty list
			first_flag=1


		#found unique chr:
		if chrom_var not in chrom_list:				
			
			if first_flag == 1:#list empty
				#print("first line of file")
				end_of_file_flag = 0
				first_flag = 0
				
			else:#list not empty
				end_of_file_flag = 1
				#var_counter = 0
				#print("****count  "+str(var_counter))
				if var_counter<2:#only 1 line
					#print("write count to file:")
					#print(chrom_var+"   "+str(var_counter))
					counter.write(chrom_var)
					counter.write("\t")
					counter.write(str(var_counter))
					counter.write("\n")
					#print("reset count")				
					var_counter = 0
				
				else: #more than one line
					#print("write count to file:")
					#print(prev_chr+"   "+str(var_counter))
					counter.write(prev_chr)
					counter.write("\t")
					counter.write(str(var_counter))
					counter.write("\n")
					#print("reset count")				
					var_counter = 0
					
			chrom_list.append(chrom_var)
			fname = "VCF_Chr"+chrom_var+"_body.csv"
			file_variable = "Chr"+chrom_var
			file_variable = open(fname,"w")
			#print("file opened with name: "+fname)
			
			#print("====Start of chr#: "+chrom_var)
			file_variable.write(str(line))
			var_counter += 1
			#print("count: "+str(var_counter))
			
			
		
		
		#not unique
		else:
			prev_chr = chrom_var
			#print("====At chr#: "+chrom_var)
			file_variable.write(str(line))
			var_counter += 1
			#print("count: "+str(var_counter))
		#
		
			
			
			 
			
		
			

