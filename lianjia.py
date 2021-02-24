import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url, code='utf-8'):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, headers = kv)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

def getlocList(lst, locURL):
    html = getHTMLText(locURL, 'GB2312')
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('div',{'data-role':'ershoufang'})
    print(len(a))
    for i in a:
        for b in i.find_all('a'):
            try:
                href = b.attrs['href']
                lst.append(re.findall(r'/ershoufang/(.*?)/', href)[0])
            except :
                continue





def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock + '/'
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')
        page = str(soup.find_all('div',{'class':'page-box house-lst-page-box'}))
        totalpage = re.findall(r'"totalPage":(.*?),"curPage":1', page)
        print(totalpage)
        locloc = soup.find_all('a',class_='selected')[1].text
        for jj in totalpage:
            pg = int(jj)
            #with open(fpath, 'a', encoding='utf-8') as f:
            #    f.write(locloc + '\n') # write out location in chinese
            for ii in range(1,pg+1):
                if(ii==1):
                    url2 = stockURL + stock + '/'
                else:
                    url2 = stockURL + stock + '/pg' + str(ii) + '/'
                print(url2)
                try:
                    html2 = getHTMLText(url2)
                    if html2 == "":
                        continue
                    infoDict = {}
                    soup = BeautifulSoup(html2, 'html.parser')
                    houseInfo = soup.find('div', attrs={'class': 'bigImgList'})

                    namequote = houseInfo.find_all('a',attrs={'class': 'title'})
                    pricequote = houseInfo.find_all('div', attrs={'class': 'price'})
                    quote = houseInfo.find_all('div', attrs={'class': 'info'})

                    #with open(fpath, 'a', encoding='utf-8') as f:
                    #    f.write(str(len(namequote)) + '\n')

                    for cc in range(len(namequote)):

                        for k in namequote[cc]:
                            name = k
                            with open(fpath, 'a', encoding='utf-8') as f:
                                f.write(name)

                        z = pricequote[cc].text
                        price = z
                        with open(fpath, 'a', encoding='utf-8') as f:
                            f.write('/' + price)

                        v = quote[cc].text
                        key = v
                        with open(fpath, 'a', encoding='utf-8') as f:
                            f.write('/' + key + '\n')
                except:
                    continue

            with open(fpath, 'a', encoding='utf-8') as f:
                f.write('\n' + '\n')
            print('finish write '+stock)


def main():
    stock_list_url = 'https://sh.lianjia.com/ershoufang/'
    stock_info_url = 'https://sh.lianjia.com/ershoufang/'
    output_file = '/Users/yingwei/PycharmProjects/crawl/house_lianjia/houseinfo_sh.txt'
    slist = []
    getlocList(slist, stock_list_url)
    print('finish get list')
    getStockInfo(slist, stock_info_url, output_file)


main()