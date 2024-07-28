# CREATE VARIANT NODES



from connectDB import connect_to_Neo4j_Database
#from neo4j import GraphDatabase

#Connect to DB
driver = connect_to_Neo4j_Database()

with driver.session() as session:  
    session.write_transaction(addVariantNodes)
driver.close()




