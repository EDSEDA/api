import sys
import six

# need for python3.12
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from config import settings


class KafkaClient:
    def __init__(self, topic, bootstrap_servers=f'127.0.0.1:{29092}', producer_config={}, consumer_config={}):
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                      api_version=(0, 10),
                                      **producer_config)
        self.consumer = KafkaConsumer(self.topic,
                                      bootstrap_servers=bootstrap_servers,
                                      auto_offset_reset='earliest',
                                      value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                      api_version=(0, 10),
                                      **consumer_config)

    def send_message(self, message):
        try:
            self.producer.send(self.topic, message)
            self.producer.flush()
            logging.info(f"Сообщение отправлено в топик {self.topic}: {message}")
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")

    def listen_messages(self, process_func):
        try:
            logging.info(f"Подписка на топик {self.topic} и ожидание сообщений...")
            for message in self.consumer:
                logging.info(f"Получено сообщение: {message.value}")
                process_func(message.value)
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


if __name__ == "__main__":
    topic = 'test_topic'
    kafka_client = KafkaClient(topic=topic)

    kafka_client.send_message({"key": "value"})

    # # Прослушивание топика и обработка сообщений
    # # Внимание: следующая строка блокирует выполнение, расскомментируйте для использования
    kafka_client.listen_messages(process_message)
