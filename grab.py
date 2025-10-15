# 這邊第一個先來端傳媒的科技資料
# 網址連結如下
# https://theinitium.com/channel/technology
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from PIL import Image
from wordcloud import WordCloud
from collections import Counter
import time
import datetime
import json
import pandas as pd
import jieba
import numpy as np
import matplotlib.pyplot as plt
import requests
import pyimgur

def run_article():
    path="./templates/articleLink.json"
    driver = webdriver.Chrome()
    driver.get('https://theinitium.com/channel/technology')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    titles = soup.select('#root > main > div > div > div > div > div > div > div > div> div > a > h3')
    driver.close()

    #將所有搜尋資料輸出至記事本
    file = open(r"./article/article.txt","w",encoding='utf-8')
    for i, title in enumerate(titles):
        file.write(title.text.strip())
    file.close()

    #將五筆資料初出道link模板
    #字串處理：Line的lebal文字不可超過40個字元
    #開始進行模板更新
    data =  json.load(open(path,'r',encoding="utf-8"))
    for i in range(5):
        data['body']['contents'][i]['action']['label']=str(titles[i].text.strip())
        data['body']['contents'][i]['action']['uri']="https://theinitium.com/channel/technology/"
    
    f = open(path,'w')
    json.dump(data,f)
    f.close()

def run_stock(stockNO):
    #stockNO = input("請輸入想要查詢之股票代碼或名稱")
    x = datetime.datetime.now()
    nowtime = (x.strftime("%Y"))+(x.strftime("%m"))+(x.strftime("%d"))
    data = {
        'response':'json',
        'date':nowtime,
        'stockNo':stockNO,
        '_':'1520905854825'
    }
    res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY', params=data)
    result = json.loads(res.text)
    result['fields']=['Date','Trading Volume','Business Volume','Opening Price','Highest Price','Lowest Price','Closing Price','Change','Transaction']
    df = pd.DataFrame(result['data'])
    df.columns = result['fields']
    df1 = df[0:19][['Date','Trading Volume','Business Volume','Transaction']]
    df2 = df[0:19][['Date','Opening Price','Highest Price','Lowest Price','Closing Price','Change']]
    """
    df1 = df[0:19][['日期','成交股數','成交金額','成交筆數']]
    df2 = df[0:19][['日期','開盤價','最高價','最低價','收盤價','漲跌價差']]
    df1.rename(columns = {'日期':'Date','成交股數':'Trading Volume','成交金額':'Business Volume','成交筆數':'Transaction'})
    df2.rename(columns = {'日期':'Date','開盤價':'Opening Price','最高價':'Highest Price','最低價':'Lowest Price','收盤價':'Closing Price','漲跌價差':'Change'})
    """
    print(df1)
    print(df2)
    url1=store_pandas_picture(df1,"table1")
    url2=store_pandas_picture(df2,"table2")
    return url1,url2

def search_stockNO(companyName):
    driver = webdriver.Chrome()
    driver.get("https://pchome.megatime.com.tw/search")
    elem = driver.find_element(By.NAME, "search_text_table")
    elem.clear()
    ActionChains(driver).double_click(elem).perform()
    elem.send_keys(companyName)
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    print(soup)
    TagcompanyStockNO = soup.select('tr > td > a')
    totalName = (TagcompanyStockNO[0].text.strip()) 
    StrcompanyStockNO=""
    for i in range (4):
        StrcompanyStockNO+=totalName[i]
    print(companyName+"的股票代碼為"+StrcompanyStockNO)
    driver.close()
    return (companyName+"的股票代碼為"+StrcompanyStockNO)

