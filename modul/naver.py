from bs4 import BeautifulSoup
import requests
import re
class naver:
    def __init__(self,url):
        respon=requests.get(url)
        self.__data = BeautifulSoup(respon.text, 'html.parser')
        respon.close()
    def getName(self):
        nama=self.__data.find(class_='_2IA5sp7BRM').text
        return nama
    def getPrice(self):
        harga=self.__data.select('strong ._7bB3O2y55c')[0]
        harga="".join(re.findall('\d+',harga.text))
        return int(harga)
    def __getColor(self):
        try:
            temp=[]
            color=self.__data.select("._7XbdNgoi2q")[0]
            for i in color.children:
                clr=i.attrs['style']
                temp.append(re.findall('(?<=:)#\w*',clr)[0])
            return temp
        except Exception as e:
            return False
    def __getSize(self):
        try:
            temp=[]
            size=self.__data.select("._1b3Gy3ENzj")[0]
            for i in size.children:
                #print i.text
                if not i.has_attr('disabled'):
                    temp.append(i.text)
            return temp
        except Exception as e:
            return False
    def __getOptionDropdown(self):
        try:
            a=re.findall('(?<=\"standardCombinations\":)\[.*?\]',self.__data.text)[0]
            
            b=re.findall('(?<=\"optionName2\":\").*?(?=\")',a)
            if len(b)>0:
                return b
            
            b=re.findall('(?<=\"optionName1\":\").*?(?=\")',a)
            if len(b)>0:
                return b
            else:
                return False
        except Exception as e:
            return False
    def getOption(self):
        temp=dict()
        if self.__getColor():
            temp.update({'color':self.__getColor()})
        if self.__getOptionDropdown() :
            temp.update({'size':self.__getOptionDropdown()})
        if self.__getSize() :
            temp.update({'size':self.__getSize()})

        return temp
    def getText(self):
        return self.__data.text