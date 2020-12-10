from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

fields = ['Tên', 'Mức giá', 'Diện tích', 'Loại tin đăng', 'Địa chỉ',
          'Mặt tiền', 'Đường vào', 'Hướng ban công', 'Số tầng', 'Số phòng ngủ',
          'Số toilet', 'Nội thất', 'Pháp lý', 'Tên dự án', 'Chủ đầu tư',
          'Quy mô', 'Ngày đăng', 'Ngày hết hạn', 'Loại tin', 'Mã tin', 'Phòng ngủ', 'Hướng nhà']

def write_csv(dictionary):
    file_path = "data_batdongsan_com_vn.csv"
    try:
        with open(file_path, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            #writer.writeheader()
            #for data in dictionary:
            writer.writerow(dictionary)
    except IOError:
        print("I/O error")

def extract_title(driver):
    title= driver.find_elements_by_xpath('//div[@class="description"]/h1[@class="tile-product"]')[0].text
    dic = dict()
    dic['Tên'] = title
    #print(dic)
    return dic

def extract_price_and_area(driver):
    short_detail_get = driver.find_elements_by_xpath('//ul[@class="short-detail-2 clearfix pad-16"]/li/span')
    short_detail_list = []
    for i in range(len(short_detail_get)):
        short_detail_list.append(short_detail_get[i].text)

    dic = dict()
    key = ''
    value = 0
    bound = len(short_detail_list)
    i = 0
    while i < bound:
        if i % 2 == 0:
            key = short_detail_list[i][:-1]
        else:
            value = short_detail_list[i]
            dic[key] = value

        i = i + 1

    #print(dic)
    return dic

def extract_detail(driver):
    detail_product_get = driver.find_elements_by_xpath(
        '//div[@class="box-round-grey3"]/div/span')
    detail_product_list = []
    for i in range(len(detail_product_get)):
        detail_product_list.append(detail_product_get[i].text)

    dic = dict()
    key = ''
    value = 0
    bound = len(detail_product_list)
    i = 0
    while i < bound:
        if i % 2 == 0:
            key = detail_product_list[i][:-1]
        else:
            value = detail_product_list[i]
            dic[key] = value

        i = i + 1

    #print(dic)
    return dic

def extract_date_and_id(driver):
    date_and_id_get = driver.find_elements_by_xpath('//ul[@class="short-detail-2 list2 clearfix"]/li/span')
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
            key = date_and_id[i][:-1]
        else:
            value = date_and_id[i]
            dic[key] = value

        i = i + 1

    #print(dic)
    return dic

if __name__ == '__main__':
    #################Fix chomedriver file path
    driver = webdriver.Chrome('./chromedriver')
    file_path = 'links_list.txt'
    with open(file_path) as f:
        links_list = f.readlines()

    ################Fix your range, fix order and num
    order = 584 #the index of first record do you want to crawl
    num = 10000 #number of record do you want to crawl
    start = order
    end = start + num

    for i in range(start, end + 1):
        link = links_list[i]
        print('-----------------------------------------------------------')
        print(order, '- ', link)
        #link_test = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-duong-minh-khai-phuong-vinh-tuy-prj-imperia-sky-garden/-chinh-chu-ban-nhanh-goc-dong-nam-toa-c-full-100-noi-that-view-dep-gia-4-5x-ty-pr27951316'
        driver.get(link)
        data = dict()


        try:
            #Get title:
            title = extract_title(driver)

            #Get price and area
            price_area = extract_price_and_area(driver)

            #Get detail:
            detail = extract_detail(driver)

            #Get date and id
            date_and_id = extract_date_and_id(driver)

            #involving
            data.update(title)
            data.update(price_area)
            data.update(detail)
            data.update(date_and_id)

            print(data)

            write_csv(data)
            order = order + 1
            with open('start_end.txt', 'a') as f:
                f.writelines(str(order) + '\n')

            # stop = stop + 1
            # if (stop == 2):
            #     break

        except:
            print('Item is not available or Error')


#434 -  https://batdongsan.com.vn/ban-can-ho-chung-cu-pho-phung-hung-1-phuong-phuc-la-prj-khu-do-thi-moi-xa-la/sieu-pham-nha-dep-gia-tot-tai-ct1a-90m-bc-dong-nam-full-noi-that-gia-1-52-ty-tl-manh-pr28084191
#502
