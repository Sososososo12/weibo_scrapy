import re
from lxml import etree
import requests
import time
import pandas as pd

w_urls=[]
name_topics=[]
infomations_slim=[]
account_urls=[]
account_names=[]
times=[]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie': 'SUV=002F43732417FDC55B90CEEE786EE877; CXID=C610D90D5EF40AEA9E24970D2DEC16BA; SUID=C5FD17243665860A5B90D79A000B8DA2; IPLOC=CN3100; wuid=AAGyGaA8JgAAAAqLFD2NogcAGwY=; ad=OEp8ykllll2N9AONlllllV1YrTDlllllK9evmkllll9lllll4klll5@@@@@@@@@@; ABTEST=1|1562861640|v1; SNUID=70D5CBF488820AED9C77D0B888839821; weixinIndexVisited=1; JSESSIONID=aaarvpWQ02QY757KbUuRw; ppinf=5|1562861694|1564071294|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyMzpTbyUyMCVFNSVBNyU5QSVFOSU5RCU5NnxjcnQ6MTA6MTU2Mjg2MTY5NHxyZWZuaWNrOjIzOlNvJTIwJUU1JUE3JTlBJUU5JTlEJTk2fHVzZXJpZDo0NDpvOXQybHVBb0t5MVZQMFhDX25tUHh1UXZkRGJvQHdlaXhpbi5zb2h1LmNvbXw; pprdig=u9bMJfukI-dXLq2h8R9Atos8x99y-glmzEPfsU05P35LE54YCUZFWWBxtX_q1v9d-5Db2zE1kbciCGw6A07PHnRQcPGVw-O7bwg32XjhV-D1rl5AdLKuBQd_4BJQCeXzvdBAeNjTa4C6a_h0OpLN9ae7zXHTOXHafPyZWFN-vPE; sgid=10-38252659-AV0nYH5DmsjwtvbdxviaDYK4; ppmdig=15628616940000009e433739ab7cee7823fec44ab3bec8f5; sct=3'
}

for page_num in range(1,89):
    url = 'https://weixin.sogou.com/weixin?query={}&type=2&page={}&ie=utf8'.format('2019环青海湖', str(page_num))
    content = requests.get(url, headers=headers).content.decode('utf-8')
    # print(content)
    selector = etree.HTML(content)
    items = selector.xpath('//ul[@class="news-list"]/li')
    for item in items:
        w_url = item.xpath('div[@class="txt-box"]/h3/a/@href')[0]
        name_topic_state = item.xpath('div[@class="txt-box"]/h3/a')
        name_topic = name_topic_state[0].xpath('string(.)')
        infomation_slim_state = item.xpath('div[@class="txt-box"]/p')
        infomation_slim = infomation_slim_state[0].xpath('string(.)')
        account_url = item.xpath('div[@class="txt-box"]/div/a/@href')[0]
        account_name = item.xpath('div[@class="txt-box"]/div/a/text()')[0]
        time_state = item.xpath('div[@class="txt-box"]/div/span/script/text()')[0]

        w_urls.append(w_url)
        name_topics.append(name_topic)
        infomations_slim.append(infomations_slim)
        account_urls.append(account_url)
        account_names.append(account_name)
        times.append(time)
    print('已完成第 '+str(page_num)+' 页的爬取! 现有数据'+str(len(w_urls))+'条')
    time.sleep(3)

    print('开始保存数据!')
    data1 = pd.DataFrame({'w_url': w_urls,
                          'name_topic': name_topics,
                          'infomation_slim': infomations_slim,
                          'account_url': account_urls,
                          'account_name': account_names,
                          'time': times,
                          })
    data1.to_excel(u'../weixing/weixin_07_11_test.xls', index=False, encoding='"utf_8_sig')
    print('信息写入完成！')
        # time=re.findall('timeConvert(\'(.*)\')',time_state)
        # print()


# import requests,re
# # 输入基于搜狗微信的文章临时链接，获取阅读数和点赞数
# def get_c_detail(url):
#     # 临时文章链接
#     linshi_link = url.encode('utf-8')
#     # 正则表达式，提取timestamp和signature参数
#     timestamp = re.findall('timestamp=(\d+)',url)[0]
#     signature = re.findall('signature=(.+)',url)[0]
#     # 生成接口链接
#     s = 'http://mp.weixin.qq.com/mp/getcomment?src=3&timestamp={}&ver=1&signature={}'.format(timestamp,signature)
#     # get方法获取接口信息
#     r = requests.get(s,headers=headers)
#     if r.status_code == 200:
#         c = r.content
#         # 正则表达式，提取阅读数和点赞数
#         # 阅读数
#         read_num = re.findall('"read_num":(\d+)',c)[-1]
#         # 点赞数
#         like_num = re.findall('"like_num":(\d+)',c)[-1]
#         return read_num,like_num
#
# url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1562861868&ver=1722&signature=Mz3qO8gRhFHbOp0*KiIiTXqFsClbfDSLxuRvCqIZwBZ4zExm11otmbdZazcrXQEkiMoLCWRr7ja0ZZVFvYg1NC93zNAbEPjD9-t7Rc-g2COBsZvdS7GvMAAN41TOP*yI&new=1'
# print(get_c_detail(url))