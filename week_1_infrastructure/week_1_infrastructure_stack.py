from aws_cdk import (
    Stack,
    Duration,               # Required for retention settings
    RemovalPolicy,          # Required for cleanup
    CfnOutput,              # Required to output the StreamName
    aws_s3 as s3,
    aws_kms as kms,
    aws_kinesis as kinesis, # <--- Vital: Imports Kinesis from the core v2 lib
)
from constructs import Construct

class Week1InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- 1. KMS Key ---
        data_key = kms.Key(self, "DataKey",
            description="KMS Key for Data Engineering Lab Week 1",
            enable_key_rotation=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        # --- 2. S3 Bucket ---
        data_bucket = s3.Bucket(self, "RawDataBucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=data_key,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # --- 3. Kinesis Data Stream ---
        stream = kinesis.Stream(self, "InputStream",
            stream_name="week-1-lab-stream",
            shard_count=1,
            retention_period=Duration.hours(24),
            removal_policy=RemovalPolicy.DESTROY
        )

        # --- 4. Outputs ---
        CfnOutput(self, "BucketName", value=data_bucket.bucket_name)
        CfnOutput(self, "StreamName", value=stream.stream_name)