import os
import re

import requests
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
import xlsxwriter
from threading import Timer

menu_url = {'电工电料':'2_1', '电线电缆':'1_1', '灯具照明':'3_1', '电器':'4_1', '给排水':'5_1', '卫浴':'6_1', '水暖器材':'7_1', '空调通风':'8_1', '消防器材':'9_1','安全防护':'10_1', '涂料化工':'11_1', '装饰材料':'13_1', '日用百货':'14_1', '工具':'15_1', '焊接切割':'16_1', '搬运存储':'17_1', '建筑机械':'18_1', '钢材':'19_1','机械机电':'20_1', '紧固件':'21_1', '五金丝网':'22_1', '建筑辅材':'23_1', '副食粮油':'24_1', '市政园林':'2022_1', '自用商品':'27_1', '信息设施':'2066_1','防水保温':'12_1'}
menu = ['电工电料', '电线电缆', '灯具照明', '电器', '给排水', '卫浴', '水暖器材', '空调通风', '消防器材',
        '安全防护', '涂料化工', '装饰材料', '日用百货', '工具', '焊接切割', '搬运存储', '建筑机械', '钢材',
        '机械机电', '紧固件', '五金丝网', '建筑辅材', '副食粮油', '市政园林', '自用商品', '信息设施','防水保温']
menu_href=[]
error_href = []


