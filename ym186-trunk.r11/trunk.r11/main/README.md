# 1. Extract Chromosomes
Extract all chromosomes from file 'hs37d5.fa' by splitting the chromosomes to their individual .fa files using '1_extractFASTA.py'
# 2. Create nodes and relations of chromosomes
Each '.fa' file is loaded to script 'step_1.py' to generate two '.csv' files each for every chromosome
# 3. Split VCF files
Split the file 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.gz' to header and body using scripts, '5_get_VCF_head.py' and '6_get_VCF_body.py'
# 4. Extract VCFs
Extract all variations from 'body.vcf' by splitting the file to individual vcfs using the script '7_separate_vcf_body.py'
# 5. Create nodes and relations of variations
Each variation file 'vcf.csv' is loaded to script 'create_vcf_nodes.py'to get the following 7 files for each variation file: 'alt_alt_rel.csv', 'ref_alt_rel.csv', 'alt_nodes.csv', 'start_rel.csv', 'alt_ref_rel.csv', 'end_rel.csv', 'mutation_nodes.csv'
# 6. Apache Spark
Connect to Apache Spark and push the files generated from 2 and 5 to GraphX to get RDDs
# 7. Connect to Neo4j
Connect Apache Spark to Neo4j database
Get the resultant RDD files from Apache Spark and push them to Neo4j
