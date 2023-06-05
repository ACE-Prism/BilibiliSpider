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

n = 'Prism'
url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=13188752&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=9fb9e08c9b7d75b29bbd731e7bc67a9d&wts=1685805913']

# n = '考研数学武忠祥老师'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=6e8b3c578daee21482a0fcf06706d624&wts=1685767628',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=22e7e6e05c5bb419aa2ad4e5486d7128&wts=1685767688',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=f60d9052661d4334e6606b9a1befee70&wts=1685767716',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=4&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=8924e37352fe5311dedea33ea4a95c5b&wts=1685767732',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=5&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=ace96857d96320528b10851a08e6decb&wts=1685767749',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=6&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=78460f2a420ffb9ad29777adbe457612&wts=1685767758',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=7&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=25dc2795bbccae5268c9a09c05774a88&wts=1685767766',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=8&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=32f05bca43838569572a907906c87436&wts=1685767790',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=9&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=2cf939251b678578c2f4f6bf1d336d38&wts=1685767806',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=10&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=0084458f8b03ac6c4390d70a63db2f68&wts=1685767816',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=11&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=cf3a1207be774e4f05452d77f10a2c03&wts=1685767826',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=12&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=be209e5df9f092a116940a7d504d8034&wts=1685767851',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=13&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=bc3f045b5d79f327d21008c985720276&wts=1685767860',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=14&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=2fec2745a4ce704b22b89addf26c1415&wts=1685767868',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=15&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=91b8c755ed3ec7260c74f54d5f2e4477&wts=1685767880',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=16&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=f176283f5d4cfc8d7ab9668fe74d57c2&wts=1685767896',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=17&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=15fdddde0c42a20e2310fcf57df99f70&wts=1685767905',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=18&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=b5b04748c05f4f9b4b540e28b747c074&wts=1685767924',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=19&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=b8b75216888c44bcf92a616ef61f81a5&wts=1685767951',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=20&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=ac3571d95514efe310b73ef7aefa7fdd&wts=1685767961',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=21&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=8a7b8c7a3edfdaa6e8f459906af3c2b2&wts=1685767975',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=22&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=c7b683bfd104d174afc2d9a8d971164b&wts=1685767992',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=23&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=1322fce12afb59a647f6d6320c3fd478&wts=1685768005',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=24&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=4ad55646976a1e6030ca87f11784fe19&wts=1685768016',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=25&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=b7ba96f79adfb6bcd92c6057cbf13f14&wts=1685768026',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=26&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=218a83ac7c91e71c215a42fb2a1c5188&wts=1685768048',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=27&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=425e7ed0cfdb4c85284a98bb5e59d6d3&wts=1685768070',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=28&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=3f2210b5c64932c52843b3cd579e9f42&wts=1685768080',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=29&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=8d88275479f446d7b948f15a0de446e3&wts=1685768092',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=30&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=ea459258e20b74b927e51e1f56fe9399&wts=1685768104',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=31&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=aa1479987177529d334a7aa475159ded&wts=1685768118',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=32&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=de8a6bedfb44e9553e0ebe19d6a62c13&wts=1685768128',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=33&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=3e8f5401697b9c10d86d6a9fda248420&wts=1685768141',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=34&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=6a95241fea7f8a266e54213173647993&wts=1685768151',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=35&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=e195166f090fa4c26553d16a5442093a&wts=1685768175',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=36&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=ab526de4224521b3062c59f727acbaaa&wts=1685768187',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=37&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=7617adabec52911c6c010ba0cf79f91d&wts=1685768199',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=38&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=26ec3b771be073c6887b1201f348b161&wts=1685768217',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=39&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=2c14cbe1d5721b87d303cac58fdc5ccf&wts=1685768227',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=688379639&ps=30&tid=36&special_type=&pn=40&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=2094287b12cff241813884acab388ca1&wts=1685768239']

# n = '宋浩老师官方'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=66607740&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=6bed76f456e711ab3768ccd17edcadd8&wts=1685767087',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=66607740&ps=30&tid=36&special_type=&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=e9bc9eea87965f10b1709126808fb08a&wts=1685767104']

# n = '数学建模学习交流'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=52614961&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=c1b44562f8f17b94d6bc7b243ae57385&wts=1685766830',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=52614961&ps=30&tid=36&special_type=&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=1153ddf6240a189d3ff1ec92ae1b7c3e&wts=1685766840',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=52614961&ps=30&tid=36&special_type=&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=50f732141c9c950ae0f579f4537bf2ae&wts=1685766849',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=52614961&ps=30&tid=36&special_type=&pn=4&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=97a08eb334b2cc1a7210665ee2647012&wts=1685766858']

