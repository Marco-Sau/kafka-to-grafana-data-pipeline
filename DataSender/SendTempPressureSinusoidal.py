import time
import math
import random
from kafka import KafkaProducer
import json


def send_sensor_data(producer, temperature_topic, pressure_topic):
    while True:
        t = time.time()
        
        # Slow sinusoidal trend over time for temperature (10-minute cycles)
        trend = math.sin(t / 600)
        temperature = 99.0 + trend * 5 + random.uniform(-0.7, 0.7)

        # Create JSON payload for temperature
        temperature_payload = {"temperature": round(temperature, 2)}

        # Serialize temperature payload to JSON
        temperature_data = json.dumps(temperature_payload)

        # Send temperature data to temperature topic
        producer.send(temperature_topic,
                      value=temperature_data.encode("utf-8"))
        producer.flush()

        # Slow sinusoidal trend over time for pressure (1-minute cycles)
        trend = math.sin(t / 60)
        pressure = 100.0 + trend * 5 + random.uniform(-0.5, 0.5)

        # Create JSON payload for pressure
        pressure_payload = {"pressure": round(pressure, 2)}

        # Serialize pressure payload to JSON
        pressure_data = json.dumps(pressure_payload)

        # Send pressure data to pressure topic
        producer.send(pressure_topic, value=pressure_data.encode("utf-8"))
        producer.flush()

        print(f"Sent temperature data: {round(temperature, 2)}°C")
        print(f"Sent pressure data: {round(pressure, 2)} hPa")

        time.sleep(1)  # Wait for 1 second (more frequent updates)


if __name__ == "__main__":
    bootstrap_servers = "localhost:9093"  # Kafka broker address
    temperature_topic = "temperature"  # Topic to send temperature data
    pressure_topic = "pressure"  # Topic to send pressure data

    # Create Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        # Use default serialization
        value_serializer=lambda v: v,
        api_version=(2, 0, 2)
    )

    try:
        send_sensor_data(producer, temperature_topic, pressure_topic)
    except KeyboardInterrupt:
        print("\nStopping data transmission...")
    finally:
        producer.close()
        print("Producer closed.") 