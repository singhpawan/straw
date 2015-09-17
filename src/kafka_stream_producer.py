#!/usr/bin/python3
#
#   Put documents from the stream into Kafka
#

import argparse
from kafka import SimpleProducer, KafkaClient

def chunk_iterable(A,n):
    '''An iterable that contains the iterates of A divided into lists of size n.
       A    iterable
       n    int, size of chunk
    '''
    cnt = 0
    chunk = []
    for v in A:
        if cnt<n:
            cnt+=1
            chunk.append(v)
        else:
            yield(chunk)
            cnt = 0
            chunk = []
    if len(chunk)>0:
        yield(chunk)

if __name__=="__main__":

    # arg parsing
    parser = argparse.ArgumentParser(description="Feed Kafka a stream from a file")
    parser.add_argument("file", help="A file of data, one datum per line")
    parser.add_argument("host", help="Public IP address of a Kafka node")
    parser.add_argument("topic", help="Kafka topic to feed")
    parser.add_argument("-p", "--port", default="9092", help="Public IP address of a Kafka node, default 9092")
    parser.add_argument("-c", "--chunksize", default=10, help="Number of messages to send at one time,  default 10")    
    args = parser.parse_args()

    # get a client
    print("Connecting to Kafka node {0}:{1}".format(args.host, args.port))
    kafka = KafkaClient("{0}:{1}".format(args.host, args.port))
    producer = SimpleProducer(kafka)
    
    # read through the file and send messages to Kafka in chunks
    with open(args.file, "rb") as f:
        for chunk in chunk_iterable(f, 10):
            print("Sending {0} messages to topic {1} on {2}".format(len(chunk), args.topic, args.host))
            print(chunk[0])
            producer.send_messages(args.topic, *chunk)
            
