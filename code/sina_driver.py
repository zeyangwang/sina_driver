# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 09:20:58 2020

@author: Administrator
"""
import time
from selenium import webdriver
from bs4 import BeautifulSoup



'''
使用selenium模拟登录，需导入该包，并同时下载相应浏览器的对应版本驱动，建议先升级谷歌浏览器到最新版
Google Chrome浏览器驱动下载地址：http://npm.taobao.org/mirrors/chromedriver/
我的谷歌浏览器版本是84.0.4147.105，所以下载：http://npm.taobao.org/mirrors/chromedriver/84.0.4147.30/
将下载好解压后的驱动exe程序放在Python的安装目录下，如果用的是anacada,它集成的Python安装目录是：D:\python\python370和D:\python\python370\Scripts
'''
#模拟登录新浪微博,并返回登录状态的浏览器对象
def login_sina():
    print(u'登陆新浪微博手机端...')
    ##打开google浏览器
    #'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    browser = webdriver.Chrome()
    ##给定登陆的网址
    url = 'https://passport.weibo.cn/signin/login'
    browser.get(url)
    time.sleep(3)
    #找到输入用户名的地方，并将用户名里面的内容清空，然后送入你的账号
    username = browser.find_element_by_css_selector('#loginName')
    time.sleep(2)
    username.clear()
    username.send_keys('')#输入自己的账号
    #找到输入密码的地方，然后送入你的密码
    password = browser.find_element_by_css_selector('#loginPassword')
    time.sleep(2)
    password.send_keys('')#输入自己的密码
    #点击登录
    browser.find_element_by_css_selector('#loginAction').click()
    ##这里给个15秒非常重要，因为在点击登录之后，新浪微博会有个九宫格验证码，下图有，通过程序执行的话会有点麻烦（可以参考崔庆才的Python书里面有解决方法），这里就手动
    time.sleep(5)
    print('完成登陆!')
    
    
    return browser

#打开对应的页面
def open_urlpage(browser,url):
    browser.get(url)
    time.sleep(3)
    
    return browser.page_source

#提取对应页面内容
def get_userinfo(user_html):
    #使用BeautifulSoup解析网页的HTML
    soup = BeautifulSoup(user_html, 'lxml')
    #爬取微博的昵称
    nicheng = soup.find("div",class_="ut").contents[0]
    print("nicheng:  "+nicheng)
    #爬取微博数量
    divMessage = soup.find("div", class_="tip2").find_all('a')[:-1]
    #divMessage = soup.find('div',attrs={'class':'tip2'})
   
    weiboCount = divMessage[0].getText()[3:-1]
    weibo_url = get_tatolurl(divMessage[0].get('href'))
    gaunzhuCount = divMessage[1].getText()[3:-1]
    gaunzhu_url = get_tatolurl(divMessage[1].get('href'))
    diannzanCount = divMessage[2].getText()[3:-1]
    diannzan_url = get_tatolurl(divMessage[2].get('href'))
    
    #封装成字典备用
    value = {"nicheng":nicheng,"weiboCount":weiboCount,"gaunzhuCount":gaunzhuCount,"diannzanCount":diannzanCount,"weibo_url":weibo_url,"gaunzhu_url":gaunzhu_url,"diannzan_url":diannzan_url}
    #print(nicheng,weiboCount,gaunzhuCount,diannzanCount)
    #print(weibo_url,gaunzhu_url,diannzan_url)
    
    
    return value

#返回完整网址
def get_tatolurl(url):
    url_pre = "https://weibo.cn"
    return url_pre+url

#存储为text
def save_text(path,str):
    f = open(path,'a', encoding='utf-8')  #若文件不存在，系统自动创建。'a'表示可连续写入到文件，保留原内容，在原内容之后写入。
    f.write(str)  #将爬取信息写入文件中
    f.write("\n") 
    f.close()   

#主方法
if __name__=='__main__':

    browser_sina = login_sina()
    
    userid =  ""#写入个人的userid
    user_url = 'http://weibo.cn/u/'+userid
    user_html = open_urlpage(browser_sina,user_url)
    
    text = get_userinfo(user_html)
    print(text)
    
    path = "sina_userinfo.txt"
    save_text(path,str(text))

    
    
