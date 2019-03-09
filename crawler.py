import json
import re
import requests
from lxml import etree


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):

    def get_proxies(self, callback):
        proxies = []
        try:
            for proxy in eval('self.{}()'.format(callback)):
                print('成功获取代理', proxy)
                proxies.append(proxy)
        except Exception as e:
            print('网站爬取错误', repr(e))
        return proxies


    def get_page(self, url):
        """
        抓取代理网站的页面
        :param url: 代理网站的url
        :return: HTML的dom树
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                html = etree.HTML(res.text)
                return html
        except:
            print(url, '抓取失败')
            return None

    def crawl_daili66(self, page_count=4):
        """
        获取代理66的proxy
        :param page_count: 页码
        :return: ip地址:端口
        """
        for page in range(1, page_count + 1):
            url = 'http://www.66ip.cn/{}'.format(page)
            print('Crawling', url)
            html = self.get_page(url)
            contents = html.xpath('//div[@id="main"]//tr')[1:]
            for content in contents:
                ip = content.xpath('./td[1]/text()')[0]
                port = content.xpath('./td[2]/text()')[0]
                yield ':'.join([ip, port])


    def crawl_ip3366(self, page_count=4):
        for i in range(1, page_count+1):
            url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(i)
            print('Crawling', url)
            html = self.get_page(url)
            contents = html.xpath('//div[@id="container"]//tbody/tr')
            for content in contents:
                ip = content.xpath('./td[1]/text()')[0]
                port = content.xpath('./td[2]/text()')[0]
                yield ':'.join([ip, port])


    def crawl_iphai(self):
        url = 'http://www.iphai.com/'
        print('Crawling', url)
        html = self.get_page(url)
        contents = html.xpath('//div[@class="table-responsive module"]//tr')[1:]
        for content in contents:
            ip = content.xpath('./td[1]/text()')[0]
            port = content.xpath('./td[2]/text()')[0]
            yield ':'.join([ip.strip(), port.strip()])


    def crawl_data5u(self):
        url = 'http://www.data5u.com/free/gngn/index.shtml'
        print('Crawling', url)
        html = self.get_page(url)
        contents = html.xpath('//ul[@class="l2"]')
        for content in contents:
            ip = content.xpath('./span[1]/li/text()')[0]
            port = content.xpath('./span[2]/li/text()')[0]
            yield ':'.join([ip.strip(), port.strip()])


    # def crawl_xicidaili(self, page_count=3):
    #     for i in range(1, page_count+1):
    #         url = 'https://www.xicidaili.com/nn/{}'.format(i)
    #         print('Crawling', url)
    #         html = self.get_page(url)
    #         contents = html.xpath('//table[@id="ip_list"]//tr')[1:]
    #         for content in contents:
    #             ip = content.xpath('./td[2]/text()')[0]
    #             port = content.xpath('./td[3]/text()')[0]
    #             yield ':'.join([ip, port])








