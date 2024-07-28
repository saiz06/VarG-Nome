from connectDB import connect_to_Neo4j_Database

count_variant_node_update=0
count_alt_nodes_deletes=0
count_new_alt_node_created=0
count_new_rel_created=0

#total_time_variant_node_update= 

def update_variant_nodes(tx, old_first, old_last, new_first, new_last):
    of = old_first
    ol = old_last
    nf = new_first -1
    nl = new_last+1
    
    tx.run(
        """
        MATCH (r:Reference) WHERE r.pos = $o_first
        MATCH (s:Reference) WHERE s.pos = $o_last
        MATCH (a:Reference) WHERE a.pos = $n_first
        MATCH (b:Reference) WHERE b.pos = $n_last
        WITH r, s, a, b
        MATCH (r)<-[f:FIRST]-(v:Variant)-[l:LAST]->(s)
        WITH v, f, l, a, b
        DELETE f, l
        WITH v, a, b
        MERGE (a)<-[:FIRST]-(v)-[:LAST]->(b)
        SET v.leftaligned="true"
        
        """ , o_first=of, o_last=ol, n_first=nf, n_last=nl)

def delete_alt_nodes(tx, alt_nodes_to_delete):
    for pos in alt_nodes_to_delete:
        tx.run(
            """
            MATCH (a:Alternate) WHERE a.pos = $p
            DETACH DELETE a
            """, p=pos)

def add_first_rel_in_extended_node(tx,first_position_alt_path, first_position_ref_path):
    tx.run(
        """
        MATCH (r:Reference) WHERE r.pos = $fr_pos
        MATCH (a:Alternate) WHERE a.pos = $fa_pos
        WITH r, a
        MERGE (r)-[:ALT]->(a)
        """, fr_pos=first_position_ref_path, fa_pos=first_position_alt_path)

def add_last_rel_in_trimmed_node(tx, last_position_alt_path, last_position_ref_path):
    tx.run("""
    MATCH (a:Alternate) WHERE a.pos = $la_pos
    MATCH (r:Reference) WHERE r.pos = $lr_pos
    WITH a, r
    MERGE (a)-[:ALT]->(r)
    """,la_pos=last_position_alt_path,lr_pos=last_position_ref_path)


def add_alt_node_to_empty_allele(tx,nuc_of_empty_allele, pos_of_empty_allele, last_position_ref_path ):
    f_pos = pos_of_empty_allele -1
    l_pos = last_position_ref_path + 1

    tx.run(
        """
        MATCH (a:Reference) WHERE a.pos = $f_ref_pos
        MATCH (b:Reference) WHERE b.pos = $l_ref_pos
        WITH a, b
        MERGE (a)-[:ALT]->(:Alternate{id:$nuc, pos:$pos})-[:ALT]->(b)
        """, f_ref_pos=f_pos, nuc=nuc_of_empty_allele, pos=pos_of_empty_allele, l_ref_pos=l_pos )


def normalize_graph(ref,alt):
    to_right_trim = True
    to_left_extend = False

    #flags to start sessions
    var_node_flag = False
    empty_node_flag = False
    extended_node_flag = False
    right_trim_flag = False

    #From Reference Path:
    last_node_ref_path = ref.nodes[-1]
    first_node_ref_path = ref.nodes[0]
    last_position_ref_path = last_node_ref_path["pos"]
    first_position_ref_path = first_node_ref_path["pos"]
    #for updating Var nodes:
    old_last_position_ref_path = last_node_ref_path["pos"]+1
    old_first_position_ref_path = first_node_ref_path["pos"]-1

    
    #From Alt Path:
    allele_length = len(alt)+1
    last_node_alt_path = alt.nodes[-1]
    first_node_alt_path = alt.nodes[0]
    last_position_alt_path = last_node_alt_path["pos"]
    first_position_alt_path = first_node_alt_path["pos"]
    alt_nodes_to_del_trimmed = []
    alt_nodes_to_del_extended = []
    nuc_of_empty_allele = ""
    pos_of_empty_allele=0
#     print("AT start: allele_length->",allele_length)

    #while right trim or left extend are true
    while to_right_trim or to_left_extend:
        #checks if right trimmable or left extendable
        to_right_trim = True
        to_left_extend = False

