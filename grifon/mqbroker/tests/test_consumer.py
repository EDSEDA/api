import asyncio

from grifon.mqbroker.kafka_client import KafkaClient

kafka_client = KafkaClient("localhost:9092")


async def handler_example(msg):
    """Пример обработчика сообщения."""
    print(f"Received message: {msg.value().decode('utf-8')} from topic {msg.topic()}")


@kafka_client.register_topic_handler("my_topic2")
async def handler_example(msg):
    """Пример обработчика сообщения."""
    print(f"Received message: {msg.value().decode('utf-8')} from topic {msg.topic()}")


async def main():
    kafka_client.register_topic_handler("my_topic1", handler_example)
    kafka_client.register_topic_handler("my_topic1", handler_example)

    # Запуск обработчика сообщений в фоне
    await kafka_client.start_handling()


if __name__ == "__main__":
    asyncio.run(main())
