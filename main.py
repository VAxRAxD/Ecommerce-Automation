from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from .config import *
import csv
import time

class Ecommerce:
    def __init__(self):
        self.driver=webdriver.Firefox()
        self.file=open('./sample.csv')
    def readData(self):
        reader=csv.reader(self.file)
        data=list()
        for row in reader:
            data.append(row)
        del data[0]
        return data
    def placeOrder(self):
        self.driver.get('https://edalnice.cz/en/bulk-purchase/index.html ')
        details=self.readData()
        order=1
        for data in details:
            self.driver.find_element(By.ID,f'react-select-{order+1}-input').send_keys((data[0].split())[0])
            while True:
                try:
                    element=self.driver.find_element(By.XPATH,f'//div[contains(text(),"{data[0]}")]')
                    if element:
                        self.driver.execute_script("arguments[0].scrollIntoView();",element)
                        element.click()
                        break
                except:
                    pass
            self.driver.find_element(By.XPATH,f'(//*[@id="valid-since-input"])[{order}]').send_keys(data[1])
            self.driver.find_element(By.XPATH,f'(//input[@type="text" and @class="order-0 flex-grow-1"])[{order}]').send_keys(data[2])
            self.driver.find_element(By.XPATH,f'(//input[@type="text" and @class="order-0 flex-grow-1"])[{order}]').send_keys(Keys.RETURN)
            if data[3]!="":
                self.driver.find_element(By.ID,f'alternative_fuel_type_checkbox_{order-1}').click()
                if data[3]=="Natural Gas":
                    self.driver.find_element(By.ID,f'natural_gas_radio_array_option_{order-1}').click()
                else:
                    self.driver.find_element(By.ID,f'bio_methane_radio_array_option_{order-1}').click()
            if data[4]=="Annual":
                plan="ANNUAL"
            elif data[4]=="30-day":
                plan="DAYS30"
            else:
                plan="DAYS10"
            self.driver.execute_script("arguments[0].scrollIntoView();",self.driver.find_element(By.XPATH,f'(//div[contains(@class,"m-0 form-group")])[{order}]'))
            ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH,f'(//div[@data-testid="charge-card-{plan}"])[{order}]')).click().perform()
            while True:
                try:
                    element=self.driver.find_element(By.XPATH,f'(//div[contains(@class,"border-success")])[{order}]')
                    if element:break
                except:
                    ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH,f'(//div[@data-testid="charge-card-{plan}"])[{order}]')).click().perform()
            time.sleep(5)
            if order<len(details):
                self.driver.find_element(By.XPATH,'//button[contains(@class,"btn-danger") and contains(@class,"kit__button")]').click()
                order+=1
        self.driver.execute_script("arguments[0].scrollIntoView();",self.driver.find_element(By.XPATH,'//button[contains(@class,"w-100")]'))
        self.driver.find_element(By.XPATH,'//button[contains(@class,"w-100")]').click()
        time.sleep(3)
        self.driver.quit()

ignis=Ecommerce()
ignis.placeOrder()