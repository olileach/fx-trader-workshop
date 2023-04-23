import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql import DataFrame, Row
import datetime
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Kinesis Stream
dataframe_KinesisStream_node1 = glueContext.create_data_frame.from_options(
    connection_type="kinesis",
    connection_options={
        "typeOfData": "kinesis",
        "streamARN": "arn:aws:kinesis:{region_name}:{account_id}:stream/fx-trades-stream",
        "classification": "json",
        "startingPosition": "earliest",
        "inferSchema": "true",
    },
    transformation_ctx="dataframe_KinesisStream_node1",
)


def processBatch(data_frame, batchId):
    if data_frame.count() > 0:
        KinesisStream_node1 = DynamicFrame.fromDF(
            glueContext.add_ingestion_time_columns(data_frame, "hour"),
            glueContext,
            "from_data_frame",
        )
        # Script generated for node S3 bucket
        S3bucket_node3_path = (
            "s3://fx-trader-{account_id}-{region_name}-bucket/fx-trader-example/parquet/"
        )
        S3bucket_node3 = glueContext.getSink(
            path=S3bucket_node3_path,
            connection_type="s3",
            updateBehavior="UPDATE_IN_DATABASE",
            partitionKeys=["ingest_year", "ingest_month", "ingest_day", "ingest_hour"],
            compression="gzip",
            enableUpdateCatalog=True,
            transformation_ctx="S3bucket_node3",
        )
        S3bucket_node3.setCatalogInfo(
            catalogDatabase="fx_trader_database", catalogTableName="trades"
        )
        S3bucket_node3.setFormat("glueparquet")
        S3bucket_node3.writeFrame(KinesisStream_node1)


glueContext.forEachBatch(
    frame=dataframe_KinesisStream_node1,
    batch_function=processBatch,
    options={
        "windowSize": "20 seconds",
        "checkpointLocation": args["TempDir"] + "/checkpoint/",
    },
)
job.commit()
