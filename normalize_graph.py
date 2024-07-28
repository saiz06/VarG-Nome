from connectDB import connect_to_Neo4j_Database
from update_graph import normalize_graph



def query(tx, query_, **params):
    result = tx.run(query_,params)
    return list(result)



def main():
    print("Entering function main")
    #Connect to DB
    d = connect_to_Neo4j_Database()
    
    with d.session() as s:
        ref_path = s.read_transaction(
            query,
            """
            MATCH (v:Variant) WHERE v.leftaligned=false
            MATCH (a:Reference)<-[:FIRST]-(v)-[:LAST]->(b:Reference)
            WITH a,b
            MATCH path = (a)-[:NEXT*]->(b)
            WITH apoc.path.slice(path, 1, length(path)-2) as refPath
            RETURN refPath
            """
            )
        #assert len(path1)== 0 or print(path1)
        #path1[0]["path"]
        
    with d.session() as s:
        alt_path = s.read_transaction(
            query,
            """
            MATCH (v:Variant) WHERE v.leftaligned=false
            MATCH (r:Reference)<-[:FIRST]-(v)-[:LAST]->(s:Reference)
            WITH r, s
            MATCH path = (r)-[:ALT*]->(s)
            WITH apoc.path.slice(path, 1, length(path)-2) as altPath
            RETURN altPath
            """
            )
        #assert len(path2)== 0 or print(path2)
        #path2 = path2[0]["path"] #convert list to nodes??
        for i in range(0,len(alt_path)):
            print(i)
            alt_path_test=alt_path[i]["altPath"]
            ref_path_test=ref_path[i]["refPath"]
            print("ALT")
            print(alt_path_test)
            print(type(alt_path_test))
            print("REF")
            print(ref_path_test)
            print(type(ref_path_test))      
    
            normalize_graph(ref_path_test, alt_path_test)

if __name__ == "__main__":
    main()
