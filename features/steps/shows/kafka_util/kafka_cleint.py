#encoding:utf-8
#date:2019/9/2 上午10:28
#@Author:hcx

import json
import logging as log
import uuid
from features.constants import KAFAKA_HOST, KAFAKA_PORT
# from kafka import KafkaProducer
# from kafka import KafkaConsumer
# from kafka.common import TopicPartition
# from kafka.errors import KafkaError



class Kafka_producer:

    def __init__(self):
        self.kafkaHost = KAFAKA_HOST
        self.kafkaPort = KAFAKA_PORT
        bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
                kafka_host=self.kafkaHost,
                kafka_port=self.kafkaPort
                )
        log.info(f"boot svr:{bootstrap_servers}")
        self.producer = KafkaProducer(bootstrap_servers = bootstrap_servers
                )

    def send_kafka(self, key, topic_name, topic_content):
        try:
            parmas_message = json.dumps(topic_content, ensure_ascii=False)
            producer = self.producer
            log.info(f"kafka producer,params_message:{parmas_message}")
            v = parmas_message.encode('utf-8')
            k = key.encode('utf-8')
            log.info(f"send msg,key:{k},value:{v}")
            producer.send(topic_name, key=k, value= v)
            producer.flush()

        except KafkaError as e:
            log.info (f"kafka error:{e}")




class Kafka_consumer:
    def __init__(self):
        from kafka import KafkaConsumer
        self.consumer = KafkaConsumer(bootstrap_servers=KAFAKA_HOST+":"+KAFAKA_PORT,
                                      group_id=uuid.uuid1())

    def run(self, topic_consumer):
        try:
            tp = TopicPartition(topic_consumer, partition=0)
            self.consumer.assign([tp])
            committed = self.consumer.committed(tp)
            self.consumer.seek_to_end(tp)
            last_offset = self.consumer.position(tp)
            log.info(f"topic:{topic_consumer}  committed:{committed} last:{last_offset}")
            self.consumer.seek(TopicPartition(topic_consumer, partition=0), last_offset - 1)
            for msg in self.consumer:
                value = msg.value.decode(encoding="utf-8")
                log.info(f"topic_value:{msg.topic},partition_value:{msg.partition},"
                         f"offeset_value:{msg.offset},value:{value}")
                if not value:
                    self.consumer.close()
                    break
                return value
        except KeyboardInterrupt as e:
            log.info(f"key board Interrupt:{e}")

    def get(self,topic_name):
        return self.run(topic_name)