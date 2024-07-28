
#Imports
from connectDB import connect_to_Neo4j_Database
from relationships import addRel_NEXT, addRel_ALT, addRel_startALT, addRel_endALT
#from neo4j import GraphDatabase

#Connect to DB
driver = connect_to_Neo4j_Database()


with driver.session() as session:      
    
    session.write_transaction(addRel_NEXT, 1, 2, 1, 1)
    session.write_transaction(addRel_NEXT, 2, 3, 1, 1)
    session.write_transaction(addRel_NEXT, 3, 4, 1, 1)
    session.write_transaction(addRel_NEXT, 4, 5, 1, 1)
    session.write_transaction(addRel_NEXT, 5, 6, 1, 1)
    session.write_transaction(addRel_NEXT, 6, 7, 1, 1)
    session.write_transaction(addRel_NEXT, 7, 8, 1, 1)
    session.write_transaction(addRel_NEXT, 8, 9, 1, 1)
    session.write_transaction(addRel_NEXT, 9, 10, 1, 1)
    session.write_transaction(addRel_NEXT, 10, 11, 1, 1)
    session.write_transaction(addRel_NEXT, 11, 12, 1, 1)
    session.write_transaction(addRel_NEXT, 12, 13, 1, 1)    
    session.write_transaction(addRel_NEXT, 13, 14, 1, 1)
    session.write_transaction(addRel_NEXT, 14, 15, 1, 1)
    session.write_transaction(addRel_NEXT, 15, 16, 1, 1)
    session.write_transaction(addRel_NEXT, 16, 17, 1, 1)
    session.write_transaction(addRel_NEXT, 17, 18, 1, 1)
    session.write_transaction(addRel_NEXT, 18, 19, 1, 1)
    session.write_transaction(addRel_NEXT, 19, 20, 1, 1)
    session.write_transaction(addRel_NEXT, 20, 21, 1, 1)
    session.write_transaction(addRel_NEXT, 21, 22, 1, 1)
    session.write_transaction(addRel_NEXT, 22, 23, 1, 1)
    session.write_transaction(addRel_NEXT, 23, 24, 1, 1)
    session.write_transaction(addRel_NEXT, 24, 25, 1, 1)
    session.write_transaction(addRel_NEXT, 25, 26, 1, 1)    
    session.write_transaction(addRel_NEXT, 26, 27, 1, 1)
    session.write_transaction(addRel_NEXT, 27, 28, 1, 1)
    session.write_transaction(addRel_NEXT, 28, 29, 1, 1)
    session.write_transaction(addRel_NEXT, 29, 30, 1, 1)

    session.write_transaction(addRel_NEXT, 30, 31, 1, 1)
    session.write_transaction(addRel_NEXT, 31, 32, 1, 1)
    session.write_transaction(addRel_NEXT, 32, 33, 1, 1)
    session.write_transaction(addRel_NEXT, 33, 34, 1, 1)
    session.write_transaction(addRel_NEXT, 34, 35, 1, 1)
    session.write_transaction(addRel_NEXT, 35, 36, 1, 1)
    session.write_transaction(addRel_NEXT, 36, 37, 1, 1)
    session.write_transaction(addRel_NEXT, 37, 38, 1, 1)
    session.write_transaction(addRel_NEXT, 38, 39, 1, 1)
    session.write_transaction(addRel_NEXT, 39, 40, 1, 1)
    session.write_transaction(addRel_NEXT, 40, 41, 1, 1)
    session.write_transaction(addRel_NEXT, 41, 42, 1, 1)
    session.write_transaction(addRel_NEXT, 42, 43, 1, 1)
    session.write_transaction(addRel_NEXT, 43, 44, 1, 1)
    session.write_transaction(addRel_NEXT, 44, 45, 1, 1)
    session.write_transaction(addRel_NEXT, 45, 46, 1, 1)
    session.write_transaction(addRel_NEXT, 46, 47, 1, 1)
    session.write_transaction(addRel_NEXT, 47, 48, 1, 1)

    session.write_transaction(addRel_startALT, 13, 14, 1)
    session.write_transaction(addRel_startALT, 17, 18, 1)
    session.write_transaction(addRel_startALT, 27, 28, 1)

    session.write_transaction(addRel_endALT, 14, 17, 1)
    session.write_transaction(addRel_endALT, 20, 21, 1)
    session.write_transaction(addRel_endALT, 28, 29, 1)

    session.write_transaction(addRel_ALT, 18, 19)
    session.write_transaction(addRel_ALT, 19, 20)

    session.write_transaction(addRel_startALT, 33, 34, 1)
    session.write_transaction(addRel_ALT, 34, 35)
    session.write_transaction(addRel_ALT, 35, 36)
    session.write_transaction(addRel_ALT, 36, 37)
    session.write_transaction(addRel_ALT, 37, 38)
    session.write_transaction(addRel_ALT, 38, 39)
    session.write_transaction(addRel_ALT, 39, 40)
    session.write_transaction(addRel_ALT, 40, 41)
    session.write_transaction(addRel_ALT, 41, 42)
    session.write_transaction(addRel_ALT, 42, 43)
    session.write_transaction(addRel_ALT, 43, 44)
    session.write_transaction(addRel_ALT, 44, 45)
    session.write_transaction(addRel_endALT, 45, 48, 1)    

           
driver.close()




