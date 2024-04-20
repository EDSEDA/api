import asyncio

from pydantic import BaseModel

from grifon.mqbroker.kafka_client import KafkaClient

kafka_client = KafkaClient("localhost:9092")


async def send_test_message(topic: str, message: str | BaseModel):
    kafka_client.send_message(topic, message)
    kafka_client.flush()
    print(f"Sent message: {message} to topic {topic}")


class TestMessage(BaseModel):
    id: int
    name: str


m = TestMessage(id=12, name='Nik')


async def main():

    # Отправка тестового сообщения в топики
    await send_test_message("my_topic1", m)
    await send_test_message("my_topic2", m)


if __name__ == "__main__":
    asyncio.run(main())
