import os
import boto3
import json
import time
import random
from faker import Faker
from datetime import datetime

# --- CONFIGURATION ---
# The script will auto-discover the stream name from the Outputs,
# but hardcoding the name ensures consistency in this lab.
STREAM_NAME = "week-1-lab-stream"
# The region is pulled from the environment variable (or hardcoded here)
REGION = "us-east-1"

# Initialize (Boto3 will automatically use the AWS_PROFILE environment variable)
kinesis = boto3.client('kinesis', region_name=REGION)
fake = Faker()


def generate_record():
    """Generates a fake stock trade record."""
    # Data Volume and Variety: Simulates typical trading data
    return {
        "event_time": datetime.now().isoformat(),
        "ticker": random.choice(["AAPL", "AMZN", "MSFT", "GOOGL", "TSLA", "NFLX"]),
        "price": round(random.uniform(100, 3000), 2),
        "volume": random.randint(1, 100),
        "trade_id": fake.uuid4()
    }


def put_records():
    # ... (Diagnostics remain the same) ...
    print(f"🚀 Starting STRESS TEST for stream: {STREAM_NAME}")

    while True:
        records = []
        # MAXIMIZE BATCH: Kinesis allows up to 500 records per API call.
        # We will fill the boat to force the throttle.
        for _ in range(500):
            data = generate_record()
            partition_key = data['ticker']
            records.append({
                'Data': json.dumps(data),
                'PartitionKey': partition_key
            })

        try:
            # SEND FAST: No sleep. Maximum payload.
            response = kinesis.put_records(
                StreamName=STREAM_NAME,
                Records=records
            )

            failed_count = response.get('FailedRecordCount', 0)

            # If we failed, we succeeded in our lab goal.
            if failed_count > 0:
                print(f"⚠️ SUCCESS! Throttling achieved: {failed_count} records rejected.")
                # We print the specific error codes from the first failed record to confirm
                # it is indeed ProvisionedThroughputExceeded
                for r in response['Records']:
                    if 'ErrorCode' in r:
                        print(f"❌ Error Code: {r['ErrorCode']} - {r['ErrorMessage']}")
                        break
            else:
                print(f"✅ Batch of 500 sent. Still accepted. Pushing harder...")

        except Exception as e:
            print(f"❌ Unhandled Error: {str(e)}")

        # NO SLEEP. We want to flood it.
        # time.sleep(0.1)

if __name__ == "__main__":
    put_records()