README.txt – Terminal Commands for Kafka and Zookeeper Integration

Step 1: Start Zookeeper

cd /usr/local/kafka/kafka_2.13-3.2.1
bin/zookeeper-server-start.sh config/zookeeper.properties &

Step 2: Start Kafka Broker

bin/kafka-server-start.sh config/server.properties &

Step 3: Create Kafka Topic for Streaming Test Data

bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test_data

To confirm topic creation:

bin/kafka-topics.sh --list --bootstrap-server localhost:9092

Step 4: Run Kafka Producer Script to Send Test Data

Navigate to the project directory where your `producer_test_data.py` file is located.
Then run the following using your Python environment (Anaconda Python used here):

~/anaconda3/bin/python producer_test_data.py

This script sends 100-row batches of test data every 5 seconds to the Kafka topic `test_data`.
Total test rows streamed: 15,479

Dependency Notes

If the producer fails due to missing Python packages (e.g., `pandas`), install them with:

pip install pandas

(Ensure you're using the Python environment tied to the producer execution.)