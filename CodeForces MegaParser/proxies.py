import requests
from lxml.html import fromstring

def get_proxies(number_proxies):
  url = 'https://free-proxy-list.net/'
  response = requests.get(url)
  parser = fromstring(response.text)
  proxies = set()
  for i in parser.xpath('//tbody/tr')[:number_proxies]:
    if i.xpath('.//td[7][contains(text(),"yes")]'):
      #Grabbing IP and corresponding PORT
      proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
      proxies.add(proxy)
  return proxies

def get_proxies_manually():
  proxies = set()
  proxies.add('158.58.197.227:51481')
  proxies.add('195.238.85.215:50948')
  proxies.add('85.187.245.113:34158')
  proxies.add('195.123.228.82:8118')
  proxies.add('62.73.127.10:37790')
  proxies.add('95.158.137.254:57477')
  proxies.add('92.247.148.126:8080')
  proxies.add('193.68.19.34:40377')
  proxies.add('78.130.246.44:41444')
  proxies.add('94.236.198.160:33822')
  proxies.add('92.247.151.174:59284')
  proxies.add('95.87.14.3:34731')
  proxies.add('77.85.169.19:36776')
  proxies.add('178.239.225.245:45932')
  proxies.add('93.183.145.120:53281')
  proxies.add('87.120.145.59:53281')
  proxies.add('185.242.168.118:8080')
  proxies.add('85.196.183.162:8080')
  proxies.add('109.120.224.33:33221')
  proxies.add('185.108.141.19:8080')
  proxies.add('85.187.245.45:53281')
  proxies.add('78.128.77.171:8080')
  proxies.add('92.247.142.14:53281')
  proxies.add('87.121.49.250:53281')
  proxies.add('213.91.235.82:8888')
  proxies.add('62.182.114.164:43741')
  proxies.add('212.95.180.50:53281')
  proxies.add('5.32.131.98:53792')
  proxies.add('46.10.240.182:55878')
  proxies.add('83.228.74.251:50800')
  proxies.add('193.68.135.124:61982')
  proxies.add('109.199.133.161:23500')
  proxies.add('213.226.11.149:41878')
  proxies.add('77.70.115.103:8080')
  proxies.add('85.187.245.13:53281')
  proxies.add('46.229.206.135:42689')
  proxies.add('92.247.23.114:53281')
  proxies.add('193.68.135.123:59278')
  proxies.add('95.158.153.57:49753')
  proxies.add('87.118.185.23:80')
  proxies.add('185.108.141.74:8080')
  proxies.add('185.189.199.75:23500')
  return proxies