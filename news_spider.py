# -*- coding: UTF-8 -*-
import requests
import os,base64
import re
import json
import datetime
from datetime import timedelta
import operator
import translators as ts
from io import BytesIO
import yaml
from hoshino import R

class news_class:
    def __init__(self,news_time,news_url,news_title):
        self.news_time = news_time
        self.news_url = news_url
        self.news_title = news_title

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

    res = requests.post(url=url,data=json.dumps(data),headers=headers, timeout=(5,10))
    res_dict = res.json()
    return res_dict

def sort_news():
    res_dict = get_item()
    news_list = []
    for n in range(0, 5):
        if (res_dict['information_list'][n]['update_at'] == None):
            news_time = res_dict['information_list'][n]['post_at']
        else :
            news_time = res_dict['information_list'][n]['update_at']

        news_id = res_dict['information_list'][n]['announce_id']
        news_url = '▲https://umamusume.jp/news/detail.php?id=' + str(news_id)
        news_title = res_dict['information_list'][n]['title']
        news_list.append(news_class(news_time, news_url ,news_title))

    news_key = operator.attrgetter('news_time')
    news_list.sort(key = news_key, reverse = True)
    return news_list

def get_news():
    news_list = sort_news()
    msg = '◎◎ 马娘官网新闻 ◎◎\n'
    for news in news_list:
        time_tmp = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        news_time = time_tmp - timedelta(hours=1)
        msg = msg + '\n' + str(news_time) + '\n' + news.news_title + '\n' + news.news_url + '\n'
    return msg

def news_broadcast():
    news_list = sort_news()
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    init_time = str(file.read())
    file.close()
    init_time = datetime.datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    msg = '◎◎ 马娘官网新闻更新 ◎◎\n'
    for news in news_list:
        prev_time = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        if (init_time >= prev_time):
            break
        else:
            time_tmp = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
            news_time = time_tmp - timedelta(hours=1)
            msg = msg + '\n' + str(news_time) + '\n' + news.news_title + '\n' + news.news_url + '\n'

    for news in news_list:
        set_time = news.news_time
        break
    file = open(current_dir, 'w', encoding="UTF-8")
    file.write(str(set_time))
    file.close()
    return msg

# 判断一下是否有更新，为什么要单独写一个函数呢
# 函数单独写一个是怎么回事呢？函数相信大家都很熟悉，但是函数单独写一个是怎么回事呢，下面就让小编带大家一起了解吧。
# 函数单独写一个，其实就是我想单独写一个函数，大家可能会很惊讶函数怎么会单独写一个呢？但事实就是这样，小编也感到非常惊讶。
# 这就是关于函数单独写一个的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！
def judge() -> bool:
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    if (os.path.exists(current_dir) == True):
        file = open(current_dir, 'r', encoding="UTF-8")
        init_time = str(file.read())
        file.close()
    else:
        news_list = sort_news()
        for news in news_list:
            init_time = news.news_time
            break
        current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
        file = open(current_dir, 'w', encoding="UTF-8")
        file.write(str(init_time))
        file.close()

    news_list = sort_news()
    for news in news_list:
        prev_time = news.news_time
        break
    
    if (init_time != prev_time):
        return True
    else:
        return False

# 替换不必要的文本
def replace_text(text_tmp):
    # 替换多余的html关键字
    text = text_tmp.replace('&nbsp;', ' ')
    text = text.replace('<br>', '\n')
    text = text.replace('</div>', '\n')
    text = text.replace('<div class="postscript-01">', '')
    text = re.sub(r'<span.+?>', '', text)
    text = text.replace('</span>', '')
    text = text.replace('<span title=\"\">', '')
    text = text.replace('<strong>', '')
    text = text.replace('</strong>', '')
    text = text.replace('<h2 class="heading">', '\n\n')
    text = text.replace('<h3 class="subheading">', '\n\n')
    text = text.replace('</h2>', '\n\n')
    text = text.replace('</h3>', '\n\n')
    text = text.replace('<h3>', '\n\n')
    text = re.sub(r'<figure>.+?<\/figure>', '', text)
    # 替换赛马娘游戏术语
    current_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    file = open(current_dir, 'r', encoding = 'UTF-8')
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader = yaml.FullLoader)
    keys_list = list(config.keys())
    for key in keys_list:
        value = config[key]
        text = text.replace(f'{key}', f'{value}')
    return text

# 翻译完如果把中文又翻译一遍导致出问题可以在这里，再次替换一下？
def second_replace(news_text):
    # news_text = news_text.replace('', '') # 我先注释了
    return news_text

# 翻译新闻
def translate_news(news_id):
    url = 'https://umamusume.jp/api/ajax/pr_info_detail?format=json'
    data = {}
    data['announce_id'] = news_id
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
    }
    flag = 0
    try:
        res = requests.post(url=url,data=json.dumps(data),headers=headers, timeout=(5,10))
        res_dict = res.json()
        if res_dict['detail']['title'] == '現在確認している不具合について':
            news_msg = res_dict['detail']['message'][:500] + '...'
            flag = 1
        else:
            news_msg = res_dict['detail']['message']
        news_msg = replace_text(news_msg)
    except:
        news_text = '错误！马娘官网连接失败'
        return news_text
    try:
        news_text = ts.youdao(news_msg, 'ja', 'zh-CN')
        news_text = second_replace(news_text)
        if flag == 1:
            news_text = '(该新闻特别长，因此只显示前500个字符)\n\n' + news_text
        if res_dict['detail']['image_big'] != '':
            img_url = res_dict['detail']['image_big']
            response = requests.get(img_url)
            ls_f = base64.b64encode(BytesIO(response.content).read())
            imgdata = base64.b64decode(ls_f)
            save_dir = R.img('umamusume_news').path
            path_dir = os.path.join(save_dir,'news_img.jpg')
            file = open(path_dir,'wb')
            file.write(imgdata)
            file.close()
            news_img = ' '.join(map(str, [
                R.img(f'umamusume_news/news_img.jpg').cqcode,
            ]))
            news_text = f'{news_img}' + news_text
    except:
        # 用于检查错误
        print('error_check --> news_msg: ' + news_msg)
        news_text = '错误！翻译失败！'
    return news_text
