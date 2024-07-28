import pandas as pd
import os
import ray

@ray.remote
def combine(BASE_PATH, RefGenome):
    nodes_path = os.path.join(BASE_PATH, f'{RefGenome}'.split('.')[0]+f'nodes')
    edges_path = os.path.join(BASE_PATH, f'{RefGenome}'.split('.')[0]+f'edges')
    # edges_path=os.path.join(BASE_PATH, edges_folder)
    # nodes_path=os.path.join(BASE_PATH, nodes_folder)

    # Create a new folder to store generated chromosomes nodes and relationships CSV
    nodes_rel_chromes_path = os.path.join(BASE_PATH, f'{RefGenome}'.split('.')[0]+f'_nodes_rel_chromes')
    try:
        os.mkdir(nodes_rel_chromes_path)
    except FileExistsError:
        print("Folder Already exists")

    edges_files = os.listdir(edges_path)
    nodes_files = os.listdir(nodes_path)
    for node in nodes_files:
        for edge in edges_files:
            if node.split('_')[4] == edge.split('_')[4]:
                node_df = pd.read_csv(os.path.join(nodes_path,node))
                edge_df = pd.read_csv(os.path.join(edges_path,edge))
                gen_df = pd.concat([node_df, edge_df], axis=1)
                gen_df.to_csv(os.path.join(nodes_rel_chromes_path,f"{node}{edge}.csv"), index=False)


if __name__ == "__main__":
    BASE_PATH = os.path.dirname(__file__)
    combine(BASE_PATH, "hs37d5.fa")