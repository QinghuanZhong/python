# 导入所需的库
import pika
import requests
import pickle

# 定义队列的最大优先级和总消息数量，以及队列名称
MAX_PRIORITY = 100
TOTAL = 100
QUEUE_NAME = 'scrape_queue'

# 创建一个到本地RabbitMQ服务器的连接
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
# 创建一个通道
channel = connection.channel()
# 在通道上声明一个持久的队列
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# 循环TOTAL次，每次创建一个请求并将其发送到队列
for i in range(1, TOTAL + 1):
    # 创建一个URL，其中的数字每次循环都会增加
    url = f'https://ssr1.scrape.center/detail/{i}'
    # 创建一个GET请求
    request = requests.Request('GET', url)
    # 将请求序列化并发送到队列
    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # 使消息持久化
                          ),
                          body=pickle.dumps(request))  # 序列化请求
    # 打印已发送的请求的URL
    print(f'Put request of {url}')