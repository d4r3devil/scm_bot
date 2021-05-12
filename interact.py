import browser as bbf
import browserC as bbc 
from tkinter import *
import sys
url_lst=[]
float_lst=[]
cost_lst=[]
rec=''
sen=''
sen_pass=''

def use_conf(name):
    global rec,sen,sen_pass,url_lst,float_lst,cost_lst
    url_lst=[]
    float_lst=[]
    cost_lst=[]
    try:
        if name[0].isalnum()==False:
                name=name[1:-1]
        file=open(name,'r')
    except FileNotFoundError:
        report('invalid')
    except IndexError:
        report('missing')

    f=file.readlines()
    file.close()
    try:
        t= f[0][6:-3] + ', '
        while len(t)>1:
            ind=t.find(',')
            url_lst.append(t[0:ind])
            t=t[ind+1:]    
        t=f[1][8:-3] + ', '
        while len(t)>1:
            ind=t.find(',')
            float_lst.append(float(t[0:ind]))
            t=t[ind+1:] 
        t= f[2][7:-3] + ', '  
        while len(t)>1:
            ind=t.find(',')
            cost_lst.append(float(t[0:ind]))
            t=t[ind+1:]    
        rec=f[3][10:-3]    
        sen=f[4][8:-3]
        sen_pass=f[5][6:-2]
    except:
        report('fileerror')
    
def report(rep):
    if rep=='missing':
        messagebox.showinfo("ERROR", "no file name given--type a text file name")
    elif rep=='invalid':
        messagebox.showinfo("ERROR", "file does not exist")
    elif rep=='fileerror':
        messagebox.showinfo("ERROR", "error in config file\n check values")
    else:
        print('check report code')
    
def start():
    use_conf(fname.get())
    if brow.get()==1:
        bbf.run(url_lst,float_lst,cost_lst,sen,sen_pass,rec,prof.get(),int(page_time.get()))
    if brow.get()==0:
        bbc.run(url_lst,float_lst,cost_lst,sen,sen_pass,rec,prof.get(),int(page_time.get()))        
def setup():
    if brow.get()==1:
        bbf.setup(prof.get())
    if brow.get()==0:
        bbc.setup(prof.get())
#if len(sys.argv)==5:
 #   if sys.argv[1]=='setup' and sys.argv[2]=='firefox':
  #      bbf        
top=Tk()
top.geometry("280x120")
labelp=Label(top,text="  profile name: ",)
prof=Entry(top)
brow=IntVar(top)
chr=Radiobutton(top,text="chrome",variable=brow,value=0)
frx=Radiobutton(top,text="firefox",variable=brow,value=1)
label=Label(top,text="  config file name or path:",)
fname=Entry(top)
labelt=Label(top,text=" time spent on each page:",)
page_time=Entry(top)
page_time.insert(-1,'5')

b_start=Button(top,text="START",command=start,activebackground="green",activeforeground="white")
b_setup=Button(top,text="SETUP",command=setup,activebackground="blue",activeforeground="white")
labelp.grid(row=0,column=0)
prof.grid(row=0,column=1)
chr.grid(row=1,column=0)
frx.grid(row=1,column=1)
label.grid(row=2,column=0)
fname.grid(row=2,column=1)
labelt.grid(row=3,column=0)
page_time.grid(row=3,column=1)
b_start.grid(row=4,column=0)
b_setup.grid(row=4,column=1)
top.mainloop()