class SpiderO:
    def __init__(self):
        self.url = 'https://www.fsyuncai.com/category/{}.html'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # self.driver = webdriver.Chrome(options=self.options)
        # self.driver.get(url=self.url)
        self.top_type = 'error'
        self.index_handle = None
        self.menu_title=menu
        self.count = 0
        self.data = []

        self.starttime = time.time()
        # self.driver.set_script_timeout(4)
        # self.driver.set_page_load_timeout(7)
        self.menu = menu_href
        self.page=1
        self.no_href=[]

    def parse_two(self):
        time.sleep(1)
        links = self.driver.find_elements_by_xpath('//div[@class="box_iocImg"]/a')
        # links.click()
        links_list = []
        if links:
            for index,link in enumerate(links):
                try:
                    # print(link)
                    href = link.get_attribute('href')
                    # print(href)
                    links_list.append(href)
                except Exception as e:
                    self.no_href.append(f'第{self.page}页，第{index+1}个无法获取地址')
                    print(e)
        return links_list

    def parse_three(self, href_links):
        print('页码：',self.page)
        print('地址:',href_links)
        for href in href_links:
            print(href)
            js = f'window.open("{href}");'
            self.driver.execute_script(js)
            all_handles = self.driver.window_handles
            self.driver.switch_to.window(all_handles[1])
            # 解析提取数据

            try:
                self.parse_four()
            except Exception as e:
                print(href, '连接超时', e)
                global error_href
                error_href.append(href)


            # self.t.cancel()

            # time.sleep(2)
            self.driver.close()
            self.driver.switch_to.window(all_handles[0])


    def parse_four(self):
        # 主类别
        t_type = self.driver.find_element_by_xpath('//span[@class="brandCat"]/label[1]//label').text
        print(t_type)
        # 一级类别

        first_type = self.driver.find_element_by_xpath('//span[@class="brandCat"]/label[2]//label').text
        print('first_type', first_type)
        # 二级类别
        second_type = self.driver.find_element_by_xpath('//span[@class="brandCat"]/label[3]//label').text
        print('second_type', second_type)
        # 名称

        title = self.driver.find_element_by_xpath('//b[@class="curProduct"]').text
        title = ''.join(title.split(' ')[:-1])

        print('title', title)
        # 单位 （最少起订量）

        unit = self.driver.find_element_by_xpath('//span[@class="minnum"]').text

        print('unit', unit)
        more_spec_price = []

        sps = self.driver.find_elements_by_xpath('//div[@class="list productList"]/ul')
        if sps:
            for sp in sps:
                spec = sp.find_element_by_xpath('./li[@class="row_gg"]').text
                price = sp.find_element_by_xpath('./li[@class="row_p"]').text
                # print('原price', price)
                price = re.findall('(\d*\.\d*)', price)[0]
                # print('新price', price)
                more_spec_price.append((spec, price))
            print(more_spec_price)
            print(f'{len(more_spec_price)}个规格')

        else:
            spec = self.driver.find_element_by_xpath('//a[@class="curr"]').text
            price = self.driver.find_element_by_xpath('//span[@class="yc-price" or @class="p-price"]/b').text
            price = re.findall('(\d*.\d)', price)[0]
            more_spec_price.append((spec, price))
            print(more_spec_price)
        print(f'{len(more_spec_price)}个规格')
        # image
        try:
            img = self.driver.find_element_by_xpath('//div[@class="large_box"]//li/img')
            img=img.get_attribute('src')
            img_name=self.write_imgaes(img)
            print(img_name)
        except Exception as e:
            img_name='error'
            print(e)
        self.data.append((first_type, second_type, title, unit, more_spec_price,img_name,t_type))
        # print(self.data)
        print('*' * 10)

    def write_imgaes(self,url):
        im=requests.get(url=url).content
        if not os.path.exists(f'./image_{self.top_type}'):
            os.mkdir(f'./image_{self.top_type}')
        print('image', os.getcwd())

        with open(f'./image_{self.top_type}/image'+str(self.count)+'.jpg','wb') as f:
            f.write(im)
        self.count+=1
        return f'image{self.count-1}.jpg'


    def write_files(self,title,retry=False):
        print('xlsx',os.getcwd())
        self.workbook = xlsxwriter.Workbook('材料价格指导价格指数表' +title+
                                            time.strftime('%Y_%m_%d_%H_%M') + '.xlsx')
        self.data = sorted(self.data, key=lambda x: (x[0], x[1]))
        print('*' * 100)
        print(self.data)
        worksheet = self.workbook.add_worksheet(title)
        merge_format = self.workbook.add_format({
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
        })
        worksheet.merge_range('A1:I1', '', merge_format)
        worksheet.merge_range('A2:I2', '价格指数表（工具）', merge_format)

        worksheet.merge_range('A3:C3', f'更新时间：{time.strftime("%Y年%m月%d日")}')
        worksheet.merge_range('H3:I3', '单价：含税单价', merge_format)
        worksheet.write_row('A4', ['序号', '材料类别1', '材料类别2', '材料名称', '规格', '单位', '图片', '价格','备注'], merge_format)
        count = 5
        worksheet.set_column(0, 0, 5)
        worksheet.set_column(1, 1, 11.75)
        worksheet.set_column(2, 2, 12.75)
        worksheet.set_column(3, 3, 25)
        worksheet.set_column(4, 4, 25)
        worksheet.set_column(5, 5, 5)
        worksheet.set_column(6, 6, 11)
        worksheet.set_column(7, 7, 15)

        worksheet.set_row(0, 33)
        worksheet.set_row(1, 31)
        worksheet.set_row(2, 31.5)
        worksheet.set_row(3, 56)
        worksheet.set_row(4, 30)
        for item in self.data:
            # print('item',item)
            # print('item type',type(item))
            for sps in item[-3]:
                # print('sps', sps)
                # print('sps type', type(sps))
                print('正在写入--->', [count - 4,item[0], item[1], item[2], sps[0], item[3], item[-2],sps[1]])
                worksheet.set_row(count, 30)
                if not retry:
                    worksheet.write_row(f'A{count}', [count - 4, item[0], item[1], item[2], sps[0], item[3],'',sps[1]],merge_format)
                else:
                    worksheet.write_row(f'A{count}',[count - 4, item[0], item[1], item[2], sps[0], item[3], '', sps[1],item[-1]],merge_format)
                if not item[-1]== 'error':
                    print(f'正在写入->./image/{item[-2]}')
                    worksheet.insert_image(f'G{count}',f'./image_{self.top_type}/{item[-2]}',
                                           {'x_scale': 0.09, 'y_scale': 0.09,
                                            'x_offset':23,'y_offset':2,

                                            })
                count += 1

        self.data = []
        self.workbook.close()

    def retry_error(self,error_hrefs):
        if not os.path.exists('./error'):
            os.mkdir('./error')
        os.chdir('./error')
        error_count=0
        for href in error_hrefs:
            self.driver = webdriver.Chrome(options=self.options)
            self.driver.set_script_timeout(5)
            self.driver.set_page_load_timeout(7)
            try:
                self.driver.get(href)
                print('正在重新尝试',href)
            except Exception as e:
                print(e)
            try:
                self.driver.find_element_by_xpath('//*[@id="addressDia"]/div/ul/li[1]/span').click()
            except Exception as e:
                print(e)
            time.sleep(1)
            try:
                self.parse_four()
                self.write_files(title=f'_超时链接_{error_count}',retry=True)
                error_count+=1
            except Exception as e:
                print(href, '连接超时', e)




    def parse_run(self,item):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.driver.set_script_timeout(5)
        self.driver.set_page_load_timeout(7)
        try:
            self.driver.get(self.url.format(item))
            print('正在进入',self.url.format(item))
        except Exception as e:
            print(e)
        try:
            self.driver.find_element_by_xpath('//*[@id="addressDia"]/div/ul/li[1]/span').click()
        except Exception as e:
            print(e)
        time.sleep(1)
        while True:
            href_links = self.parse_two()
            self.parse_three(href_links)
            self.driver.refresh()
            try:
                page_count=self.driver.find_element_by_xpath('//div[@class="page-count"]').text
                page=int(re.findall('共(\d+)页',page_count)[0])
            except IndexError as i:
                break
            # print(page)
            if self.page!=page:
                self.driver.find_element_by_xpath('//input[@class="jump-ipt"]').send_keys(self.page+1)
                self.driver.find_element_by_xpath('//a[@class="jump-btn"]').click()
                time.sleep(3)
                if self.page==6:
                    time.sleep(7)
                self.page+=1
            else:
                break


            # try:
            #     self.driver.refresh()
            #     self.driver.find_element_by_xpath(f'//a[@data-page="{self.page+1}"]').click()
            #     time.sleep(2)
            #     self.page+=1
            # except Exception as e:
            #     break



        print('正在写入....')
        self.write_files(self.top_type)
        self.driver.close()
        self.count = 0
        self.page=1

    def run(self):
        if self.menu:
            for index,item in enumerate(self.menu):
                self.top_type=self.menu_title[index]
                print('*' * 10, '正在抓取', self.top_type, '*' * 10)
                if not os.path.exists(f'./{self.top_type}'):
                    os.mkdir(f'./{self.top_type}/')
                os.chdir(f'./{self.top_type}/')
                # self.top_type = item
                self.parse_run(item)
                global error_href
                if error_href:
                    with open(f'./error_href.txt', 'w')as f:
                        for href in error_href:
                            f.writelines(href + '\n')
                    error_href=[]
                if self.no_href:
                    with open(f'./error_no_href.txt', 'w')as f:
                        for i in self.no_href:
                            f.writelines(i + '\n')
                os.chdir('../')
                endtime = time.time()
                print(endtime - self.starttime)
        print(self.no_href)



