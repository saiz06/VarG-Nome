#functions to add relationships

def addRel_NEXT(tx, pos1, pos2, chr1, chr2):
    tx.run("""
        MATCH (x:Reference) WHERE (x.pos = $startPos) AND (x.chr = $startChr)
        MATCH (y:Reference) WHERE (y.pos = $endPos) AND (y.chr = $endChr)
        WITH x , y
        MERGE (x)-[:NEXT]->(y)
        """
        ,startPos=pos1, startChr=chr1, endPos=pos2, endChr=chr2)

def addRel_ALT(tx, pos1, pos2):
    tx.run("""
        MATCH (a:Alternate) WHERE (a.pos = $firstPos)
        MATCH (b:Alternate) WHERE (b.pos = $secondPos)
        
        MERGE (a)-[:ALT]->(b)
        """,firstPos=pos1,secondPos=pos2)

def addRel_startALT(tx, pos1, pos2, chrno):
    tx.run("""
        MATCH (a:Reference) WHERE (a.pos = $firstPos) AND (a.chr = $number)
        MATCH (b:Alternate) WHERE (b.pos = $secondPos)
        
        MERGE (a)-[:ALT]->(b)
        """, firstPos=pos1,secondPos=pos2,number=chrno)


def addRel_endALT(tx, pos1, pos2, chrno):
    tx.run("""
        MATCH (a:Alternate) WHERE (a.pos = $firstPos)
        MATCH (b:Reference) WHERE (b.pos = $secondPos) AND (b.chr = $number)
        MERGE (a)-[:ALT]->(b)
        """, firstPos=pos1,secondPos=pos2,number=chrno)

