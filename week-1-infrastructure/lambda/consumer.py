import base64
import json
import time

print("Loading function")


def handler(event, context):
    """
    Standard Kinesis Event Consumer (Lambda Handler).
    Decodes the payload and logs structured data to CloudWatch.
    """
    # Kinesis sends records in batches. We must iterate through them.
    for record in event['Records']:
        try:
            # 1. Decode the Base64 Kinesis data (Standard Requirement)
            payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            data = json.loads(payload)

            # 2. SENIOR PATTERN: Structured Logging
            # We output JSON (instead of raw strings) so it can be queried
            # efficiently by CloudWatch Logs Insights.
            print(json.dumps({
                "status": "processed",
                "source": "kinesis-consumer",
                "ticker": data.get("ticker"),
                "price": data.get("price"),
                "event_id": record['eventID'],
                "timestamp": time.time()
            }))

        except Exception as e:
            # If a record fails (e.g., corrupt JSON, "Poison Pill"), log the error.
            # In W1-L3, we will modify this to handle the error more gracefully.
            print(f"❌ Error processing record: {e}")

    return f"Successfully processed {len(event['Records'])} records."