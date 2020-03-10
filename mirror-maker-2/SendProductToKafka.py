from confluent_kafka import Producer, KafkaError
import json, os

KAFKA_BROKERS = os.getenv('KAFKA_BROKERS','my-cluster-kafka-bootstrap-jb-kafka-strimzi.gse-eda-demos-fa9ee67c9ab6a7791435450358e564cc-0001.us-east.containers.appdomain.cloud:443')
KAFKA_APIKEY = os.getenv('KAFKA_APIKEY','')
KAFKA_CERT = os.getenv('KAFKA_CERT','ca.crt')
KAFKA_USER =  os.getenv('KAFKA_USER','boyerje@us.ibm.com')
KAFKA_PWD =  os.getenv('KAFKA_PWD','Spr!ng2020IsMild')
SOURCE_TOPIC='products'

options ={
    'bootstrap.servers': KAFKA_BROKERS,
    'group.id': 'ProductsProducer'
}

if (KAFKA_APIKEY != '' ):
    options['security.protocol'] = 'SASL_SSL'
    options['sasl.mechanisms'] = 'PLAIN'
    options['sasl.username'] = 'token'
    options['sasl.password'] = KAFKA_APIKEY

if (KAFKA_CERT != '' ):
    options['security.protocol'] = 'SSL'
    options['sasl.username'] = KAFKA_USER
    options['sasl.password'] = KAFKA_PWD
    options['ssl.ca.location'] = KAFKA_CERT

print('[KafkaProducer] - {}'.format(options))
producer=Producer(options)

def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('[ERROR] - [KafkaProducer] - Message delivery failed: {}'.format(err))
        else:
            print('[KafkaProducer] - Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def publishEvent(topicName, products):
    try:
        for p in products:
            print(p)
            producer.produce(topicName,
                key=p["product_id"],
                value=json.dumps(p).encode('utf-8'), 
                callback=delivery_report)
    except Exception as err:
        print('Failed sending message {0}'.format(dataStr))
        print(err)
    producer.flush()
    
def readProducts():
    p = open('./data/products.json','r')
    return json.load(p)

def signal_handler(sig,frame):
    producer.close()
    sys.exit(0)

if __name__ == "__main__":
    products = readProducts()
    try:
        publishEvent(SOURCE_TOPIC,products)
    except KeyboardInterrupt:
        producer.close()
        sys.exit(0)
    