from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from grifon.config import settings      # noqa


class KafkaClient:
    def __init__(self, topic, bootstrap_servers=f'127.0.0.1:{9092}', producer_config={}, consumer_config={}):
        self.topic = topic
        self.group_id = 'test_group_id'

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Подтверждение от всех реплик
            **producer_config
        )
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id=self.group_id,  # Указание идентификатора группы потребителей
            **consumer_config
        )

    def send_message(self, message):
        try:
            future = self.producer.send(self.topic, message)
            result = future.get(timeout=60)  # Ожидание завершения отправки
            logging.info(f"Сообщение отправлено в топик {self.topic}: {result}")
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")

    def listen_messages(self, process_func):
        try:
            logging.info(f"Подписка на топик {self.topic} и ожидание сообщений...")
            for message in self.consumer:
                logging.info(f"Получено сообщение: {message.value}")
                process_func(message.value)
                self.consumer.commit()  # Ручной коммит смещения
        except Exception as e:
            logging.error(f"Ошибка при получении сообщений: {e}")
        finally:
            self.consumer.close()
            logging.info("Потребитель закрыт.")

    def close(self):
        self.producer.close()
        logging.info("Производитель закрыт.")


def process_message(message):
    logging.info(f"Обработка сообщения: {message}")


def test_kafka_process_message():
    topic = 'test_topic'
    kafka_client = KafkaClient(topic=topic)

    kafka_client.send_message({"key": "value"})

    # # Прослушивание топика и обработка сообщений
    # # Внимание: следующая строка блокирует выполнение, расскомментируйте для использования
    kafka_client.listen_messages(process_message)


if __name__ == "__main__":
    test_kafka_process_message()