#         print("-------------F L A G S ----------------")

#         print("if first_position_alt_path (" ,first_position_alt_path, ")!=(",last_position_alt_path,") last_position_alt_path:")
        #this means allele has more than one node
        if first_position_alt_path != last_position_alt_path:
#             print("set to_right_trim to true")            
            to_right_trim = True
#             print("to_right_trim->", to_right_trim)
        else: #this means allele has only one node
#             print("above not true, so set extend to T")
            #to_right_trim = True
            
            to_left_extend = True
#             print("to_left_extend->", to_left_extend)
            #dont break here, we want to check if allele is empty or not

        #if allele is not empty
#         print("if allele is not empty, allele length->", allele_length)
        if allele_length>0:
#             print("set to_right_trim to true")
            to_right_trim = True
#             print("to_right_trim->", to_right_trim)
        #allele is empty
        else:
#             print("allele is empty, set left extend to true")
            to_left_extend = True
#             print("to_left_extend->", to_left_extend)

        #iterate over the ALT allele starting from last node:

        print("-------------T R I M ----------------")
        
        if to_right_trim:
#             print("RIGHT TRIM:")
            for alt_node in reversed(alt.nodes):
#                 print("iterate over alt path starting from last node")
                if alt_node["id"] == last_node_ref_path["id"]:
                    right_trim_flag = True
#                     print("--nucleotides match--")
#                     print("alt_id->",alt_node["id"], "and ref_id->",last_node_ref_path["id"])
#                     print("alt_pos->",alt_node["pos"], "and ref_id->",last_node_ref_path["pos"])
                    
                    last_position_ref_path = last_position_ref_path -1
#                     print("update last ref pos from ",last_position_ref_path+1,"to ",last_position_ref_path)
                      
                    #set new last ref node
                    for ref_node in ref.nodes:
                        if ref_node["pos"]==last_position_ref_path:
                            last_node_ref_path = ref_node
#                     print("last ref node->",last_node_ref_path)
                    
                    alt_nodes_to_del_trimmed.append(last_position_alt_path)
#                     print("DELTE NODE->",last_position_alt_path)
                    
                    #change last position of alt path
                    last_position_alt_path = last_position_alt_path - 1
                    #set new last alt node
                    for alt_node in alt.nodes:
                      if alt_node["pos"]==last_position_alt_path:
                        last_node_alt_path =   alt_node
#                     print("new last alt node->",last_node_alt_path)
                    
                    
                    allele_length = allele_length -1
#                     print("allele len reduced here->",allele_length)
                    
                else:
#                     print("nuc bases not same, set right trim to false")
                    to_right_trim = False
                    to_left_extend = True
                    
#                     print("to_right_trim->", to_right_trim)
#                     print("to_left_extend->",to_left_extend)

#                     print("check if allele len == 1")
#                     print("allele len->",allele_length)
                    if allele_length==1:
#                         print("allele len is 1, set right trim to F")
                        to_right_trim = False
#                         print("to_right_trim->", to_right_trim)
#                 print("check if allele len == 0 i.e. empty allele")
#                 print("allele len->",allele_length)
                if allele_length == 0: #(allele is empty)
#                     print("allele is empty, set right trim to F and left extend to T")
                    to_right_trim=False
                    to_left_extend=True
#                     print("to_right_trim->", to_right_trim)
#                     print("to_left_extend->", to_left_extend)

        print("------------- E X T E N D ----------------")
        if to_left_extend:
#             print("check if allele len > 0 i.e. allele is not empty")
#             print("allele len->",allele_length)

            if allele_length>0:#allele is not empty and has atleast one node
                to_left_extend = True
#                 print("allele is not empty, compare nuc bases")
#                 print("set left extend to true->", to_left_extend)
                
                for alt_node in alt.nodes:
#                     print("iterating over alt nodes")
                    if allele_length>0:
#                         print("Allele is not empty so:")
#                         print("ref node->", first_node_ref_path)
#                         print("alt node->", alt_node)
#                         print("allele_length->", allele_length)
                        first_position_ref_path = alt_node["pos"]
