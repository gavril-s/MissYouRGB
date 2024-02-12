from threading import Thread
import asyncio
import confluent_kafka


class Queue:
    def __init__(self):
        self.admin = confluent_kafka.amdin.AdminClient({"bootstrap.servers": "localhost:9092"})

    def create_topics(self, topics):
        new_topics = [
            confluent_kafka.admin.NewTopic(topic, num_partitions=1, replication_factor=1)
            for topic in topics
        ]
        response = self.admin.create_topics(new_topics)

        for topic, future in response.items():
            try:
                future.result()
                print(f"Topic {topic} created")
            except Exception as err:
                print(f"KafkaManager failed to create topic {topic}: {err}")


class MessageProducer:
    def __init__(self, configs, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._producer = confluent_kafka.Producer(
            {"bootstrap.servers": "localhost:9092"}
        )
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def produce(self, topic, value):
        result = self._loop.create_future()

        def on_delivery(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, confluent_kafka.KafkaException(err)
                )
            else:
                self._loop.call_soon_threadsafe(result.set_result, msg)

        self._producer.produce(topic, value, on_delivery=on_delivery)
        return result
    
    def close(self):
        self._cancelled = True
        self._poll_thread.join()


class MessageConsumer:
    def __init__(self):
        self.consumer = confluent_kafka.Consumer(
            {
                "bootstrap.servers": "localhost:9092",
                "group.id": "mygroup",
                "auto.offset.reset": "earliest",
            }
        )
        self.consumer.subscribe(["mytopic"])

    def read_messages(self):
        messages = []
        while True:
            message = self.consumer.poll(0.1)

            if message is None:
                break
            if message.error():
                print(f"MessageConsumer error: {message.error()}")
                continue

            message = message.value().decode("utf-8")
            messages.append(message)
            print(f"MessageConsumer received: {message}")

        return messages

    def close(self):
        self.consumer.close()
