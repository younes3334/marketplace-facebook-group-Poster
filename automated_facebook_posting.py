import os
import time

import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager import chrome

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#uc.TARGET_VERSION = '99'





def image_dowloader(data):
    print("Downloading Images for the posts...")
    #Function to dowlond images
    #options = uc.ChromeOptions()
    options = webdriver.ChromeOptions()
    #options.add_argument('allow-elevated-browser')
    options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    #driver = uc.Chrome(options=options)
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    for i in range(len(data['Link'])):
        #launch URL
        driver.get(data["Link"][i])
        #open file in write and binary mode
        with open(f'images/{i}.png', 'wb') as file:
        #identify image to be captured
            l = driver.find_element(By.TAG_NAME,'img')
        #write file
            file.write(l.screenshot_as_png)
    #close browser
    driver.quit()
    print("Images donwloaded succefully !")

def posting(wait,driver,group_link,picture_path,title_data,price_data,description_data,tags_data):
    driver.get(links['groupe_url'][0])

    time.sleep(3)
    #Find the sell button and click it
    sellbutton = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Sell Something"]')))
    sellbutton.click()

    time.sleep(2)
    #Find the item sell button and click it
    itemsell = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'a8c37x1j.buofh1pr')))
    itemsell.click()
    time.sleep(2)

    #Fill in the information as required
    # Picture uploading
    photo_element = wait.until(EC.presence_of_element_located((By.XPATH,'//input[@accept="image/*,image/heif,image/heic"]')))
    photo_element.send_keys(picture_path)

    # Title uploading
    title = wait.until(EC.presence_of_element_located((By.XPATH,'//label[@aria-label="Title"]')))
    title.send_keys(title_data)

    # price uploading
    price = wait.until(EC.presence_of_element_located((By.XPATH,'//label[@aria-label="Price"]')))
    price.send_keys(price_data)

    # Condition uploading
    wait.until(EC.presence_of_element_located((By.XPATH,'//label[@aria-label="Condition"]'))).click()
    Condition = driver.find_element(By.XPATH,'//div[@role="listbox"]').find_elements(By.XPATH,'//div[@role="option"]')
    Condition[0].click()

    # Description uploading
    Description = driver.find_element(By.XPATH,'//label[@aria-label="Description"]')
    Description.send_keys(description_data)

    # Product tags uploading
    Product_tags = driver.find_element(By.XPATH,'//label[@aria-label="Product tags"]')
    Product_tags.send_keys(tags_data)

    # Next button
    Next_button = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@aria-label="Next"]')))
    Next_button.click()

    time.sleep(1)
    # Post in marketplace check
    post_market = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.mg4g778l.pfnyh3mw.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.btwxx1t3.abiwlrkh.p8dawk7l.lzcic4wl.ue3kfks5.pw54ja7n.uo3d90p7.l82x9zwi.a8c37x1j")))
    post_market[2].click()

    time.sleep(1)
    # Post button
    Post_button = driver.find_element(By.XPATH,'//div[@aria-label="Post"]')
    Post_button.click()
    time.sleep(4)

if __name__ == '__main__':

    print("\n\t******************************************")
    print("\n\tWelcome to the FacebookMarketPlace posting !")
    print("\n\t******************************************")

    print("\nUploading data...")
    data = pd.read_csv('data.csv')
    print("Data uploaded succefully!")

    #First Step
    #Download images
    image_dowloader(data)

    #option = uc.ChromeOptions()
    option = webdriver.ChromeOptions() 

    # Handling of Allow Pop Up In Facebook
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-notifications")

    """
        remove the " # " in the line 112 so it will be headless (that means the code will run and do the work whithout opening the browser)
    """
    #options.add_argument("--headless") 
    print("\nOpening the browser...")
    #driver = uc.Chrome(options=option)
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
    wait = WebDriverWait(driver, 10)
    print("Browser opened succefully")
    time.sleep(1)
    driver.maximize_window()

    #enter to facebook login page
    print("\nLogin to facebook ...")
    url = "https://www.facebook.com"
    time.sleep(1)
    driver.get(url)

    #connecting to the account
    time.sleep(2)
    usr = "info@macserver.se"
    pwd = "1234@Free"

    elem = driver.find_element(By.ID,"email")
    elem.send_keys(usr)

    # Enter user password
    elem = driver.find_element(By.ID,"pass")
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)

    time.sleep(2)
    print("Login to Facebook succefully")
    print("\nPosting....")
    for i in range(len(data)):
        #groupes links
        links = pd.read_excel('group_links.xlsx')
        for j in range(len(links)):
            posting(wait,driver,links['groupe_url'][j],os.getcwd()+f"\images\{i}.png",data["Title"][i],data["Price"][i],data["Description"][i],data["After description"][i])
            time.sleep(5)
        time.sleep(5)
        print("Content succefully posted. ")
    print("\n\tAll content are Posted :) ")
