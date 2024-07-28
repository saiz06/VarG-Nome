import os
from graphframes import *
import pyspark.sql.functions as fn



class Extract():
    def __init__(self, sc):
        self.sc = sc

    def nodes_to_rdd(self, BASE_PATH, file_path):
        df=self.sc.read.format("csv").option("header","true").option("inferSchema", "true").load(os.path.join(f"/hs37d5_nodes_rel_chromes", file_path))
        # Vertex DataFrame
        node_data=df.withColumn("Property",fn.concat(fn.col("pos"),fn.lit(','),fn.col("RefGenome"),fn.lit(','),fn.col("chrom"),fn.lit(','),fn.col("ref"))).drop("pos").drop("RefGenome").drop("chrom").drop("ref").drop("LABEL")
        return node_data
    
    # def edges_to_rdd(self, BASE_PATH, file_path):
    #     edge_df=self.sc.read.format("csv").option("header","true").option("inferSchema", "true").load(os.path.join(f"/hs37d5_nodes_rel_chromes", file_path))
    #     # Vertex DataFrame
    #     edge_rdd=edge_df.select(fn.col("START_ID(Ref-ID)"), fn.col("END_ID(Ref-ID)")).distinct()
    #     return edge_rdd

    def write_to_neo(self, df):
        df.repartition(1).write \
            .format("org.neo4j.spark.DataSource") \
            .mode("Append") \
            .option("url", "neo4j+s://fafa72d4.databases.neo4j.io") \
            .option("authentication.basic.username", "neo4j")\
            .option("authentication.basic.password", "oFoD65J-2T1WNET3VfFLuOWa-sO8fy6LEISbj6_QxhA")\
            .option("relationship", "CHROMOSOMES") \
            .option("relationship.properties", "Property") \
            .option("relationship.save.strategy", "keys") \
            .option("relationship.source.labels", ":START_ID(Ref-ID)") \
            .option("relationship.source.node.keys", "START_ID(Ref-ID):id") \
            .option("relationship.source.save.mode", "overwrite") \
            .option("relationship.target.labels", ":END_ID(Ref-ID)") \
            .option("relationship.target.nodes.keys", "END_ID(Ref-ID):id") \
            .option("relationship.target.save.mode", "overwrite") \
            .save()