# n = '考研竞赛凯哥'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=1d469e866eb6eeddba0cbbdb45ff0ed5&wts=1685766510',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=0c77eb770705d400f8695bebe7446e1f&wts=1685766522',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=a10cdb8dfc8ce458050642a890bca99c&wts=1685766545',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=4&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=1d3b4259fa173f35fa5e3de6cee48ba5&wts=1685766558',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=5&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=cdb7462987d595ad0b60e4d1007e0a27&wts=1685766570',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=6&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=e8933b2b88f939971d8b9bf99c8a5614&wts=1685766584',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=7&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=dd0eb66c081e65140453b2f28b79bb46&wts=1685766622',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=8&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=d3ecf27c747791ae3fdb0ca82412cf91&wts=1685766639',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=9&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=5539b7ec85ba95e81ee2fbf08511289c&wts=1685766649',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=10&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=9e3e9a38fbe923160b9facfa5957ef00&wts=1685766660',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=11&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=7a0b6a163be7a538546871562928f1b9&wts=1685766687',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=12&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=cc3af2b1a075ed49928a5028f84075bf&wts=1685766701',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=13&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=40f726a92779b0c61982710d27056143&wts=1685766713',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=42428180&ps=30&tid=36&special_type=&pn=14&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=54aef91cee427fb9da800c89aaf17830&wts=1685766727']

# n = '考研数学不将就'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=628479407&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=7b1c315a1113eba69a98cb6e712c3c05&wts=1685766414',]

# n = '聆歌学长Egregium'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=123667802&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=52b5b74fb99e1c1aa4c9acc6f94f261b&wts=1685766208',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=123667802&ps=30&tid=36&special_type=&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=256727daa112749cacf39220a780ed91&wts=1685766258',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=123667802&ps=30&tid=36&special_type=&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=de27d19f44222370a77ec10d35ff95e0&wts=1685766272',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=123667802&ps=30&tid=36&special_type=&pn=4&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=76b37da62d6e780ff67b9567874977c2&wts=1685766287',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=123667802&ps=30&tid=36&special_type=&pn=5&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=c59d5e0b3c0a2a27e5bb4d802b301f73&wts=1685766303',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=123667802&ps=30&tid=36&special_type=&pn=6&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=db855e3c69b967789256e846e5d4dc38&wts=1685766316']

# n = 'SCHEME_maths'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=361732174&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=cf749995284081ac3514c4f3e492a767&wts=1685766076',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=361732174&ps=30&tid=0&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=2130ec55ae0df70c222e9a6b1dbb8490&wts=1685766092',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=361732174&ps=30&tid=0&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=f26104dbc7c4fe1608a51950f4c1cb70&wts=1685766133']

# n = '沉迷学习的PickleFermi'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=8b24c7c83614f392d60df36037c35ce4&wts=1685765710',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=1a3ddafa1e91a18bc073db0c4fee3342&wts=1685765900',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=90a27e2bf24f7fd53228d2a0cefa8c36&wts=1685765929',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=4&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=df3bd2311031853c74c862e62c3fe010&wts=1685765961',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=5&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=6f784998fad597ee3a93134015e98b2f&wts=1685765973',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=6&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=6068ab531d059f8149c38ee6f0b3b5fe&wts=1685765984',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=7&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=b451c2433ffbbef4a518e0835591f525&wts=1685765995',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=8&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=5d3a52950584a124c14be858ada2bc27&wts=1685766006',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=9&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=c0d5eb3b7ddd99698254d56bf5132dec&wts=1685766021',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=85609159&ps=30&tid=36&special_type=&pn=10&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=1f9ba7d38c19ee6585a3016cc3fe649d&wts=1685766032']

# n = '熤熤的名字就是意义'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=756155&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=474833ddbe6b8a07a73662d4e578c34a&wts=1685764727',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=756155&ps=30&tid=0&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=76089aea91b65e357043ce2ee94147cc&wts=1685764776']

# n = '夜雨教你考研竞赛'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=a9ea45b195e0ef318af5bcb9e9d33240&wts=1685764971',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=2&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=a768a7827cf7509b411b85f7f38f754f&wts=1685765007',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=3&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=26b08526f7f109b90fe1fda7e5ad62ac&wts=1685765032',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=4&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=c37ea77374199155b5afb03ca5baf444&wts=1685765048',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=5&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=627316936236ca68948b7647151627f4&wts=1685765071',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=6&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=627684078e1445a36e6d27bf1d461445&wts=1685765089',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=7&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=9a2c53b0274618080e9e4adf34ca26fe&wts=1685765103',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=8&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=3b51e39c6ef645498ce862762d1bd22f&wts=1685765117',
# 'https://api.bilibili.com/x/space/wbi/arc/search?mid=25327929&ps=30&tid=0&pn=9&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=6c6e5ea1585e30932a3d1b081372b6ee&wts=1685765116']

# n = 'kumiko想要学分析'
# url = ['https://api.bilibili.com/x/space/wbi/arc/search?mid=3156848&ps=30&tid=36&special_type=&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=6e0daffa8565410dc09b115eb5ef6c59&wts=1685628349']

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