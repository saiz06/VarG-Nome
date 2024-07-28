#connect to neo4j
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "sanna"

def connect_to_Neo4j_Database():
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver


