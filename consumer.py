# 导入所需的库
import pika
import pickle
import requests

# 定义队列的最大优先级和队列名称
MAX_PRIORITY = 100
QUEUE_NAME = 'scrape_queue'

# 创建一个到本地RabbitMQ服务器的连接
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
# 创建一个通道
channel = connection.channel()
# 创建一个requests会话
session = requests.Session()

# 定义一个名为scrape的函数，该函数接收一个请求对象，发送请求，并打印结果
def scrape(request):
    try:
        # 使用会话发送准备好的请求
        response = session.send(request.prepare())
        # 如果请求成功，打印成功的消息
        print(f'success scraped {response.url}')
    except requests.RequestException:
        # 如果请求失败，打印错误消息
        print(f'error occurred when scraping {request.url}')

# 主循环，不断从队列中获取消息并处理
while True:
    # 从队列中获取一条消息
    method_frame, header, body = channel.basic_get(
        queue=QUEUE_NAME, auto_ack=True)
    # 如果消息体存在
    if body:
        # 使用pickle反序列化消息体
        request = pickle.loads(body)
        # 打印获取的请求
        print(f'Get {request}')
        # 调用scrape函数处理请求
        scrape(request)