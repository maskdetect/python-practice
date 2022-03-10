import json
import requests
from bs4 import BeautifulSoup
import os
from matplotlib import pyplot as plt
import pandas as pd


def crawl_wiki_data2():
    """
    爬取百度百科中《乘风破浪的姐姐》中嘉宾信息，返回html
    """
    headers = {
        "authority": "www.zhihu.com",
        "method": "POST",  # post好牛逼啊
        "scheme": "https",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": '_zap=4b8fd0b0-5ece-4710-8a39-4690be3cc915; d_c0="ACDn4-HhLA-PTloTkzkSI1g9NSQ0UNbecnY=|1553490041"; _xsrf=iqWraCpzOAEVVHNZGwDfyaUPzBb7lkuI; z_c0="2|1:0|10:1553513989|4:z_c0|92:Mi4xTHpaZUJBQUFBQUFBSU9majRlRXNEeVlBQUFCZ0FsVk5CUXlHWFFCVjdwTFIwbjFVeXdZWmREdDVybTVvVWtVa0NR|e97ba19d5423a0bb2269441eb310b80853aaed3e4cfdcd555c5b4517e681824d"; __gads=ID=ef86bad0aef0dc13:T=1553514097:S=ALNI_MaIcscAZVawHrwdA_5OzAq3gGMLfg; __utmv=51854390.100-1|2=registration_date=20170314=1^3=entry_date=20170314=1; _ga=GA1.2.1820027566.1554478077; tst=r; q_c1=c09535e464704c7e8aa93032d032f507|1556906107000|1553490042000; __utma=51854390.1820027566.1554478077.1555816095.1556906108.7; __utmz=51854390.1556906108.7.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; tgw_l7_route=060f637cd101836814f6c53316f73463',
        # 方便登录
        "origin": "https://www.zhihu.com",
        "referer": "https://www.zhihu.com/topic",  # 来源自哪里
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",  # 为 XMLHttpRequest，则为 Ajax 异步请求！
        "x-xsrftoken": "iqWraCpzOAEVVHNZGwDfyaUPzBb7lkuI",  # 反验证功能
        "_xsrf": "697157726143707a4f41455656484e5a47774466796155507a4262376c6b7549"  # 页面校检码，是来检查你是否是从正常的登录页面过来的
    }
    url = 'https://baike.baidu.com/item/乘风破浪的姐姐第二季'

    try:
        response = requests.get(url, headers=headers)
        # 将一段文档传入BeautifulSoup的构造方法,就能得到一个文档的对象, 可以传入一段字符串
        soup = BeautifulSoup(response.text, 'html.parser')

        # 返回所有的<table>所有标签
        tables = soup.find_all('table')
        # print(tables)

        crawl_table_title = "按姓氏首字母排序"
        table_attress = [];
        for table in tables:
            # 对当前节点前面的标签和字符串进行查找
            table_titles = table.find_previous('div')
            # print (1,table_titles)
            for title in table_titles:
                if (crawl_table_title in title):
                    # print (table)
                    table_attress.append(table)
                    # return table
        return table_attress
    except Exception as e:
        print(e)


def parse_wiki_data(table_html):
    '''
    解析得到选手信息，包括包括选手姓名和选手个人百度百科页面链接，存JSON文件,保存到work目录下
    '''
    bs = BeautifulSoup(str(table_html), 'html.parser')
    all_trs = bs.find_all('tr')

    stars = []
    for tr in all_trs:
        all_tds = tr.find_all('td')  # tr下面所有的td

        for td in all_tds:
            # star存储选手信息，包括选手姓名和选手个人百度百科页面链接
            star = {}
            if td.find('a'):
                # 找选手名称和选手百度百科连接
                if td.find_next('a'):
                    star["name"] = td.find_next('a').text
                    # print(len(td.find_next('a').text),td.find_next('a').text)
                    star['link'] = 'https://baike.baidu.com' + td.find_next('a').get('href')

                elif td.find_next('div'):
                    # print(len(td.find_next('div').find('a').text),td.find_next('div').find('a').text)
                    star["name"] = td.find_next('div').find('a').text
                    star['link'] = 'https://baike.baidu.com' + td.find_next('div').find('a').get('href')
                # print(len(star["name"]),star["name"])
                if (star["name"] != " "):
                    stars.append(star)

    json_data = json.loads(str(stars).replace("\'", "\""))
    with open('work/' + 'stars1.json', 'w', encoding='UTF-8') as f:
        json.dump(json_data, f, ensure_ascii=False)


