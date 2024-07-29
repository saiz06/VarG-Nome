cd extract

copy input data file here

python vcfExtraction.py


GenerateSessionFASTA.py

Generates python scripts which connect to neo4j and populate the database with chromosome and reference nodes. These files will appear in the populate folder.

To populate Reference Genome:

cd populate
./run_all_scripts.sh
