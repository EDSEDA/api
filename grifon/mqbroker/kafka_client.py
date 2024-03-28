import asyncio
import logging
from typing import Union

from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from pydantic import BaseModel

from grifon.config import settings  # noqa


class KafkaClient:
    def __init__(self, broker_urls=settings.KAFKA_CLIENT_PORT):
        self.broker_urls = broker_urls
        self.topics_handlers = {}
        self.consumer = Consumer({
            'bootstrap.servers': self.broker_urls,
            'group.id': 'my_group',
            'auto.offset.reset': 'earliest'
        })
        self.producer = Producer({'bootstrap.servers': self.broker_urls})

        self.admin_client = AdminClient({'bootstrap.servers': self.broker_urls})

    def register_topic_handler(self, topic: str, handler):
        """Регистрирует обработчик для заданного топика."""
        self._create_topic_if_not_exist(topic)
        self.topics_handlers[topic] = handler
        logging.info(f'New topic registered: "{topic}"')

    def _create_topic_if_not_exist(self, topic):
        if topic not in self.admin_client.list_topics(timeout=10).topics:
            new_topic = [NewTopic(topic, num_partitions=1, replication_factor=1)]
            fs = self.admin_client.create_topics(new_topic)
            for topic, f in fs.items():
                f.result()
                logging.info(f"Topic '{topic}' created")

    async def start_handling(self):
        """Запускает обработку сообщений для всех зарегистрированных топиков."""
        self.consumer.subscribe(list(self.topics_handlers.keys()))
        logging.info('Starting message handling...')
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    await asyncio.sleep(0.1)  # небольшая задержка, чтобы не загружать CPU
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                topic = msg.topic()
                if topic in self.topics_handlers:
                    handler = self.topics_handlers[topic]
                    await handler(msg)
        finally:
            self.consumer.close()

    def send_message(self, topic: str, message: Union[str, BaseModel]):
        """Отправляет сериализованное сообщение в заданный топик."""

        if isinstance(message, str):
            serialized_message = message
        elif isinstance(message, BaseModel):
            serialized_message = message.model_dump_json()
        else:
            logging.error(f"Unsupported message type: {type(message)}")
            return

        def acked(err, msg):
            if err is not None:
                logging.error(f"Failed to deliver message: {err}")
            else:
                logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

        self.producer.produce(topic, serialized_message, callback=acked)
        self.producer.poll(0)

    def flush(self):
        """Ожидает завершения всех асинхронных операций отправки сообщений."""
        self.producer.flush()
