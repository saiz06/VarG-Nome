import os
from fastapi import FastAPI, UploadFile, File
import uvicorn
import shutil
from extractFASTA import extractFASTA_func
from step_1 import nodes_rels_of_chromosomes
from get_VCF_head import split_vcf_header
from get_VCF_body import split_vcf_body
from separate_vcf_body import extract_varaiations_from_body_vcf
from to_rdd import Extract
from pandas_combine import combine
import time
import ray

#spark stuff
from pyspark.sql import SparkSession
import pyspark.sql.functions as fn
from pyspark.sql.types import StringType, StructField, StructType, ArrayType, LongType
from graphframes import *
import json

spark = (
    SparkSession.builder.appName("pipeline-processor")
    .master('local[*]')
    .getOrCreate()
    )

extract_obj = Extract(spark)

app = FastAPI()
BASE_PATH = os.path.dirname(__file__)

@app.get("/")
def root():
    return {"Message": "Welcome to the data preprocessing pipeline"}


@app.post("/preprocess")
def extractall(fa_file: UploadFile=File(...), all_wgs_file: UploadFile=File(...), BASE_PATH=BASE_PATH):
    try:
        with open(os.path.join(BASE_PATH, fa_file.filename), "wb") as fa:
            shutil.copyfileobj(fa_file.file, fa)

        with open(os.path.join(BASE_PATH, all_wgs_file.filename), "wb") as fa:
            shutil.copyfileobj(all_wgs_file.file, fa)
    finally:
        fa_file.file.close()
        all_wgs_file.close()
    extractFASTA_func.remote(BASE_PATH, fa_file.filename)
    nodes_rels_of_chromosomes.remote(BASE_PATH, fa_file.filename)
    combine.remote(BASE_PATH, fa_file.filename)
    split_vcf_body.remote(BASE_PATH, all_wgs_file.filename)
    split_vcf_header.remote(BASE_PATH, all_wgs_file.filename)
    time.sleep(10)
    extract_varaiations_from_body_vcf.remote(BASE_PATH, 'vcf_header_and_body')
    time.sleep(10)
    for file in os.listdir(os.path.join(BASE_PATH, 'hs37d5_nodes_rel_chromes')):
        if file.split("_")[0] == "nodes":
            node_data = extract_obj.nodes_to_rdd(BASE_PATH, file)
            extract_obj.write_to_neo(node_data)
    #     else:
    #         edge_data = extract_obj.edges_to_rdd(BASE_PATH, file)
    #         extract_obj.write_to_neo(edge_data)
    return {"Message": "Processing completed successfully"}


if __name__ == '__main__':
    ray.init()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")