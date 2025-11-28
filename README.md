# Week 1: Serverless Data Ingestion & Processing

## Infrastructure Overview
**Stack:** `Week1InfrastructureStack` (AWS CDK / Python)
- **Security:** S3 Bucket encrypted with Customer Managed Key (KMS).
- **Governance:** S3 Versioning enabled, auto-deletion policies for lab cleanup.
- **Ingestion:** Kinesis Data Stream (`week-1-lab-stream`) provisioned with **1 Shard** to test scaling limits.

---

## Lab 1: Kinesis Ingestion Stress Test
**Objective:** Validate stream capacity and observe throttling behavior.

**Experiment:**
- Configured `week-1-lab-stream` with **1 Shard** (Limits: 1MB/s or 1000 records/s).
- Ran `producer.py` with batch size 500 and 0s sleep to force high throughput.

**Outcome:**
- Throttling confirmed after ~60 seconds of execution.
- **Senior Analysis:** The producer successfully overwhelmed the single shard's ingestion limit, triggering the `ProvisionedThroughputExceededException`. In production, this would require resharding or implementing exponential backoff.

**Evidence (Log):**
```text
🚀 Starting STRESS TEST for stream: week-1-lab-stream
✅ Batch of 500 sent. Still accepted. Pushing harder...
✅ Batch of 500 sent. Still accepted. Pushing harder...
✅ Batch of 500 sent. Still accepted. Pushing harder...
⚠️ SUCCESS! Throttling achieved: 500 records rejected.
❌ Error Code: ProvisionedThroughputExceededException - Rate exceeded for shard shardId-000000000000 in stream week-1-lab-stream under account 637423431972.
⚠️ SUCCESS! Throttling achieved: 500 records rejected.
❌ Error Code: ProvisionedThroughputExceededException - Rate exceeded for shard shardId-000000000000 in stream week-1-lab-stream under account 637423431972.
```

---

## Lab 2: Serverless Consumer
**Objective:** Process stream data using AWS Lambda with event-driven architecture.

**Architecture:**
- **Trigger:** Kinesis Event Source Mapping (Batch Size: 100, Position: TRIM_HORIZON).
- **Compute:** Python 3.12 Lambda function.
- **Logic:** Base64 decoding -> JSON parsing -> Structured Logging (JSON).

**Outcome:**
- The Lambda function successfully connected to the stream.
- It automatically processed the backlog of records generated during Lab 1.
- Structured logs were verified in CloudWatch, proving the end-to-end data flow.

**Evidence (Log):**
```json
{
    "status": "processed", 
    "source": "kinesis-consumer", 
    "ticker": "TSLA", 
    "price": 750.25, 
    "event_id": "shardId-000000000000:496468..."
}
```
