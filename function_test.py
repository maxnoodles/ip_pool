import requests
from lxml import etree

# url = 'https://www.baidu.com'
#
# proxy = {
#     'http': '176.98.76.210:42953',
#     'https': '176.98.76.210:42953'
# }
#
# res = requests.get(url=url, proxies=proxy, timeout=10)
# print(res.status_code)

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            html = etree.HTML(res.text)
            return html
    except:
        print(url, '抓取失败')
        return None

def crawl_daili66(page_count=4):
    """
    获取代理66的proxy
    :param page_count: 页码
    :return:
    """
    for page in range(1, page_count + 1):
        url = 'http://www.66ip.cn/{}'.format(page)
        html = get_page(url)
        contents = html.xpath('//div[@id="main"]//tr')[1:]
        print(contents)
        for content in contents:
            ip = content.xpath('./td[1]/text()')[0]
            port = content.xpath('./td[2]/text()')[0]
            print(':'.join([ip, port]))


def crawl_ip3366(page_count=4):
    """
    获取代理66的proxy
    :param page_count: 页码
    :return:
    """
    for i in range(1, page_count + 1):
        url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(i)
        html = get_page(url)
        contents = html.xpath('//div[@id="container"]//tbody/tr')
        print(contents)
        for content in contents:
            ip = content.xpath('./td[1]/text()')[0]
            port = content.xpath('./td[2]/text()')[0]
            print(':'.join([ip, port]))


def crawl_data5u():
    """
    获取代理66的proxy
    :param page_count: 页码
    :return:
    """
    url = 'http://www.data5u.com/free/gngn/index.shtml'
    html = get_page(url)
    contents = html.xpath('//ul[@class="l2"]')
    print(contents)
    for content in contents:
        ip = content.xpath('./span[1]/li/text()')[0]
        port = content.xpath('./span[2]/li/text()')[0]
        print(':'.join([ip.strip(), port.strip()]))

def crawl_xicidaili(page_count=3):
    """
    获取代理66的proxy
    :param page_count: 页码
    :return:
    """
    for i in range(1, page_count+1):
        url = 'https://www.xicidaili.com/nn/{}'.format(i)
        html = get_page(url)
        contents = html.xpath('//table[@id="ip_list"]//tr')[1:]
        print(contents)
        for content in contents:
            ip = content.xpath('./td[2]/text()')[0]
            port = content.xpath('./td[3]/text()')[0]
            print(':'.join([ip, port]))


crawl_xicidaili()


