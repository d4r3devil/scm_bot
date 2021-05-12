from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import time
from tkinter import messagebox 
import getpass
import os
import pickle
def run(url_lst,float_lst,cost_lst,sen,sen_pass,rec,name):#,head=False):
    lst_tab=[]
    reqs=0
    count=0
    here=0
    page_time=5#time to wait on each skin in given list of skins
    path=r'/home/'+ getpass.getuser() + r'/Documents/scm_bot/'
    if (name+'.cook') in os.listdir(path):
        cookies_f=open(path +name+'.cook','rb')
        cookies=pickle.load(cookies_f)
        cookies_f.close()
    else:
        messagebox.showinfo("WARNING", "PROFILE NOT FOUND\nclick setup")
        return
    fp = webdriver.FirefoxProfile()
    fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0")
    driver = webdriver.Firefox(fp,executable_path='./geckodriver.exe')
    driver.install_addon(os.getcwd() +'/float.xpi', temporary=False)
    driver.get('about:preferences')
    messagebox.showinfo("INSTRUCTION", "1.CLICK ON CHECK BOX CONTAINING OPEN LINKS IN NEW TABS\n INSTEAD OF NEW WINDOWS\n\n2.click OK")
    driver.get('https://steamcommunity.com/')
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
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
        ti2=time.perf_counter()
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
            try:
                #fnd the sort button and click
                sort=driver.find_element_by_xpath('//*[@id="csgofloat_sort_by_float"]')#'/html/body/div[1]/div[7]/div[2]/div[1]/div[4]/div[1]/div[3]/div[4]/div[2]/a[1]')
                #for so in range(0,3):
                 #   sort.click()
                    #sort.send_keys(Keys.RETURN)
            except:
                print('sort button not found in',lst_tab[i],'\n retrying next round')
                count+=1
                if count==6:
                    if time.perf_counter-ti2<=15:
                        count=0
                        print('requests made from the start=',reqs)
                        reqs=0
                        time.sleep(500)
                        ti2=time.perf_counter()
                    driver.refresh()
                continue
            time.sleep(0.5)
            #print('checking floats')
            try:    
                for j in range(2,103):
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
                                        #while True:
                                         #   try:
                                        chk_box.send_keys(Keys.SPACE)
                                          #  except:
                                           #     if time.perf_counter()-ti>=3:
                                            #        break
                                             #   continue
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
                                                    driver.find_element_by_xpath('//*[@id="market_buynow_dialog_purchase"]')
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
    path=r'/home/'+ getpass.getuser() + r'/Documents'
    folds=os.listdir(path)
    if 'scm_bot' not in folds:
        os.system('mkdir ' +path +'/scm_bot')
    cookies_f=open(path +'/scm_bot/' +name+'.cook','wb')
    fp = webdriver.FirefoxProfile()
    #path to default profile:  C:\Users\DELL\AppData\Roaming\Mozilla\Firefox\Profiles
    fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0")
    driver = webdriver.Firefox(fp,executable_path='./geckodriver.exe')
    driver.install_addon(os.getcwd() +'/float.xpi', temporary=False)
    driver.get('https://steamcommunity.com/login/home/')
    messagebox.showinfo("INSTRUCTION", "1.LOGIN IN WITH WORKING STEAM ACCOUNT\n\n2.click OK")
    cookies=driver.get_cookies()
    pickle.dump(cookies,cookies_f)
    cookies_f.close()
    driver.close()
