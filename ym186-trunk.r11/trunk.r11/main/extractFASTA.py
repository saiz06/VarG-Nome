################################################################
#
#		SPLIT FILE to individual .fa
#
####################((B.O.D.Y))################################
import  re
import os
import ray


@ray.remote
def extractFASTA_func(BASE_PATH, fa_file):
    fa_file_file_path = os.path.join(BASE_PATH, f'{fa_file}'.split('.')[0]+f'_fas')
    try:
        os.mkdir(fa_file_file_path)
    except FileExistsError:
        print("Folder Already exists")

    file_variable = ""

    file = open(os.path.join(BASE_PATH, fa_file), 'r+')
    inputfasta = file.readlines()
    file.close()

    #read file line by line
    for line in inputfasta:
        #find start line
        if re.findall ('>', line):
            g = re.findall('>(.+?)\s',line)
            chrno = str(g).strip('[\']')
            fname = "Ref_Chr_"+chrno+".fa"
            file_variable = "Chr"+chrno
            file_variable = open(os.path.join(fa_file_file_path, fname),"w")
            file_variable.write(line)
        else:
            line = line.rstrip()
            file_variable.write(line)

if __name__=='__main__':
    futures = extractFASTA_func.remote('/Users/lawrence/Documents/Lawrence/data-api', 'hs37d5.fa')
    ray.get(futures)

