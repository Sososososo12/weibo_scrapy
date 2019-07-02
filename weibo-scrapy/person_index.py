from lxml import etree
import requests
import time
import pandas as pd
import xlrd

start_site = 'https://weibo.cn/{}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie': 'SCF=ApUALGl5o2wQZBDEzzMpnkGUO_OEfMiAuO8L4uvywo-Qq1UmAIG7nzOa2WPlftUWSyyuXvFrE7PmFBBAjXLI_Ug.; SUB=_2A25wHrWLDeRhGeBN4lcQ9irEyTqIHXVT4NvDrDV6PUJbkdAKLUL5kW1NRAY1GGVLmHMHYEoOOXNt-U6wOMN6luhA; SUHB=0D-FVI9EeEaRPU; MLOGIN=1; _T_WM=82867258802; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D2019%25E7%258E%25AF%25E9%259D%2592%25E6%25B5%25B7%25E6%25B9%2596%25E8%2587%25AA%25E8%25A1%258C%25E8%25BD%25A6%25E8%25B5%259B%2526t%253D0; WEIBOCN_FROM=1110106030'
}


def get_user_id():
    filename = r'../weibo-scrapy/comment_2019_07_02_test.xls'
    data = xlrd.open_workbook(filename=filename)
    sheet1 = data.sheet_by_index(0)
    race_id_set = sheet1.col_values(3)
    race_id_set.remove('id')
    # print(race_id_set)
    return race_id_set


def get_person_info(user_id='tdql'):
    based_site = start_site.format(str(user_id))
    content = requests.get(based_site, headers=headers, verify=False).text
    selector = etree.HTML(content.encode('UTF-8'))
    items = selector.xpath('//div[@class="tip2"]')
    # 通过items的存在判断网页是否加载正确
    if items != []:
        state = 1
        content_count = items[0].xpath('span/text()')[0].replace('微博[', '').replace(']', '')
        follow_count = items[0].xpath('a/text()')[0].replace('关注[', '').replace(']', '')
        fans_count = items[0].xpath('a/text()')[1].replace('粉丝[', '').replace(']', '')
    else:
        state = 0
        content_count = 0
        follow_count = 0
        fans_count = 0
        print('网页加载失败，请重新尝试!')
    return content_count, follow_count, fans_count, state


content_count = []
follow_count = []
fans_count = []
state = []

user_set = get_user_id()
for user in user_set:
    if type(user)==type(120.0):
        user=str(int(user))
    user_info = get_person_info(user)
    content_count.append(user_info[0])
    follow_count.append(user_info[1])
    fans_count.append(user_info[2])
    state.append(user_info[3])
    print('已爬取用户：' + user + ' 信息')
    time.sleep(3)

print('开始保存数据!')
data1 = pd.DataFrame(
    {'user_id':user_set,
     'content_count':content_count,
     'follow_count':follow_count,
     'fans_count':fans_count,
     'state':state
                      })
data1.to_excel(u'../weibo-scrapy/user_info_test.xls', index=False, encoding='"utf_8_sig')
print('信息写入完成！')

get_person_info()
