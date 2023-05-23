import re
import xlwt
import requests
from bs4 import BeautifulSoup
 
def getHtml(url):  
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}  
    page = requests.get(url,headers = headers)
    html =page.text
    return html
 
if __name__=='__main__':
    Workbook = xlwt.Workbook()
    sheet = Workbook.add_sheet('豆瓣读书Top250')
    sheet.write(2,2,'书名')
    sheet.write(2,3,'作者')
    sheet.write(2,4,'译者')
    sheet.write(2,5,'出版单位')
    sheet.write(2,6,'出版时间')
    sheet.write(2,7,'定价')
    sheet.write(2,8,'豆瓣评分')
    sheet.write(2,9,'评价人数')
    sheet.write(2,10,'短评')


    i = 3
    j = 3
    k = 3
    m = 3
    for page in range(0,250,25):
        url = 'https://book.douban.com/top250?start={0}'.format(page)
        html = getHtml(url)
        Soup = BeautifulSoup(html,'html.parser')
        names = Soup.find_all('div',class_ = 'pl2')
        
        for name in names:
            book = name.find('a')
            book = book.text.strip()
            book = book.replace(' ','')
            sheet.write(i,2,book)
            i += 1
        
        Infos = Soup.find_all('p',class_ = 'pl')
        for Info in Infos:
            r = 1
            authorinfo =  Info.text
            authors = authorinfo.split('/')
            if len(authors) < 4:
                sheet.write(j,5,authors[0])
                sheet.write(j,6,authors[1])
                sheet.write(j,7,authors[2])
                j += 1
                continue
            sheet.write(j,3,authors[0])
            if authorinfo.count('/') == 4:
                sheet.write(j,4,authors[r])
                r += 1
            sheet.write(j,5,authors[r])
            sheet.write(j,6,authors[r+1])
            sheet.write(j,7,authors[r+2])
            j += 1
 
        rating_nums = Soup.find_all('div',class_ = 'star clearfix')
        for rating in rating_nums:
            star = rating.find_all('span')
            sheet.write(k,8,star[1].text)
            reg = r'\d+'
            vote = re.findall(reg,star[2].text)
            sheet.write(k,9,vote)
            k += 1
        quotes = Soup.find_all('p',class_ = 'quote')
        for quote in quotes:
            sheet.write(m,10,quote.text)
            m += 1
        
    
    Workbook.save('豆瓣读书Top250.xls')