#                         print("alt_node[id]->", alt_node["id"], "ref_node[id]", first_node_ref_path["id"])
#                         print("alt_node[pos]->", alt_node["pos"], "ref_node[pos]", first_node_ref_path["pos"])
                        if alt_node["id"]==first_node_ref_path["id"]:
#                             print("Nuc bases are same, trim here")
                            alt_nodes_to_del_extended.append(alt_node["pos"])
                            first_position_alt_path = first_node_alt_path["pos"] + 1
                            allele_length = allele_length-1
#                             print("del first alt, alle len->", allele_length)
                            for ref_node in ref.nodes:
                                if ref_node["pos"] ==alt_node["pos"]+1 and allele_length>0:
                                    first_node_ref_path = ref_node
                                    
                            #set this in the loop: first_position_alt_path = first_node_alt_path["pos"]
                            for alt_node in alt.nodes:
                                if alt_node["pos"]==first_position_alt_path:
                                    first_node_alt_path = alt_node
                                    
                        else: #nuc bases not same
#                             print("***************bases not same, set left_extend to false")
                            extended_node_flag = True
                            to_left_extend = False
#                             print("left_extend->",to_left_extend)
                        
            if allele_length == 0:
                empty_node_flag = True
#                 print("last pos ref node->",last_position_ref_path)
#                 print("first node ref->",first_node_ref_path)
                nuc_of_empty_allele=first_node_ref_path["id"]
                pos_of_empty_allele= first_node_ref_path["pos"]
#                 print("create new node->", nuc_of_empty_allele, pos_of_empty_allele, last_position_ref_path)

#                 print("set left extend to F")
                to_left_extend=False
#         print("to_left_extend->", to_left_extend, "to_right_trim->",to_right_trim)
        if to_left_extend==False and to_right_trim==False:
            var_node_flag = True
    #end while loop

#     print("-------- V A R - C O L L E C T I O N----------")
#     print("---First Ref---")
#     print("old-first ref pos->",old_first_position_ref_path)
#     print("first pos ref node->", first_position_ref_path)
#     print("new first ref node->", first_node_ref_path)
#     print("---Last Ref---")
#     print("old_last ref pos->",old_last_position_ref_path)
#     print("last pos ref node->", last_position_ref_path)
#     print("new last ref node->", last_node_ref_path)
    
#     print ("---trimmed alt nodes to delete:---")
#     for a in alt_nodes_to_del_trimmed:
#         print(a)
        
#     print ("---extdended alt nodes to delete:---")
#     for a in alt_nodes_to_del_extended:
#         print(a)
    
#     print("first ref node:->", first_node_ref_path)

#     #first_position_ref_path = first_node_ref_path["pos"]

    
#         #print("new_first alt node->",first_position_ref_path)
#     #print("new_last alt node>",last_position_ref_path)

    print("----------- S E S S I O N S ------------")
    d = connect_to_Neo4j_Database()
    with d.session() as s:
        if right_trim_flag:
            #Delete alt nodes
            s.write_transaction(delete_alt_nodes,alt_nodes_to_del_trimmed)
            #make last rel
            actual_lr_position = last_position_ref_path +1
            s.write_transaction(add_last_rel_in_trimmed_node, last_position_alt_path, actual_lr_position)
            
            
        if empty_node_flag:
            #Delete alt nodes
            s.write_transaction(delete_alt_nodes,alt_nodes_to_del_extended)
            s.write_transaction(delete_alt_nodes,alt_nodes_to_del_trimmed)
            #Add new node + its rels
            s.write_transaction(add_alt_node_to_empty_allele, nuc_of_empty_allele, pos_of_empty_allele, last_position_ref_path )
            
        if extended_node_flag:
            actual_fr_position = first_position_ref_path - 1
            #Delete alt nodes
            s.write_transaction(delete_alt_nodes,alt_nodes_to_del_extended)
            #create rel between first alt node and ref path
            s.write_transaction(add_first_rel_in_extended_node,first_position_alt_path, actual_fr_position)
        
        #update var node        
        if var_node_flag:
            s.write_transaction(update_variant_nodes, old_first_position_ref_path, old_last_position_ref_path, first_position_ref_path, last_position_ref_path)       
        
