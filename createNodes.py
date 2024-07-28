#Imports
from connectDB import connect_to_Neo4j_Database
from nodes import addChromosomeNode, addReferenceNode, addAlternateNode
#from neo4j import GraphDatabase

#Connect to DB
driver = connect_to_Neo4j_Database()

#Add Nodes using session and write transactions
with driver.session() as session:
    session.write_transaction(addChromosomeNode,1)
    
    session.write_transaction(addReferenceNode, 1, 1, 'G')
    session.write_transaction(addReferenceNode, 2, 1, 'G')
    session.write_transaction(addReferenceNode, 3, 1, 'G')
    session.write_transaction(addReferenceNode, 4, 1, 'G')
    session.write_transaction(addReferenceNode, 5, 1, 'C')
    session.write_transaction(addReferenceNode, 6, 1, 'A')
    session.write_transaction(addReferenceNode, 7, 1, 'T')
    session.write_transaction(addReferenceNode, 8, 1, 'G')
    session.write_transaction(addReferenceNode, 9, 1, 'G')
    session.write_transaction(addReferenceNode, 10, 1, 'G')
    session.write_transaction(addReferenceNode, 11, 1, 'G')
    session.write_transaction(addReferenceNode, 12, 1, 'T')
    session.write_transaction(addReferenceNode, 13, 1, 'T')
    session.write_transaction(addReferenceNode, 14, 1, 'G')
    session.write_transaction(addReferenceNode, 15, 1, 'T')
    session.write_transaction(addReferenceNode, 16, 1, 'G')
    session.write_transaction(addReferenceNode, 17, 1, 'C')
    session.write_transaction(addReferenceNode, 18, 1, 'A')
    session.write_transaction(addReferenceNode, 19, 1, 'C')
    session.write_transaction(addReferenceNode, 20, 1, 'T')
    session.write_transaction(addReferenceNode, 21, 1, 'G')
    session.write_transaction(addReferenceNode, 22, 1, 'C')
    session.write_transaction(addReferenceNode, 23, 1, 'T')
    session.write_transaction(addReferenceNode, 24, 1, 'G')
    session.write_transaction(addReferenceNode, 25, 1, 'C')
    session.write_transaction(addReferenceNode, 26, 1, 'A')
    session.write_transaction(addReferenceNode, 27, 1, 'T')    
    session.write_transaction(addReferenceNode, 28, 1, 'G')
    session.write_transaction(addReferenceNode, 29, 1, 'G')
    session.write_transaction(addReferenceNode, 30, 1, 'G')
    session.write_transaction(addReferenceNode, 31, 1, 'C')
    session.write_transaction(addReferenceNode, 32, 1, 'A')
    session.write_transaction(addReferenceNode, 33, 1, 'T')

    session.write_transaction(addReferenceNode, 34, 1, 'G')
    session.write_transaction(addReferenceNode, 35, 1, 'G')
    session.write_transaction(addReferenceNode, 36, 1, 'G')    
    session.write_transaction(addReferenceNode, 37, 1, 'C')
    session.write_transaction(addReferenceNode, 38, 1, 'A')
    session.write_transaction(addReferenceNode, 39, 1, 'C')
    session.write_transaction(addReferenceNode, 40, 1, 'A')
    session.write_transaction(addReferenceNode, 41, 1, 'C')
    session.write_transaction(addReferenceNode, 42, 1, 'A')
    session.write_transaction(addReferenceNode, 43, 1, 'C')
    session.write_transaction(addReferenceNode, 44, 1, 'A')
    session.write_transaction(addReferenceNode, 45, 1, 'G')
    session.write_transaction(addReferenceNode, 46, 1, 'G')
    session.write_transaction(addReferenceNode, 47, 1, 'G')
    session.write_transaction(addReferenceNode, 48, 1, 'T')
    
    session.write_transaction(addAlternateNode, 14, 'G')
    session.write_transaction(addAlternateNode, 18, 'A')
    session.write_transaction(addAlternateNode, 19, 'C')
    session.write_transaction(addAlternateNode, 20, 'A')
    session.write_transaction(addAlternateNode, 28, 'A')

    session.write_transaction(addAlternateNode, 34, 'G')
    session.write_transaction(addAlternateNode, 35, 'G')
    session.write_transaction(addAlternateNode, 36, 'G')
    session.write_transaction(addAlternateNode, 37, 'C')
    session.write_transaction(addAlternateNode, 38, 'A')
    session.write_transaction(addAlternateNode, 39, 'C')
    session.write_transaction(addAlternateNode, 40, 'A')
    session.write_transaction(addAlternateNode, 41, 'C')
    session.write_transaction(addAlternateNode, 42, 'A')
    session.write_transaction(addAlternateNode, 43, 'G')
    session.write_transaction(addAlternateNode, 44, 'G')
    session.write_transaction(addAlternateNode, 45, 'G')
    
driver.close()

#Add Reference Nodes





