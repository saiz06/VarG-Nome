#Functions to Create nodes in Neo4j


def addChromosomeNode(tx, chrno):
    tx.run("MERGE (c:Chromosome {id: $number})", number=chrno)

def addReferenceNode(tx, position, chrno, nucleotide):
    tx.run("MERGE (r:Reference{pos : $pos , chr : $number , id : $nuc})", pos = position, number=chrno, nuc=nucleotide)

def addAlternateNode(tx, position, nucleotide):
    tx.run("MERGE (a:Alternate{pos : $pos ,  id : $nuc})", pos = position, nuc=nucleotide)

def addVariantNodes(tx):
    tx.run(
        """
        MATCH path = (first:Reference)-[:ALT*]->(last:Reference)
        WHERE size([i in nodes(path) WHERE i:Reference]) = 2

        WITH first, last, path
        MATCH (first)-[:ALT]->(firstAltNode:Alternate)
        MATCH (last)<-[:ALT]-(lastAltNode:Alternate)

        WITH first, last, firstAltNode, lastAltNode, length(path)-1 AS lengthAltPath, last.pos-first.pos-1 AS lengthRefPath
        MERGE (last)<-[:LAST]-(v:Variant)-[:FIRST]->(first)
        ON CREATE SET v.first = first.pos, v.last =last.pos, v.leftaligned=false, v.name ="Variant", v.posOfFirstNodeRefPath = first.pos+1, v.posOfLastNodeRefPath = last.pos-1, v.posOfFirstNodeAltPath = firstAltNode.pos, v.posOfLastNodeAltPath=lastAltNode.pos, v.altPathLength=lengthAltPath, v.refPathLength=lengthRefPath

        """)

