from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import traceback
import time
fields = ['Tên', 'Mức giá', 'Diện tích', 'Loại tin đăng', 'Địa chỉ',
          'Mặt tiền', 'Đường vào', 'Hướng ban công', 'Số tầng', 'Số phòng ngủ',
          'Số toilet', 'Nội thất', 'Pháp lý', 'Tên dự án', 'Chủ đầu tư',
          'Quy mô', 'Ngày đăng', 'Ngày hết hạn', 'Loại tin', 'Mã tin', 'Phòng ngủ', 'Hướng nhà']

def write_csv(dictionary):
    file_path = "data_batdongsan_com_vn.csv"
    try:
        with open(file_path, 'a',encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            #writer.writeheader()
            #for data in dictionary:
            writer.writerow(dictionary)
    except IOError:
        print("I/O error")

def extract_title(driver):
    title= driver.find_elements("xpath",'//*[@id="product-detail-web"]/h1')[0].text
    dic = dict()
    dic['Tên'] = title
    #print(dic)
    return dic
def extract_project_name(driver):
    title= driver.find_elements("xpath",'//*[@id="product-detail-web"]/div[4]/div/div[2]/div[2]/div[1]/div')[0].text
    dic = dict()
    dic['Tên dự án'] = title
    #print(dic)
    return dic

def extract_address(driver):
    title= driver.find_elements("xpath",'//*[@id="product-detail-web"]/span')[0].text
    dic = dict()
    dic['Địa chỉ'] = title
    #print(dic)
    return dic
def extract_price_and_area(driver):
    short_detail_get = driver.find_elements("xpath",'//*[@id="product-detail-web"]/div[1]/div')
    short_detail_list = []
    for i in short_detail_get:
        spanlist  = BeautifulSoup(i.get_attribute('innerHTML'),"html.parser")
        for j in spanlist.find_all("span")[:2]:
            short_detail_list.append(j.text)

    dic = dict()
    key = ''
    value = 0
    bound = len(short_detail_list)
    i = 0
    while i < bound:
        if i % 2 == 0:
            key = short_detail_list[i]
        else:
            value = short_detail_list[i]
            dic[key] = value

        i = i + 1

    return dic

def extract_detail(driver):
    detail_product_get = driver.find_elements("xpath",'//*[@id="product-detail-web"]/div[3]/div/div/div/span')
    detail_product_list = []
    for i in range(len(detail_product_get)):
        if i%3==0:
            pass
        else:
            detail_product_list.append(detail_product_get[i].text)

    dic = dict()
    key = ''
    value = 0
    bound = len(detail_product_list)
    i = 0
    while i < bound:
        if i % 2 == 0:
            key = detail_product_list[i]
        else:
            value = detail_product_list[i]
            dic[key] = value

        i = i + 1

    return dic

def extract_date_and_id(driver):
    date_and_id_get = driver.find_elements("xpath",'//*[@id="product-detail-web"]/div[9]/div/span')
    date_and_id = []
    for i in range(len(date_and_id_get)):
        date_and_id.append(date_and_id_get[i].text)

    dic = dict()
    key = ''
    value = 0
    bound = len(date_and_id)
    i = 0
    while i < bound:
        if i % 2 == 0:
            key = date_and_id[i]
        else:
            value = date_and_id[i]
            dic[key] = value

        i = i + 1

    #print(dic)
    return dic

if __name__ == '__main__':
    #################Fix chomedriver file path
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    driver = uc.Chrome(options)
    file_path = 'text_link.txt'
    # with open(file_path) as f:
    #     links_list = f.readlines()

    ################Fix your range, fix order and num
    order = 7000 #the index of first record do you want to crawl
    num = 1000 #number of record do you want to crawl
    start = order
    end = start + num

    for i in range(start,end):
        time.sleep(1)
        try:
            order=i
            # link = "https://batdongsan.com.vn"+links_list[i].replace("\n","")
            print('-----------------------------------------------------------')
            # print(order, '- ', link)
            link_test = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-pho-lieu-giai-phuong-ngoc-khanh-prj-vinhomes-metropolis-lieu-giai/cc-ban-3pn-dt-110m2-full-do-goc-re-nhat-thi-truong-gia-10-x-ty-lh-0974887733-pr34669070'
            driver.get(link_test)
            data = dict()


                #Get title:
            title = extract_title(driver)

            #Get price and area
            price_area = extract_price_and_area(driver)

            #Get detail:
            detail = extract_detail(driver)
            address = extract_address(driver)
            #Get date and id
            date_and_id = extract_date_and_id(driver)
            project_name = extract_project_name(driver)
            #involving
            data.update(title)
            data.update(price_area)
            data.update(detail)
            data.update(address)
            data.update(date_and_id)
            data.update(project_name)
            print(data)

            write_csv(data)
            order = order + 1
            with open('start_end.txt', 'a',encoding="utf-8") as f:
                f.writelines(str(order) + '\n')
        except Exception as e:
            traceback.print_exc()
            with open('start_end.txt', 'a',encoding="utf-8") as f:
                f.writelines(str(order)+ "lỗi"+ '\n')
            # stop = stop + 1
            # if (stop == 2):
            #     break
        exit()



#434 -  https://batdongsan.com.vn/ban-can-ho-chung-cu-pho-phung-hung-1-phuong-phuc-la-prj-khu-do-thi-moi-xa-la/sieu-pham-nha-dep-gia-tot-tai-ct1a-90m-bc-dong-nam-full-noi-that-gia-1-52-ty-tl-manh-pr28084191
#502
