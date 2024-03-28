import asyncio


from grifon.mqbroker.kafka_client import KafkaClient

kafka_client = KafkaClient("localhost:9092")


async def send_test_message(topic: str, message: str):
    kafka_client.send_message(topic, message)
    kafka_client.flush()
    print(f"Sent message: {message} to topic {topic}")


async def main():

    # Отправка тестового сообщения в топики
    await send_test_message("my_topic1", "Hello, Kafka to topic1!")
    await send_test_message("my_topic2", "Hello, Kafka to topic2!")


if __name__ == "__main__":
    asyncio.run(main())
