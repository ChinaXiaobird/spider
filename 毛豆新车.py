import threading
from threading import Thread
from queue import Queue
import requests
from lxml import etree
from fake_useragent import UserAgent

num = 1


def page_url(base_url):
    headers = {
        'User-Agent': ua.random,
    }
    page = '1'
    url_list = []
    while True:
        url = base_url % page
        print(url)
        html = requests.get(url, headers=headers).content.decode('utf-8')
        page = str(int(page) + 1)
        tree = etree.HTML(html)
        a_list = tree.xpath('//div[@class="list-wrap clearfix"]/a/@href')
        for a in a_list:
            url_list.append(a)
        if len(a_list) == 0:
            break
    return url_list


class Crawl_MD(Thread):
    def __init__(self, url_queue):
        super(Crawl_MD, self).__init__()
        self.url_queue = url_queue

    def run(self):
        while True:
            if self.url_queue.empty():
                break
            try:
                url = self.url_queue.get(block=False)
                self.get_request(url)
            except Exception as e:
                print(e)

    def get_request(self, url):
        headers = {
            'User-Agent': ua.random,
        }
        response = requests.get(url, headers=headers).content.decode('utf-8')
        get_queue.put(response)


class Customer_MD(Thread):
    def run(self):
        while True:
            if get_queue.empty() and flag:
                break
            try:
                response = get_queue.get(block=False)
                self.get_data(response)
            except Exception as e:
                print(e)

    def get_none(self, word):
        if len(word) > 0:
            return word[0]
        else:
            return ''

    def get_data(self, response):
        tree = etree.HTML(response)
        title = tree.xpath('//h2[@class="banner-tit"]/text()')
        img = tree.xpath('//div[@class="slider"]//li[1]/img/@src')
        soufu = tree.xpath('//div[@class="sy-yf"]//p[@class="sy-num"]/text()')
        yuegong = tree.xpath('//div[@class="sy-yf"]/div[2]/p[@class="yf-num sy-num"]/text()')
        firm_money = tree.xpath('//p[@class="price "]/text()')
        peizhi = tree.xpath('//ul[@class="config-detail"]//p/text()')
        PZ = {}
        for i, j in zip(peizhi[::2], peizhi[1::2]):
            PZ[i] = j
        # print(title, img, soufu, yuegong, firm_money, peizhi)
        data = {
            'title': self.get_none(title),
            'img': self.get_none(img),
            'soufu': ''.join(soufu).replace('   ', '|'),
            'yuegong': ''.join(yuegong).replace('  ', '|'),
            'firm_money': self.get_none(firm_money),
            'peizhi': PZ
        }
        print(data)
        global num
        word = [{"num": num}, {'data': data}]
        if lock.acquire():
            with open('m.txt', 'a') as f:
                f.write(str(word) + '\n')
                num += 1
                lock.release()


flag = False
get_queue = Queue()
if __name__ == '__main__':
    ua = UserAgent()
    list = page_url('https://www.maodou.com/car/list/all/pg%s')
    url_queue = Queue()
    crawl_list = []
    customer_list = []
    lock = threading.Lock()
    [url_queue.put(i) for i in list]
    for cre in range(3):
        crawl = Crawl_MD(url_queue)
        crawl.start()
        crawl_list.append(crawl)

    for cus in range(3):
        customer = Customer_MD()
        customer.start()
        customer_list.append(customer)

    [i.join() for i in crawl_list]

    flag = True

    [a.join() for a in customer_list]



