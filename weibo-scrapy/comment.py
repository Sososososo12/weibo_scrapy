# -*- coding: utf-8 -*-
import re
from lxml import etree
import requests
import time
import pandas as pd

'''
使用前，
cookies需要更新
'''

start_site = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&page={}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie': 'SCF=ApUALGl5o2wQZBDEzzMpnkGUO_OEfMiAuO8L4uvywo-Qq1UmAIG7nzOa2WPlftUWSyyuXvFrE7PmFBBAjXLI_Ug.; SUB=_2A25wHrWLDeRhGeBN4lcQ9irEyTqIHXVT4NvDrDV6PUJbkdAKLUL5kW1NRAY1GGVLmHMHYEoOOXNt-U6wOMN6luhA; SUHB=0D-FVI9EeEaRPU; _T_WM=82867258802'
}


def get_comment_state(weibo_url):
    '''
    判断微博评论页的获取状态，并返回评论页内容
    :param weibo_url:微博的评论页
    :return:微博评论页的内容
    '''
    content = requests.get(weibo_url, headers=headers).content
    # print(content.decode('UTF-8'))
    selector = etree.HTML(content)
    items = selector.xpath('//div[contains(@id,"C_")]')
    if len(items) == 0:
        print('评论数为0，请重新爬取！')
    return len(items), content


def get_comment_info(content):
    ids = []
    id_names = []
    informations = []
    like_nums = []
    like_urls = []
    reply_urls = []
    selector = etree.HTML(content)
    items = selector.xpath('//div[contains(@id,"C_")]')
    for item in items:
        id = item.xpath('a/@href')[0]
        id_name = item.xpath('a/text()')[0]
        information = item.xpath('span[@class="ctt"]/text()')[0]
        like_url = item.xpath('span[@class="cc"]/a/@href')[0]
        like_num = item.xpath('span[@class="cc"]/a/text()')[0].replace('赞[', '').replace(']', '')
        reply_url = item.xpath('span[@class="cc"]/a/@href')[1]
        # print(id)
        ids.append(id)
        id_names.append(id_name)
        informations.append(information)
        like_nums.append(like_num)
        like_urls.append(like_url)
        reply_urls.append(reply_url)
    return ids, id_names, informations, like_nums, like_urls, reply_urls


def get_repost_state(weibo_url,page_num=1):
    '''
    判断微博回复页的获取状态，并返回回复页内容
    :param weibo_url:微博的回复页
    :return:微博回复页的内容
    '''
    new_url_state=weibo_url.replace('&#rt','page={}')
    new_url=new_url_state.format(page_num)
    content = requests.get(new_url, headers=headers).content
    # print(content.decode('UTF-8'))
    selector = etree.HTML(content)
    items_num = selector.xpath('//div/span[@id="rt"]/text()')[0]
    repost_num_state=re.findall('转发\[(.*)\]',items_num)[0]
    repost_num=int(float(repost_num_state))
    if repost_num==0:
        print('评论数为0!')

    return repost_num, content


def get_repost_info(content):
    selector = etree.HTML(content)
    items = selector.xpath('//div[@class="c"]')
    for item in items:
        id = item.xpath('a/@href')[0]
        id_name = item.xpath('a/text()')[0]
        information = item.xpath('span[@class="ctt"]/text()')[0]
        like_url = item.xpath('span[@class="cc"]/a/@href')[0]
        like_num = item.xpath('span[@class="cc"]/a/text()')[0].replace('赞[', '').replace(']', '')
        reply_url = item.xpath('span[@class="cc"]/a/@href')[1]
        print(id)


weibo_url = 'https://weibo.cn/repost/HCDwlrJRX?uid=1647951825&#rt'
state = get_repost_state(weibo_url)
# print(state[0])
get_repost_info(state[1])