def get_error_href_files():
    print(os.getcwd())
    listdir = os.listdir('./')
    for d in listdir:
        if os.path.isdir(f'./{d}'):
            listdirs = os.listdir(f'./{d}')
            for text in listdirs:
                if text == 'error_href.txt':
                    return(f'./{d}/error_href.txt')

def retry_error_href():
    texts = []
    error_href_files=get_error_href_files()
    texts.append(error_href_files)
    print(texts)
    error_hrefs=[]
    for error_files in texts:
        with open(error_files) as f:
            # print(f.readline())
            while True:
                eh=f.readline()
                print(eh.replace('\n',''))
                if eh:
                    error_hrefs.append(eh.replace('\n',''))
                if not eh:
                    break
    print(error_hrefs)
    SpiderO().retry_error(error_hrefs)
    os.chdir('../')
    for file in texts:
        os.rename(file,file.replace('error_href.txt','error_href_retry.txt'))


def view():
    while True:
        print('*' * 50)
        print('1-----全部抓取')
        print('2-----单分类抓取')
        print('3-----多分类抓取')
        print('4-----重试错误链接')
        print('0-----退出')
        print('*' * 50)
        try:
            tag = int(input('请输入操作编码：'))
        except:
            print('错误编码')
            continue
        if tag == 0:
            print('感谢使用')
            break
        elif tag == 1:
            for item in menu:
                menu_href.append(menu_url[item])
            SpiderO().run()

            if error_href:
                print('其中以下链接抓取失败:')
                for href in error_href:
                    print(href)
            os._exit('抓取完成')
        elif tag == 2:
            view2()
        elif tag == 3:
            view3()
        elif tag==4:
            retry_error_href()
        else:
            print('无此编码')


