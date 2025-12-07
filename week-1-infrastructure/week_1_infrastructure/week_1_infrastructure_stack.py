from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    CfnOutput,
    aws_s3 as s3,
    aws_kms as kms,
    aws_kinesis as kinesis,
    aws_lambda as _lambda,               # Consumer Resource
    aws_lambda_event_sources as events,  # Trigger Configuration
)
from constructs import Construct

class Week1InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- 1. KMS Key (Security) ---
        data_key = kms.Key(self, "DataKey",
            description="KMS Key for Data Engineering Lab Week 1",
            enable_key_rotation=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        # --- 2. S3 Bucket (Storage) ---
        data_bucket = s3.Bucket(self, "RawDataBucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=data_key,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # --- 3. Kinesis Data Stream (Ingestion) ---
        stream = kinesis.Stream(self, "InputStream",
            stream_name="week-1-lab-stream",
            shard_count=1,
            retention_period=Duration.hours(24),
            removal_policy=RemovalPolicy.DESTROY
        )

        # --- 4. Lambda Consumer (Compute) ---
        # This defines the function resource
        consumer_fn = _lambda.Function(self, "KinesisConsumer",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="consumer.handler",
            code=_lambda.Code.from_asset("lambda"), # Looks for the 'lambda' folder
            timeout=Duration.seconds(60),
            environment={
                "BUCKET_NAME": data_bucket.bucket_name
            }
        )

        # --- 5. Event Source Mapping (Trigger) ---
        # This connects Kinesis to Lambda
        consumer_fn.add_event_source(events.KinesisEventSource(stream,
            batch_size=100,
            starting_position=_lambda.StartingPosition.TRIM_HORIZON
        ))

        # --- 6. Outputs ---
        CfnOutput(self, "BucketName", value=data_bucket.bucket_name)
        CfnOutput(self, "StreamName", value=stream.stream_name)
        CfnOutput(self, "LambdaName", value=consumer_fn.function_name)