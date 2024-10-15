import pika
import sys

credentials = pika.PlainCredentials('admin', 'adminpassword')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
while True:
    message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange='logs', routing_key='', body=message.encode())
    print(" [x] Sent %r" % message)
connection.close()