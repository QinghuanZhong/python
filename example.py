import requests
from bs4 import BeautifulSoup

# 发送HTTP请求
url = 'http://example.com'
response = requests.get(url)
html_content = response.content

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 获取网页标题
title = soup.title.string
print(f"网页标题: {title}")

# 获取所有链接
links = soup.find_all('a')
for link in links:
    print(link.get('href'))
