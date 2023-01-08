from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

driver = uc.Chrome()
options = uc.ChromeOptions()
options.add_argument('--headless')
driver = uc.Chrome(options)
import time
# file_path = 'links_list.txt'
# with open(file_path) as f:
#     links_list = f.readlines()

################Fix your range, fix order and num
order = 584 #the index of first record do you want to crawl
num = 9 #number of record do you want to crawl
start = order
end = start + num
files= open("text_link.txt","a",encoding="utf-8")
for i in range(261, 281):#(321,341): #26---, 61, 
    print(i)
    time.sleep(5)

    link = "https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm".format(i)
    print(link)
    print('-----------------------------------------------------------')
    print(order, '- ', link)
    #link_test = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-duong-minh-khai-phuong-vinh-tuy-prj-imperia-sky-garden/-chinh-chu-ban-nhanh-goc-dong-nam-toa-c-full-100-noi-that-view-dep-gia-4-5x-ty-pr27951316'
    driver.get(link)
    h = driver.find_elements("xpath",'//*[@id="product-lists-web"]/div')
    for i in h:
        try:
            a = BeautifulSoup(i.get_attribute('innerHTML'),"html.parser")
            linlk = a.find("a")["href"]
            print(linlk)
            files.write(linlk+"\n")
        except:
            pass
