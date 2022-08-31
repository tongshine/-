import json
import requests
import re
import csv

with open('taobao2.csv', 'w' , encoding='ANSI',newline='') as filename:
    csvwriter = csv.DictWriter(filename, fieldnames=['标题','价格','地址','销量'])
    csvwriter.writeheader()#按行写入
    #1.发送请求 被反扒时刷新重新取cookie
    headers={
    "cookie": "cna=WmaUG0l2E0cCAXQ4gxeVtlLk; t=438dd8e59304958b60aad25a9517c830; sgcookie=E100ZghBS9PNskCMxLQgx1kTy0RGJN5JieMUigoeepKXHLk2BEwe3xZ8ezJr4qlijrOBLzdpgNa7k2eWLGa3ztLEw%2FsIS36cCL8dt%2FB13tushKo%3D; uc3=nk2=gKRnpQqwL1975SMz&id2=UUGk3pfAhYuK8A%3D%3D&vt3=F8dCv4ff7RlBEsME4MQ%3D&lg2=UtASsssmOIJ0bQ%3D%3D; lgc=%5Cu95EB%5Cu7EDF%5Cu5E05%5Cu840C%5Cu840C%5Cu54D2; uc4=nk4=0%40gu%2Fzg3OfNSn8VIjEgln6mdxKwkch9kM%3D&id4=0%40U2OT7jgfYKPYFCPbDuZuGicXZ3IH; tracknick=%5Cu95EB%5Cu7EDF%5Cu5E05%5Cu840C%5Cu840C%5Cu54D2; _cc_=U%2BGCWk%2F7og%3D%3D; enc=a0TU2Ue%2FnA8%2FFkQjI6xT1iW3i5cEr9rBX5aaS41QGdHjNvchniR4vjUQ%2Fiqh3IU%2BiHeZWuErOLOt2feZ6jKg%2FQ%3D%3D; mt=ci=-1_0; thw=cn; cookie2=20226d67d9fbbde7fd3ac0ae91e504f8; _tb_token_=7377bbee4d531; xlly_s=1; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; x5sec=7b227365617263686170703b32223a2266376534326139616463313339393533306430663061376436303662626538654350474c765a674745505076354d656b706547636f674561444449354e6a41774d446b354f5455374d54436e68594b652f502f2f2f2f384251414d3d227d; JSESSIONID=EB0C2122213BF318C25C9886B0D439E1; _m_h5_tk=6a97a83e4c4b7df8b80f1748c15aa798_1661953990194; _m_h5_tk_enc=7b5049e1581eb8647b8a8f514875ef8d; uc1=cookie14=UoeyD4t%2FZfmpyw%3D%3D; tfstk=cAnRB72xyIAuj6U_RYL088OkficRZM88tIVNvDJDREQNxRjdiDoiX1I5mRQdqKC..; l=eBPxvDPcTgcFOH7BBOfahurza77OSBdYYuPzaNbMiOCPOXfw5Lz1W6l31_TeC3GVh6y2R3lI-EzHBeYBq3tSnxvte5DDwQHmn; isg=BICAdyqU90zw1YtK1hg_tl3tXw5SCWTTdt9Zi_oRTBsvdSCfohk0Y1ZFid21Xhyr",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0"}
    i=1
    for page in range(1,10):#循环页面
        print("正在爬取第{}页".format(i))
        i=i+1
        url = 'https://s.taobao.com/search?spm=1903u.1.1998181369.1.10aa6fbeUdRGDb&q=%E6%89%8B%E6%9C%BA&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&ie=utf8&initiative_id=tbindexz_20170306&tab=all&bcoffset=1&ntoffset=1&p4ppushleft=2%2C48&s={}'.format(page*44)
        resp = requests.get(url, headers=headers)
        #2.获取数据
        data = resp.text
        # /data)
        # 3.解析数据 .*贪婪匹配 .*?非贪婪匹配
        json_str = re.findall('g_page_config = (.*);', data)[0]
        # 将json转化成字典类型，去json.cn去粘贴查看
        json_dict = json.loads(json_str)
        auctions = json_dict['mods']['itemlist']['data']['auctions']
        for item in auctions:
            try:
                # title=item['raw_title']
                # price=item['view_price']
                # loc= item['item_loc']
                # sales=item['view_sales']
                # print("产品：{} 价格：{} 地址：{} 销量：{}".format(title, price, loc, sales)) #format函数使用方法
                dict = {'标题': item['raw_title'],
                        '价格': item['view_price'],
                        '地址': item['item_loc'],
                        '销量': item['view_sales'].replace("人付款",""),#字符串替换
                        }
                csvwriter.writerow(dict)#每次循环写入一行

            except:
                pass
    print("over...")