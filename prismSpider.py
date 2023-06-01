import re

import xlwt

import requests

book = xlwt.Workbook(encoding='utf-8', style_compression=0)

# 输入自己的UA头，也许会与作者的不同，在F12-->network的文件里查找。
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

# 可以自己填充新的ID与链接，要用哪个就把其他的注释掉，把当前的取消注释。n是你想要的UP主昵称，随意填写。
# 进入UP主空间后在F12-->network中通过查询任意视频标题中关键词得到一个文件，大概是search?mid开头，在Headers-->General-->Request URL里把url复制过来，每翻一页都不同，有几页就几个。
# 以下举例：

# n = ''
# url = ['',
# '']

# n = ''
# url = ['',
# '']

# n = ''
# url = ['',
# '',
# '']

n = 'kumiko想要学分析'
url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=3156848&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=6e0daffa8565410dc09b115eb5ef6c59&wts=1685628349']

# n = '究尽数学'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=233679844&ps=30&tid=0&special_type=&pn=1&keyword=&order=click&platform=web&web_location=1550101&w_rid=186c3b21b3d8f9b233a8bc8eb49b4d0b&wts=1685627924',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=233679844&ps=30&tid=0&special_type=&pn=2&keyword=&order=click&platform=web&web_location=1550101&w_rid=d77cfbca384bd2141e4ca4a22b9c0e10&wts=1685627969',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=233679844&ps=30&tid=0&special_type=&pn=3&keyword=&order=click&platform=web&web_location=1550101&w_rid=3a733f169f671cb65c6b7e72d700d039&wts=1685627992',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=233679844&ps=30&tid=0&special_type=&pn=4&keyword=&order=click&platform=web&web_location=1550101&w_rid=b8a1c43811c670236693afcdb0ca85dd&wts=1685628012',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=233679844&ps=30&tid=0&special_type=&pn=5&keyword=&order=click&platform=web&web_location=1550101&w_rid=94cad41290a335331dcec9f08cbe39f7&wts=1685628064']

# n = '马同学图解数学'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=355876061&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=ec66cd527da1f7ef9c4dc6abdb7b331a&wts=1685627664',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=355876061&ps=30&tid=0&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=7a49a52a6fb8cc6be0a6d77f9e2bf002&wts=1685627701']

# n = '两颗熟李子'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=594380494&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=55c66b0415b711360e25a9d1d620a6dc&wts=1685627549']

# n= '轩兔'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=20883932&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=fdd0009a12307f3cb7e781c63cd4b509&wts=1685627286',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=20883932&ps=30&tid=36&special_type=&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=fe23bde4e147a2e76e4ab878c64e6250&wts=1685627374']

# n = 'Solara570'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=3557916&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=60c7d113fba35856a558ed1b3f3dd0cb&wts=1685625921',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=3557916&ps=30&tid=36&special_type=&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=49696d5039d99dd02b9b606fc38a34a3&wts=1685625936']

# n = '遇见数学'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=89225756&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=decd10f2cdf03c6ee9c63d692acd3960&wts=1685626165',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=89225756&ps=30&tid=0&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=3e460e56eab01cf5d597a0e09b14eb63&wts=1685626232',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=89225756&ps=30&tid=0&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=cb0a03a229fb3c3fdf484196627bb41f&wts=1685626275',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=89225756&ps=30&tid=0&pn=4&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=adcad68d9c996d7574ca2c20336eba62&wts=1685626324',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=89225756&ps=30&tid=0&pn=5&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=729c9684da25add9bb04237cb64d1834&wts=1685626356',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=89225756&ps=30&tid=0&pn=6&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=55a8def1d76f052f57d7c52ad8cd8ae8&wts=1685626368',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=89225756&ps=30&tid=0&pn=7&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=baa9cdac29c542995fd9f4b5ae1dcce6&wts=1685626383']

# n = '数心'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=346660989&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=0fd67fed1e2310cd2217f64e7574056a&wts=1685626460']

# n = '中国数学会'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=1012693747&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=1efbcd812beb30c7f77c680d9828714a&wts=1685612808']

# n = '3B1B'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=88461692&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=0be4ee191422ceaabb93b6dc8c71878f&wts=1685607477',
#        'https://api.bilibili.com/x/space/wbi/arc/search?mid=88461692&ps=30&tid=0&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=4f9c4689d27e956fb9bb0b5e01bd71bb&wts=1685607543',
#        'https://api.bilibili.com/x/space/wbi/arc/search?mid=88461692&ps=30&tid=0&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=b447b5e0fd77c89a5f2731244391e2c7&wts=1685611902',
#        'https://api.bilibili.com/x/space/wbi/arc/search?mid=88461692&ps=30&tid=0&pn=4&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=3dfc2c536f4355ad84340a58f34d4c06&wts=1685611925']


sheet = book.add_sheet(f'{n}', cell_overwrite_ok=True)

# 可自由调整数据维度
col = ('标题', '播放', '点赞', '投币', '收藏', '弹幕', '评论', '分享')

for i in range(0, 8):
    sheet.write(0, i, col[i])

row = 1

pages = len(url)

for i in range(pages):

    response = requests.get(url=url[i], headers=headers)

    for index in response.json()['data']['list']['vlist']:

        bvid = index['bvid']
        url2 = f'https://www.bilibili.com/video/{bvid}'

        response2 = requests.get(url=url2, headers=headers, timeout=2)

        #   [0]列表类型转为字符串
        title = re.findall('"title":"(.*?)","pubdate"', response2.text)[0]
        # 去除多余的\，补上多去除的\
        title = title.replace('\\', '')
        title = title.replace('u002f', '\u002f')

        view = re.findall('"view":(.*?),"danmaku"', response2.text)[0]

        danmaku = re.findall('"danmaku":(.*?),"reply"', response2.text)[0]

        reply = re.findall('"reply":(.*?),"favorite"', response2.text)[0]

        favorite = re.findall('"favorite":(.*?),"coin"', response2.text)[0]

        coin = re.findall('"coin":(.*?),"share"', response2.text)[0]

        share = re.findall('"share":(.*?),"now_rank"', response2.text)[0]

        like = re.findall('"like":(.*?),"dislike"', response2.text)[0]

        print('标题:', title)
        sheet.write(row, 0, title)

        print('播放:', view)
        sheet.write(row, 1, view)

        print('点赞:', like)
        sheet.write(row, 2, like)

        print('投币:', coin)
        sheet.write(row, 3, coin)

        print('收藏:', favorite)
        sheet.write(row, 4, favorite)

        print('弹幕:', danmaku)
        sheet.write(row, 5, danmaku)

        print('评论:', reply)
        sheet.write(row, 6, reply)

        print('分享:', share)
        sheet.write(row, 7, share)

        row += 1

        # time.sleep(0.1)

# 自定义保存路径与文件名
savepath = f'E:\Dissertation\Data of {n}.xls'

book.save(savepath)