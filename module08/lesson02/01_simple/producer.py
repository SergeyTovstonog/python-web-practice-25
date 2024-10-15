import pika

credentials = pika.PlainCredentials('admin', 'adminpassword')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.queue_declare(queue='hi')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!'.encode())
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!'.encode())
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!'.encode())
channel.basic_publish(exchange='', routing_key='hi', body='Hello World!'.encode())
channel.basic_publish(exchange='', routing_key='hi', body='Hello World!'.encode())
print(" [x] Sent 'Hello World!'")
connection.close()
