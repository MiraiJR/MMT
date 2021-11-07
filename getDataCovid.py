from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json,urllib.request


def getDataFromJson():
    data = urllib.request.urlopen("https://static.pipezero.com/covid/data.json").read()
    output = json.loads(data)   
    dataCovidVN = output['locations']
    camachomnay = []  
    for row in dataCovidVN:
        casesToday = row['casesToday']
        camachomnay.append(casesToday)
    return camachomnay

class getData(object):
    def __init__ (self):
        self.url = "https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam"
        self.driver = webdriver.Chrome("E:\driverChrome\chromedriver.exe")
        self.delay = 5
    def load_page(self):
        driver = self.driver
        driver.get(self.url)
        all_data = driver.find_elements_by_css_selector("tbody > tr > td")
        dataCovid = []
        temp2 = []
        tinhthanh = []
        canhiem = []
        hoiphuc = []
        dieutri = []
        tuvong = []
        canhiemhomnay = getDataFromJson()
        for data in all_data:
            dataCovid.append(data.text)
        for i in range(0,314):  
            if i%5 == 0:
                tinhthanh.append(dataCovid[i])
            elif i%5 == 1:
                canhiem.append(dataCovid[i])
            elif i%5 == 2:
                dieutri.append(dataCovid[i])
            elif i%5 == 3:
                hoiphuc.append(dataCovid[i])
            elif i%5 == 4:
                tuvong.append(dataCovid[i])
        for i in range(0, 62):
            temp = []
            temp.append(tinhthanh[i])
            temp.append(canhiem[i])
            temp.append(dieutri[i])
            temp.append(hoiphuc[i])
            temp.append(tuvong[i])
            temp.append(canhiemhomnay[i])
            temp2.append(temp)
        driver.close() 
        return temp2        
    
data1 = getData()
data1.load_page()