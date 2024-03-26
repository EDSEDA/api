import asyncio

from confluent_kafka import Consumer, Producer, KafkaError


class MessageHandler:
    def __init__(self, broker_urls):
        self.broker_urls = broker_urls
        self.topics_handlers = {}
        self.consumer = Consumer({
            'bootstrap.servers': self.broker_urls,
            'group.id': 'my_group',
            'auto.offset.reset': 'earliest'
        })

    def register_topic_handler(self, topic: str, handler):
        """Регистрирует обработчик для заданного топика."""
        self.topics_handlers[topic] = handler
        # Обновление подписки с каждым новым обработчиком
        self.consumer.subscribe(list(self.topics_handlers.keys()))

    async def start_handling(self):
        """Запускает обработку сообщений для всех зарегистрированных топиков."""
        print('Starting message handling...')
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


async def send_test_message(broker_urls: str, topic: str, message: str):
    producer = Producer({'bootstrap.servers': broker_urls})
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()
    print(f"Sent message: {message} to topic {topic}")


async def handler_example(msg):
    """Пример обработчика сообщения."""
    print(f"Received message: {msg.value().decode('utf-8')} from topic {msg.topic()}")


async def main():
    handler = MessageHandler("localhost:9092")
    handler.register_topic_handler("my_topic1", handler_example)
    handler.register_topic_handler("my_topic2", handler_example)

    # Запуск обработчика сообщений в фоне
    await handler.start_handling()

    # # Отправка тестового сообщения в топики
    # await send_test_message("localhost:9092", "my_topic1", "Hello, Kafka to topic1!")
    # await send_test_message("localhost:9092", "my_topic2", "Hello, Kafka to topic2!")
    #
    # await asyncio.sleep(2)
    #
    # # Завершаем обработку сообщений
    # handler_task.cancel()
    # try:
    #     await handler_task
    # except asyncio.CancelledError:
    #     print("Message handling cancelled.")


if __name__ == "__main__":
    asyncio.run(main())
