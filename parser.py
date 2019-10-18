__email__ = "khuphj@gmail.com"
__author__= "github@DevHyung"

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from openpyxl import Workbook
from tqdm import tqdm

def save_excel(_FILENAME, _DATA, _HEADER):
    # create workbook stream
    book = Workbook()
    sheet = book.active
    sheet.title = 'result' # INPUT YOUR SHEET NAME

    # input header line
    sheet.append(_HEADER)

    # set column dimensions width
    sheet.column_dimensions['A'].width = 80
    sheet.column_dimensions['B'].width = 80
    sheet.column_dimensions['C'].width = 40

    # input data
    for data in _DATA:# assume the _DATA Type is 2D array-> [ [cite1....], [cte2...] ]
        sheet.append(data)
    # save
    book.save(_FILENAME)

if __name__ == "__main__":
    # CONFIG AREA START ...
    FILENAME = "./logicrule_cite.xlsx" # save file name     
    headerList = ['title', 'author & conference', 'link']
    startUrl = 'https://scholar.google.com/scholar?cites=18126586568111983196&as_sdt=2005&sciodt=0,5&hl=ko' # input the google Cite 1 page url
    dataList = []
    MAXPAGE = 20 # Automatically end the last page
    # CONFIG AREA END ...

    driver = webdriver.Chrome('./chromedriver')
    driver.get(startUrl)

    for _ in tqdm(range(MAXPAGE+1)):
        # wait page loading
        sleep(2)

        # convert page source to bs object
        bs = BeautifulSoup(driver.page_source,'lxml')

        # parsing
        divs = bs.find_all('div',class_='gs_r gs_or gs_scl')
        for div in divs:
            title = div.find('h3',class_='gs_rt').find('a').text.strip()
            author = div.find('div', class_='gs_a').text.strip()
            link =  div.find('h3',class_='gs_rt').find('a')['href'].strip()

            dataList.append([title,author,link])

        # move the next page
        try:
            driver.find_element_by_xpath('//*[@id="gs_n"]/center/table/tbody/tr/td[12]/a/b').click()
        except: # last page
            break
    # save
    save_excel(FILENAME, dataList, headerList)