def view2():
    while True:
        print('*' * 50)
        print('*' * 10, '单分类抓取', '*' * 10)
        print('1---电工电料', '2---电线电缆', '3---灯具照明', '4---电器', '5---给排水')
        print('6---卫浴', '7---水暖器材', '8---空调通风', '9---消防器材', '10---安全防护')
        print('11---涂料化工', '12---装饰材料', '13---日用百货', '14---工具', '15---焊接切割')
        print('16---搬运存储', '17---建筑机械', '18---钢材', '19---机械机电', '20---紧固件')
        print('21---五金丝网', '22---建筑辅材', '23---副食粮油', '24---市政园林', '25---自用商品')
        print('26---信息设施', '27---防水保温')
        print('0---返回上一级')
        print('*' * 50)
        try:
            tag = int(input('请输入编码'))
        except:
            print('编码输入错误')
            continue
        if tag == 0:
            view()
        elif 27 >= tag >= 1:
            global menu
            tag_str = menu[tag - 1]
            menu = [tag_str]
            menu_href.append(menu_url[tag_str])
            SpiderO().run()

            if error_href:
                print('其中一下链接抓取失败:')
                for href in error_href:
                    print(href)
            os._exit('抓取完成')
        else:
            print('错误编码')


def view3():
    while True:
        print('*' * 50)
        print('*' * 10, '多分类抓取', '*' * 10)
        print('1---电工电料', '2---电线电缆', '3---灯具照明', '4---电器', '5---给排水')
        print('6---卫浴', '7---水暖器材', '8---空调通风', '9---消防器材', '10---安全防护')
        print('11---涂料化工', '12---装饰材料', '13---日用百货', '14---工具', '15---焊接切割')
        print('16---搬运存储', '17---建筑机械', '18---钢材', '19---机械机电', '20---紧固件')
        print('21---五金丝网', '22---建筑辅材', '23---副食粮油', '24---市政园林', '25---自用商品')
        print('26---信息设施', '27---防水保温')
        print('0---返回上一级')
        print('*' * 50)
        str_l = input('请输入编码:(逗号间隔)')
        l_str = str_l.split(',')
        l_num = []
        for i in l_str:
            try:
                tag = int(i)
                l_num.append(tag)
            except:
                print('编码输入错误')
                continue
        if len(l_num) == 1:
            if l_num[0] == 0:
                view()
            else:
                print('只输入了一个类别，即将进入单分类抓取')
                view2()
        else:
            global menu
            global error_href
            m = []
            try:
                for tag in l_num:
                    if 27 >= tag >= 1:
                        menu_href.append(menu_url[menu[tag-1]])
                        m.append(menu[tag - 1])
                    else:
                        print('编码错误')
                        raise Exception('编码错误')
            except Exception as e:
                print(e)
                continue
            menu = m
            SpiderO().run()

            if error_href:
                print('其中一下链接抓取失败:')
                for href in error_href:
                    print(href)
            os._exit('抓取完成')


if __name__ == '__main__':
    # SpiderO().run()
    try:
        view()
    except TypeError:
        print('抓取完成')
        pass
    # except Exception as e:
    #     print(e)
    #     print('抓取异常终止')

    os.system('pause')
