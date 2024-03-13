import asyncio
import sys
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

import six

# need for python3.12
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
import json
import logging
from grifon.config import settings  # noqa


class KafkaClient:
    def __init__(self, topic, model=None, bootstrap_servers=f'127.0.0.1:{9092}', producer_config={},
                 consumer_config={}):
        self.topic = topic
        self.model = model

        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers,
                                         value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                         **producer_config)
        self.consumer = AIOKafkaConsumer(self.topic,
                                         bootstrap_servers=bootstrap_servers,
                                         auto_offset_reset='earliest',
                                         value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                         # уникальный group_id для группы потребителей
                                         group_id='your_unique_group_id',
                                         **consumer_config)
        self._worker = None

    async def send_message(self, message):
        logging.info('Start sending message ...')
        await self.producer.start()
        await asyncio.sleep(0.1)
        try:
            await self.producer.send_and_wait(self.topic, message)
            logging.info(f"Message sent to topic {self.topic}: {message}")
        finally:
            await self.producer.stop()
            await asyncio.sleep(0.1)

    async def process_tasks(self, process_func):
        logging.info(f'Start listening messages from {self.topic} ...')
        await self.consumer.start()
        try:
            while True:  # Бесконечный цикл для чтения сообщений
                msg_pack = await self.consumer.getmany(timeout_ms=1000)  # Ожидание сообщений в течение 1 секунды
                for tp, messages in msg_pack.items():
                    for message in messages:
                        await process_func(message.value)
                        await self.consumer.commit()
                await asyncio.sleep(1)
                # if some_condition:  # Условие для выхода из цикла, например, основанное на внешнем сигнале
                #     break
        finally:
            await self.consumer.stop()


async def process_message(message):
    logging.info(f"Обработка сообщения: {message}")


async def test():
    # тестовый пример внедрения механизма прослушивания топика и его обработка
    logging.info('Start test kafka work')
    topics = ['topic1', 'topic2', 'topicN']  # Список топиков для прослушивания

    # init clients for topics
    kafka_client_0 = KafkaClient(topic=topics[0])
    kafka_client_1 = KafkaClient(topic=topics[1])
    kafka_client_2 = KafkaClient(topic=topics[2])

    # send messages to all topics
    for idx, kafka_client in enumerate([kafka_client_0, kafka_client_1, kafka_client_2, ]):
        await kafka_client.send_message({"key": f"{idx} - value"})

    # start listener
    # todo пускать надо в отдельном потоке основного приложения
    tasks = [kafka_client_0.process_tasks(process_message),
             kafka_client_1.process_tasks(process_message),
             kafka_client_2.process_tasks(process_message), ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Запуск теста
    asyncio.run(test())
