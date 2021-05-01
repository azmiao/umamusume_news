# -*- coding: UTF-8 -*-
import requests
import os
import json

def get_item():
    url = 'https://umamusume.jp/api/ajax/pr_info_index?format=json'
    data = {}
    data['announce_label'] = 0
    data['limit'] = 10
    data['offset'] = 0
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
    }

    res = requests.post(url=url,data=json.dumps(data),headers=headers)
    # 气死我了，昨晚这里因为传递参数打错了一个字，导致一直无返回数据，整到了凌晨3点没整明白，果然半夜脑子不好使
    res_dict = res.json()
    return res_dict

def get_news():
    res_dict = get_item()

    current_dir = os.path.join(os.path.dirname(__file__), 'prev_id.yml')
    # current_dir = 'prev_id.yml'
    file = open(current_dir, 'r', encoding="UTF-8")
    init_id = int(file.read())
    file.close()

    msg = '◎◎ 马娘官网新闻 ◎◎\n'
    for m in range(0, 4):
        if (init_id == res_dict['information_list'][m]['announce_id'] or m == 4):
            for n in range(m, m + 5):
                news_id = res_dict['information_list'][n]['announce_id']
                news_url = '▲https://umamusume.jp/news/detail.php?id=' + str(news_id)
                news_title = res_dict['information_list'][n]['title']
                msg = msg + '\n' + news_title + '\n' + news_url
            break
    return msg

def get_prev_id():
    res_dict = get_item()
    prev_id = res_dict['information_list'][0]['announce_id']
    # print(prev_id)
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_id.yml')
    # current_dir = 'prev_id.yml'
    file = open(current_dir, 'w', encoding="UTF-8")
    file.write(str(prev_id))
    file.close()

def news_broadcast():
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_id.yml')
    # current_dir = 'prev_id.yml'
    file = open(current_dir, 'r', encoding="UTF-8")
    init_id = int(file.read())
    file.close()

    res_dict = get_item()
    prev_id = res_dict['information_list'][0]['announce_id']
    if (int(prev_id) == init_id):
        return
    msg = '◎◎ 马娘官网新闻更新 ◎◎\n'
    for n in range(0, 10):
        if (int(prev_id) != init_id):
            news_id = res_dict['information_list'][n]['announce_id']
            news_url = '▲https://umamusume.jp/news/detail.php?id=' + str(news_id)
            news_title = res_dict['information_list'][n]['title']
            prev_id = res_dict['information_list'][n+1]['announce_id']
            msg = msg + '\n' + news_title + '\n' + news_url
        else:
            break
    
    # print(msg)
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_id.yml')
    # current_dir = 'prev_id.yml'
    file = open(current_dir, 'w', encoding="UTF-8")
    file.write(str(res_dict['information_list'][0]['announce_id']))
    file.close()
    return msg

# 判断一下是否有更新，为什么要单独写一个函数呢
# 函数单独写一个是怎么回事呢？函数相信大家都很熟悉，但是函数单独写一个是怎么回事呢，下面就让小编带大家一起了解吧。
# 函数单独写一个，其实就是我想单独写一个函数，大家可能会很惊讶函数怎么会单独写一个呢？但事实就是这样，小编也感到非常惊讶。
# 这就是关于函数单独写一个的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！
def judge() -> bool:
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_id.yml')
    # current_dir = 'prev_id.yml'
    file = open(current_dir, 'r', encoding="UTF-8")
    init_id = int(file.read())
    file.close()

    res_dict = get_item()
    prev_id = res_dict['information_list'][0]['announce_id']

    if (int(prev_id) != init_id):
        return True
    else:
        return False
# get_prev_news()
# news_broadcast()