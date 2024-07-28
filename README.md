# VarG-Nome

Start with blank DB

run files in the following order:

1.createNodes.py
2.createRels.py
3.createVars.py
4.normaliza_graph.py (or .ipynb in jupyter notebook)

-------------------------------------------------------------------------
Functions is other files:
-------------------------------------------------------------------------
connectDB.py
└── connect_to_Neo4j_Database -->(change uri/username/password here)

nodes.py
├── addChromosomeNode
├── addReferenceNode
├── addAlternateNode
└── addVariantNodes

relationships.py
├── addRel_NEXT
├── addRel_ALT
├── addRel_startALT
└── addRel_endALT

update_graph.py
├── update_variant_nodes
├── delete_alt_nodes
├── add_first_rel_in_extended_node
├── add_last_rel_in_trimmed_node
├── add_alt_node_to_empty_allele
└── normalize_graph
