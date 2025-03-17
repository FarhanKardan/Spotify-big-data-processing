import csv
from kafka import KafkaConsumer

# Create a Kafka consumer to listen to messages from the Kafka topic 'listen_events'
consumer = KafkaConsumer(
    'listen_events',
    bootstrap_servers='127.0.0.1:9092',
    group_id='my_group',
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

# Open a CSV file for writing
with open('kafka_messages.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header to the CSV file (modify as per the keys/fields in your Kafka messages)
    writer.writerow(['key', 'value'])

    # Iterate over the Kafka messages
    for message in consumer:
        # Write the message key and value to the CSV file
        writer.writerow([message.key, message.value])

        # Commit the message offset
        consumer.commit()