def search_hot_topic():
    driver = webdriver.Chrome() #開啟selenium模擬行為
    driver.get('https://www.ptt.cc/bbs/Stock/index.html')
    time.sleep(1) #等待網頁更新
    soup = BeautifulSoup(driver.page_source, 'lxml') #爬取資料
    titles = soup.select('#main-container > div.r-list-container.action-bar-margin.bbs-screen > div > div.title > a')
    
    TagnewWebsiteIndex = soup.select('#action-bar-container > div > div.btn-group.btn-group-paging > a:nth-child(2)') #找到目前網頁的index(為了做網址的替換)
    temp = (str(TagnewWebsiteIndex[0])) 
    newWebsiteIndex=""
    for i in range (42,46): 
        newWebsiteIndex+=temp[i]

    #後面開始繼續爬文章
    for i in range (int(newWebsiteIndex)-10,int(newWebsiteIndex)):
        driver.get('https://www.ptt.cc/bbs/Stock/index'+str(i)+'.html')
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        titles += soup.select('#main-container > div.r-list-container.action-bar-margin.bbs-screen > div > div.title > a')
    driver.close()
    
    file = open(r"./dictionary/input.txt","w",encoding='utf-8')
    for i, title in enumerate(titles):
        file.write(title.text.strip())
    file.close()

    file = open(r"./dictionary/input.txt","r",encoding='utf-8')

    content = file.read()  # 讀取文件內容
    content = content.replace("\n", "").strip()  # 刪除換行和多餘的空格
    content_seg = jieba.cut(content)    # jieba分詞

    dictionary = Counter(content_seg)
    stopwords = [line.strip() for line in open('./dictionary/stopwords.txt', 'r', encoding='utf-8').readlines()]
    [dictionary.pop(x, None) for x in stopwords]
    font = ".\\fonts\\msjh.ttc"
    mask = np.array(Image.open(".\\image\\cloud.jpg"))
    wordcloud = WordCloud(background_color="white",mask=mask,font_path=font)
    wordcloud.generate_from_frequencies(dictionary)
    plt.figure(figsize=(6,6))
    plt.imshow(wordcloud)
    plt.axis("off")

    wordcloud.to_file(".\\image\\wordcloud.png")
    
    CLIENT_ID = "50893946923ed5e"
    PATH = 'image//wordcloud.png' #A Filepath to an image on your computer"
    title = "Uploaded with PyImgur"
    print("hi")

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.type) 
    return str(uploaded_image.link)

def compare(companyNum):
    companyList = [[1101,1102,1103,1104,1108],[1201,1216,1217,1218,1231,1234],[1301,1303,1304,1315,1326],[1402,1409,1410,1413,1414,1417],[1503,1504,1506,1513,1514,1515],[1603,1604,1605,1608,1609,1611,1612],[1708,1709,1710,1711,1712,1713,1714,1717,1718,1721,1722,1723],[2302,2303,2329,2330,2337,2338,2342,2344,2351,2363,2369,2379,2388,2401,2408,2434,2436,2441,2449,2451,2454,2458,2481]]
    #companyNum = input("請輸入想要查詢之股票代碼或名稱")
    companyCategory=-1
    for i in range (len(companyList)):
        for j in range (len(companyList[i])):
            if int(companyNum)==companyList[i][j]:
                companyCategory = i
                break
    if (companyCategory==-1):
        print("此公司代碼不存在列表中")
    else:
        dataOuput1=[]
        driver = webdriver.Chrome()
        for companyNum in ((companyList[companyCategory])):
            driver.get("https://pchome.megatime.com.tw/stock/sid"+str(companyNum)+".html")
            time.sleep(1) #等待網頁更新
            soup = BeautifulSoup(driver.page_source, 'lxml') #爬取資料
            name = soup.select("#cont-area > div > div.lb665 > div.stock-info > div.stock-data > h1 > em")[0].get_text()
            data = soup.select("#stock_info_data_a > span")
            name=name.replace("\n","").strip()
            dataOuput1.append(name)
            for i, title in enumerate(data):
                dataOuput1.append(title.text.strip())
        #print(dataOuput1)
        dataOuput2="股票代碼"+str(companyNum)+"同業比較結果\n公司名 股票代碼 成交價 漲跌 漲跌比例 市值\n"
        for i in range(len(dataOuput1)//5):
            for j in range(i*5,(i+1)*5):
                dataOuput2+=str(dataOuput1[j])+" "
            dataOuput2+="\n"
        return(dataOuput2)

def store_pandas_picture(df,name):
    plt.figure('123')            # 視窗名稱
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax,df, loc='center') #將mytable投射到ax上，且放置於ax的中間
    plt.savefig('.\\image\\'+name+'.png')     # 存檔
    url = upload_picture_to_imgur(name)
    return url
    
def upload_picture_to_imgur(name):
    CLIENT_ID = "50893946923ed5e"
    PATH = 'image//'+name+'.png' #A Filepath to an image on your computer"
    title = "Uploaded with PyImgur"

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.type) 
    return str(uploaded_image.link)


