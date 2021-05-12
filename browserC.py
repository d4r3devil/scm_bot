from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import threading
from pynput.keyboard import Key, Controller
import time
import datetime
from tkinter import messagebox 
import getpass
import os
import pickle
def run(url_lst,float_lst,cost_lst,sen,sen_pass,rec,name,page_time=5):#,head=False):
    lst_tab=[]
    reqs=0
    count=0
    here=0
    board = Controller()
    opt = Options()
    path=r'C:\\Users\\'+ getpass.getuser() + r'\Documents\\scm_bot'
    if (name+'.cook') in os.listdir(path):
        cookie_file=open('C:\\Users\\'+ getpass.getuser() + '\Documents\\scm_bot\\'+name+'.cook','rb')
        cookies=pickle.load(cookie_file)
        cookie_file.close()
    else:
        messagebox.showinfo("WARNING", "PROFILE NOT FOUND\nclick setup")
        return
    opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
    driver=webdriver.Chrome(executable_path='chromedriver.exe',options=opt)
    driver.get('https://chrome.google.com/webstore/detail/csgofloat-market-checker/jjicbefpemnphinccgikpdaagjebbnhg?hl=en')
    time.sleep(9)
    while True:
        time.sleep(3)
        try:
            print('trying to add to chrome')
            driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div/div/div/div').click()
            break       
        except:
            continue
    time.sleep(3)
    board.press(Key.tab)
    board.press(Key.space)
    #board=None
    driver.get('https://steamcommunity.com/market/listings/730/P250%20%7C%20Sand%20Dune%20%28Battle-Scarred%29')
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    page_size = Select(driver.find_element_by_id("pageSize"))
    page_size.select_by_index(4)
    for i in range (1,len(url_lst)):
        driver.execute_script('window.open("","_blank");')
    lst_tab=driver.window_handles
    for i in range(0,len(lst_tab)):
        driver.switch_to_window(lst_tab[i])
        driver.get(url_lst[i])
        reqs+=1
    lst_tab=driver.window_handles
    print('checking started')
    while True:
        for i in range(0,len(lst_tab)):
            reqs+=1
            try:   #incase tab closed
                driver.switch_to_window(lst_tab[i])
            except:
                print('this tab closed')
                del lst_tab[i]
                del float_lst[i]
                del cost_lst[i]
                i-=1
                continue
                #driver.execute_script('window.open("","_blank");')
                #driver.get(url_lst[i])
                #lst_tab=driver.window_handles
            time.sleep(page_time)
            print(datetime.datetime.now())
            try:
                #fnd the sort button and click
                sort=driver.find_element_by_xpath('//*[@id="csgofloat_sort_by_float"]')#'/html/body/div[1]/div[7]/div[2]/div[1]/div[4]/div[1]/div[3]/div[4]/div[2]/a[1]')
                for so in range(0,3):
                   sort.click()
            except:
                print('sort button not found in',lst_tab[i],'\n retrying next round')
                count+=1
                if count==6:
                    count=0
                    print('requests made from the start=',reqs)
                    reqs=0
                    time.sleep(500)
                driver.refresh()
                continue
            time.sleep(0.5)
            #print('checking floats')
            try:    
                for j in range(2,12):
                            #fnd the float and check
                            here=64
                            fl='/html/body/div[1]/div[7]/div[2]/div[1]/div[4]/div[1]/div[3]/div[4]/div[4]/div['+ str(j) +']/div[4]/div/div[1]'
                            fl=driver.find_element_by_xpath(fl)  
                            fl=float(fl.text[7:-4])
                            if fl<=float_lst[i]:
                                here=69
                                cost= '/html/body/div[1]/div[7]/div[2]/div[1]/div[4]/div[1]/div[3]/div[4]/div[4]/div['+str(j)+']/div[2]/div[2]/span/span[1]'
                                #print('checking cost')
                                cost=float(driver.find_element_by_xpath(cost).text[2:])
                                if cost<=cost_lst[i]:
                                    here=74
                                    buy='/html/body/div[1]/div[7]/div[2]/div[1]/div[4]/div[1]/div[3]/div[4]/div[4]/div['+ str(j) +']/div[2]/div[1]/div/a/span'
                                    buy=driver.find_element_by_xpath(buy)
                                    buy.click()
                                    print('buying item')                 
                                    chk_box=driver.find_element_by_xpath('//*[@id="market_buynow_dialog_accept_ssa"]')
                                    print('check box encounter')
                                    if chk_box.is_selected()==False:#to click check box for first list
                                        here=80  
                                        ti=time.perf_counter()
                                        while True:
                                            try:
                                                chk_box.click()
                                            except:
                                                if time.perf_counter()-ti>=3:
                                                    break
                                                continue
                                        print('check box clicked')
                                    here=85
                                    buy=driver.find_element_by_xpath('//*[@id="market_buynow_dialog_purchase"]')
                                    #/html/body/div[3]/div[3]/div/div[7]/div/div/div[2]/a[1]
                                    buy.click() 
                                    print('buy clicked')                                         
                                    while True:
                                            try:
                                                close=driver.find_element_by_xpath('//*[@id="market_buynow_dialog_close"]')
                                                #/html/body/div[3]/div[3]/div/div[8]/div/a[1]
                                                close.click()
                                            except:
                                                try:
                                                    driver.find_element_by_xpath('//*[@id="market_buynow_dialog_purchase"]').click()
                                                    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div').click()#cancel button
                                                    print('cancel clicked')
                                                    break
                                                except:
                                                    continue
                                            print('close clicked')
                                            break
            except:
               print('error check loop at:',here)
               driver.refresh() 
               continue
            driver.refresh()
     
           
def setup(name):
    opt=Options()
    #opt.add_extension(os.getcwd() +'\\float.crx')
    path=r'/home/'+ getpass.getuser() + r'/Documents/'
    folds=os.listdir(path)
    if 'scm_bot' not in folds:
        os.system('mkdir '+path + 'scm_bot/')
    cookies_c=open(path+name+'.cook','wb')
    driver=webdriver.Chrome(executable_path='chromedriver.exe',options=opt)
    driver.get('https://steamcommunity.com/login/home/')
    messagebox.showinfo("INSTRUCTION", "1.LOGIN IN WITH WORKING STEAM ACCOUNT\n\n2.click OK")
    cookies=driver.get_cookies()
    pickle.dump(cookies,cookies_c)
    cookies_c.close()
    driver.close()