def crawl_everyone_wiki_urls():
    '''
    爬取每个选手的百度百科图片，并保存
    '''
    with open('work/' + 'stars1.json', 'r', encoding='UTF-8') as file:
        json_array = json.loads(file.read())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    star_infos = []
    for star in json_array:
        star_info = {}
        name = star['name']
        if (ord(name[0]) == 10):
            continue
        link = star['link']
        star_info['name'] = name
        # 向选手个人百度百科发送一个http get请求
        response = requests.get(link, headers=headers)
        # 将一段文档传入BeautifulSoup的构造方法,就能得到一个文档的对象
        bs = BeautifulSoup(response.text, 'html.parser')
        # 获取选手的民族、星座、血型、体重等信息
        base_info_div = bs.find('div', {'class': 'basic-info J-basic-info cmn-clearfix'})
        dls = base_info_div.find_all('dl')

        for dl in dls:
            dts = dl.find_all('dt')
            for dt in dts:
                if "".join(str(dt.text).split()) == '民族':
                    star_info['nation'] = dt.find_next('dd').text
                if "".join(str(dt.text).split()) == '星座':
                    star_info['constellation'] = dt.find_next('dd').text
                if "".join(str(dt.text).split()) == '血型':
                    star_info['blood_type'] = dt.find_next('dd').text
                if "".join(str(dt.text).split()) == '身高':
                    height_str = str(dt.find_next('dd').text)
                    star_info['height'] = str(height_str[0:height_str.rfind('cm')]).replace("\n", "")
                if "".join(str(dt.text).split()) == '体重':
                    star_info['weight'] = str(dt.find_next('dd').text).replace("\n", "")
                if "".join(str(dt.text).split()) == '出生日期':
                    birth_day_str = str(dt.find_next('dd').text).replace("\n", "")
                    if '年' in birth_day_str:
                        star_info['birth_day'] = birth_day_str[0:birth_day_str.rfind('年')]
        star_infos.append(star_info)

        # 从个人百度百科页面中解析得到一个链接，该链接指向选手图片列表页面
        if bs.select('.summary-pic a'):
            pic_list_url = bs.select('.summary-pic a')[0].get('href')
            pic_list_url = 'https://baike.baidu.com' + pic_list_url

            # 向选手图片列表页面发送http get请求
            pic_list_response = requests.get(pic_list_url, headers=headers)

            # 对选手图片列表页面进行解析，获取所有图片链接
            bs = BeautifulSoup(pic_list_response.text, 'html.parser')
            pic_list_html = bs.select('.pic-list img ')
            pic_urls = []
            for pic_html in pic_list_html:
                pic_url = pic_html.get('src')
                pic_urls.append(pic_url)
                # 根据图片链接列表pic_urls, 下载所有图片，保存在以name命名的文件夹中
                down_save_pic(name, pic_urls)
        # 将个人信息存储到json文件中

        json_data = json.loads(str(star_infos).replace("\'", "\"").replace("\\xa0", ""))
        with open('work/' + 'stars_info1.json', 'w', encoding='UTF-8') as f:
            json.dump(json_data, f, ensure_ascii=False)


def down_save_pic(name, pic_urls):
    '''
    根据图片链接列表pic_urls, 下载所有图片，保存在以name命名的文件夹中,
    '''
    path = 'work/' + 'pics/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(pic_url, timeout=15)
            string = str(i + 1) + '.jpg'
            with open(path + string, 'wb') as f:
                f.write(pic.content)
                # print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            # print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue


def draw():
    # 显示matplotlib生成的图形

    df = pd.read_json('work/stars_info1.json')
    print(df)
    weights = df['height']
    arrs = weights.values

    arrs = [x for x in arrs if not pd.isnull(x)]
    # pandas.cut用来把一组数据分割成离散的区间。比如有一组年龄数据，可以使用pandas.cut将年龄数据分割成不同的年龄段并打上标签。bins是被切割后的区间.
    bin = [0,164,169,1000]
    se1 = pd.cut(arrs, bin)
    #print(se1)

    # pandas的value_counts()函数可以对Series里面的每个值进行计数并且排序。
    pd.value_counts(se1)

    sizes = pd.value_counts(se1)
    #print(sizes)
    labels = '<165', '165~169', '>=170'

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('''《乘风破浪的姐姐》参赛嘉宾体重饼状图''',fontsize = 24)
    plt.savefig('/home/aistudio/work/result/pie_result02.jpg')
    plt.show()


if __name__ == '__main__':
    # 爬取百度百科中《乘风破浪的姐姐》中参赛选手信息，返回html
    htmls = crawl_wiki_data2()
    #print(htmls)
    # #解析html,得到第一季选手信息，保存为json文件
    parse_wiki_data(htmls[0])
    # #从每个选手的百度百科页面上爬取,并保存
    #crawl_everyone_wiki_urls()

    print("所有信息爬取完成！")

    draw()
