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
    'Cookie': 'SCF=ApUALGl5o2wQZBDEzzMpnkGUO_OEfMiAuO8L4uvywo-Qq1UmAIG7nzOa2WPlftUWSyyuXvFrE7PmFBBAjXLI_Ug.; SUB=_2A25wHrWLDeRhGeBN4lcQ9irEyTqIHXVT4NvDrDV6PUJbkdAKLUL5kW1NRAY1GGVLmHMHYEoOOXNt-U6wOMN6luhA; SUHB=0D-FVI9EeEaRPU; MLOGIN=1; _T_WM=82867258802; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D2019%25E7%258E%25AF%25E9%259D%2592%25E6%25B5%25B7%25E6%25B9%2596%25E8%2587%25AA%25E8%25A1%258C%25E8%25BD%25A6%25E8%25B5%259B%2526t%253D0; WEIBOCN_FROM=1110106030'
}


def search_weibo(keyword='2019环青海湖自行车赛', page_num=1):
    '''
    :param keyword: 查找的关键词
           page_num: 查询的页数
    :return: 总计博文数量;该页的文本信息
    '''
    based_site = start_site.format(keyword, str(page_num))
    content = requests.get(based_site, headers=headers, verify=False).text
    content_nf = content.encode('UTF-8')
    selector = etree.HTML(content.encode('UTF-8'))
    all_amount_state = selector.xpath('//span[@class="cmt"]/text()')
    if all_amount_state != []:
        all_amount = all_amount_state[0].replace('共', '').replace('条', '')
    else:
        all_amount = 0
        print('查询不到对应的微博信息，请检查关键词！')
    return int(all_amount), content_nf


def scrapy_weibo(content):
    '''
    :param content:爬取页的文本信息
    :return: 所有的字段列表
    '''
    all_id = []
    all_id_name = []
    all_infomation = []
    all_repost = []
    all_repost_site = []
    all_comment = []
    all_comment_site = []
    all_like = []
    all_timetool = []
    all_state = []

    selector = etree.HTML(content)
    # 使用contains进行模糊查询，获取所有博文的匹配值
    item = selector.xpath('//div[contains(@id,"M_")]')
    for elements in item:
        id = elements.xpath('div/a[@class="nk"]/@href')
        id_name = elements.xpath('div/a[@class="nk"]/text()')
        content_state = elements.xpath('div/span[@class="ctt"]')
        each_content = content_state[0].xpath('string(.)')
        info_div = elements.xpath('div')[-1]
        key_state = info_div.xpath('a')
        repost_num = key_state[-3].xpath('string(.)').replace('转发[', '').replace(']', '')
        repost_site = key_state[-3].xpath('@href')[0]
        comment_num = key_state[-2].xpath('string(.)').replace('评论[', '').replace(']', '')
        comment_site = key_state[-2].xpath('@href')[0]
        like_num = key_state[-4].xpath('string(.)').replace('赞[', '').replace(']', '')

        key_state2 = elements.xpath('div/span[@class="ct"]')[0]
        time_tool = key_state2.xpath('string(.)')

        # 将获得的单条博文信息添加进列表中
        all_id.append(id)
        all_id_name.append(id_name)
        all_infomation.append(each_content)
        all_repost.append(repost_num)
        all_repost_site.append(repost_site)
        all_comment.append(comment_num)
        all_comment_site.append(comment_site)
        all_like.append(like_num)
        all_timetool.append(time_tool)

    return all_id, all_id_name, all_infomation, all_repost, all_repost_site, all_comment, all_comment_site, all_like, all_timetool


def main_frame(keyword):
    all_id = []
    all_id_name = []
    all_infomation = []
    all_repost = []
    all_repost_site = []
    all_comment = []
    all_comment_site = []
    all_like = []
    all_timetool = []
    all_timetool = []

    print('开始搜索微博信息!关键词为：' + str(keyword))
    based_data = search_weibo(keyword=str(keyword))
    info_count = int(based_data[0])
    print('博文共计 ' + str(info_count) + ' 条!')
    items_content = based_data[1]
    if info_count == 0:
        print('搜索已停止！')
    elif info_count > 10:
        # 第一页博文信息的爬取
        content_info_set = scrapy_weibo(items_content)
        all_id.extend(content_info_set[0])
        all_id_name.extend(content_info_set[1])
        all_infomation.extend(content_info_set[2])
        all_repost.extend(content_info_set[3])
        all_repost_site.extend(content_info_set[4])
        all_comment.extend(content_info_set[5])
        all_comment_site.extend(content_info_set[6])
        all_like.extend(content_info_set[7])
        all_timetool.extend(content_info_set[8])

        print('第 1 页信息已获取完成！现共计信息 ' + str(len(all_infomation)) + ' 条')
        time.sleep(3)
        # 获取总页数
        page_count = int(info_count / 10) + 1
        # 开始爬取第二页
        if page_count > 50:
            page_count = 50
        for page_index in range(2, page_count + 1):
            items_content2 = search_weibo(keyword=str(keyword), page_num=str(page_index))[1]
            content_info_set2 = scrapy_weibo(items_content2)
            all_id.extend(content_info_set2[0])
            all_id_name.extend(content_info_set2[1])
            all_infomation.extend(content_info_set2[2])
            all_repost.extend(content_info_set2[3])
            all_repost_site.extend(content_info_set2[4])
            all_comment.extend(content_info_set2[5])
            all_comment_site.extend(content_info_set2[6])
            all_like.extend(content_info_set2[7])
            all_timetool.extend(content_info_set2[8])

            print('第 ' + str(page_index) + ' 页信息已获取完成！现共计信息 ' + str(len(all_infomation)) + ' 条')
            time.sleep(3)

    else:
        # 页数<10,只爬取第一页的微博信息
        content_info_set = scrapy_weibo(items_content)
        all_id.extend(content_info_set[0])
        all_id_name.extend(content_info_set[1])
        all_infomation.extend(content_info_set[2])
        all_repost.extend(content_info_set[3])
        all_repost_site.extend(content_info_set[4])
        all_comment.extend(content_info_set[5])
        all_comment_site.extend(content_info_set[6])
        all_like.extend(content_info_set[7])
        all_timetool.extend(content_info_set[8])

        print('第1页信息已获取完成！现共计信息 ' + str(len(all_infomation)) + ' 条')
    print('\n')

    print('开始保存数据!')
    data1 = pd.DataFrame({'id': all_id,
                          'id_name': all_id_name,
                          'content': all_infomation,
                          'repost': all_repost,
                          'repost_site': all_repost_site,
                          'comment': all_comment,
                          'comment_site': all_comment_site,
                          'like': all_like,
                          'time&tool': all_timetool
                          })
    data1.to_excel(u'../weibo-scrapy/comment_{}_test.xls'.format(str(keyword)), index=False, encoding='"utf_8_sig')
    print('信息写入完成！')


if __name__ == '__main__':
    main_frame(input('请输入关键词：'))

# txt= open('../weibo-scrapy/start.txt')
# txt_content=txt.read()
# txt.close()
# selector=etree.HTML(txt_content)
# # page_amount=selector.xpath('')
# 使用contains进行模糊查询，获取所有博文的匹配值
