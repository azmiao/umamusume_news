import os
import hoshino
from hoshino import Service, R, priv
from hoshino.typing import *
from hoshino.util import FreqLimiter, concat_pic, pic2b64, silence
from .news_spider import *

sv_help = '''
=====功能=====
[马娘新闻] 查看最近五条新闻

（自动推送） 该功能没有命令
'''.strip()

sv = Service('umamusume_news', help_=sv_help, enable_on_default=True, bundle='马娘新闻订阅')
svuma = Service('umamusume-news-poller', enable_on_default=False, help_='马娘新闻播报')

# 帮助界面
@sv.on_fullmatch("马娘新闻帮助")
async def help(bot, ev):
    await bot.send(ev, sv_help)

# 主动获取新闻功能
@sv.on_fullmatch(('马娘新闻','赛马娘新闻'))
async def uma_news(bot, ev):
    await bot.send(ev, get_news())

# 马娘新闻播报
@svuma.scheduled_job('cron', minute='*/5')
async def uma_news_poller():
    if (judge() == True):
        print('检测到马娘新闻更新！')
        await svuma.broadcast(news_broadcast(), 'umamusume-news-poller', 0.2)
    else:
        print('暂未检测到马娘新闻更新')
        return