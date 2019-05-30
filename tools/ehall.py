from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from requests.cookies import RequestsCookieJar

def driver_open():
    driver=webdriver.PhantomJS('bin/phantomjs')
    driver.get("http://authserver.cidp.edu.cn/authserver/login?service=http%3a%2f%2fjw.cidp.edu.cn%2fLoginHandler.ashx")
    driver.find_element_by_id('username').send_keys('165041131')
    driver.find_element_by_id('password').send_keys('Pengyu1998@')
    driver.find_element_by_xpath('//*[@id="casLoginForm"]/p[5]/button').click()
    time.sleep(3)
    cookies = driver.get_cookies()
    cookie = [item['name']+"="+item['value'] for item in cookies]
    cookie_str = ''.join(cookie)
    print(cookie_str)
    driver.quit()
    return cookies



def open_jw(cookies):
    jar = RequestsCookieJar()
    for cookie in cookies:
        jar.set(cookie['name'], cookie['value'])
    s = requests.Session()
    p = s.get('http://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx', cookies=jar)
    p.encoding = 'utf-8'
    print(p.text)
    # r = s.get('http://ehall.cidp.edu.cn/jsonp/sendRecUseApp.json?appId=5399199055014616&_=1559186487927')
    # r = s.get('http://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx')
    # r.encoding = 'utf-8'
    # print(r.text)
