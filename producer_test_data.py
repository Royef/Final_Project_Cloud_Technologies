import os
import time
import json
import pandas as pd
from confluent_kafka import Producer

# ----------------------------
# Kafka Configuration
# ----------------------------
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# ----------------------------
# Load CSV Parts (written by Spark)
# ----------------------------
data_dir = "test_data_for_kafka"
csv_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.startswith("part-")]

# Combine all part CSVs into one DataFrame
df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Optional: Show total rows loaded
total_rows = len(df)
print(f"✅ Loaded {total_rows} rows from test set.")

# ----------------------------
# Send in Batches
# ----------------------------
batch_size = 100  # Number of rows per batch
wait_time = 5     # Seconds between batches

for i in range(0, total_rows, batch_size):
    # Slice next batch
    batch_df = df.iloc[i:i+batch_size]

    # Convert batch to list of dicts (JSON array)
    batch_records = batch_df.dropna().to_dict(orient='records')
    batch_json = json.dumps(batch_records)

    # Send batch to Kafka
    producer.produce('test_data', key=str(i), value=batch_json)
    print(f"📤 Sent batch {i//batch_size + 1} | Rows: {len(batch_records)}")

    # Wait between batches
    time.sleep(wait_time)

# Ensure all messages are delivered
producer.flush()
print("✅ All batches sent to Kafka.")

