import requests
import os
import time
from bs4 import BeautifulSoup
import re
import urllib
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as messagebox
# import tkinter.messagebox as messagebox

s=requests.session()

class Application(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.grid()



    def center_window(self, width, height):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.master.geometry(size)

    def createWidgets(self):
        self.break_photo()
        self.zhanghaoLabel = Label(self, text="账号：")
        self.zhanghaoLabel.grid(row=0,column=0)
        # self.zhanghao_value = StringVar()
        # self.zhanghao_value.set('此处可设置学号默认值')
        # self.zhanghaoInput = Entry(self,textvariable=self.zhanghao_value)
        self.zhanghaoInput = Entry(self)
        self.zhanghaoInput.grid(row=0, column=1)

        self.mimaLabel=Label(self,text="密码：")
        self.mimaLabel.grid(row=1,column=0)

        # self.mima_value = StringVar()
        # self.mima_value.set('此处可设置密码默认值')
        # self.mimaInput = Entry(self,show="*",textvariable=self.mima_value)
        self.mimaInput = Entry(self, show="*")
        self.mimaInput.grid(row=1, column=1)

        self.yanzhenmaLabel= Label (self,text='验证码:')
        self.yanzhenmaLabel.grid(row=2,column=0)
        self.yanzhenmaInput=Entry(self)
        self.yanzhenmaInput.grid(row=2,column=1)

        self.loginButton = Button(self, text='登陆',command=self.login)
        self.loginButton.grid(row=3,column=1)
        self.selectButton = Button(self, text='查询成绩', state='disabled')
        self.selectButton.grid(row=5, column=2)


        self.xuenianLabel = Label(self, text="选择学年：")
        self.xuenianLabel.grid(row=4, column=0)

        self.comboxlist_xuenian = ttk.Combobox(self,state='disabled')  # 初始化
        self.comboxlist_xuenian.grid(row=4, column=1)

        self.xueqiLabel = Label(self, text="选择学期：")
        self.xueqiLabel.grid(row=5, column=0)

        self.comboxlist_xueqi= ttk.Combobox(self,state='disabled')  # 初始化 设置为只读模式
        self.comboxlist_xueqi["values"] = ('1','2','3')
        self.comboxlist_xueqi.grid(row=5, column=1)

    def break_photo(self):
        try:
            imgUrl = "http://117.35.118.209/CheckCode.aspx"
            imgresponse = s.get(imgUrl, stream=True)
            image = imgresponse.content
            DstDir = os.getcwd() + "\\"
            # print("保存验证码到："+DstDir+"yjm.jpg"+"\n")
            try:
                with open(DstDir + "yzm.jpg", "wb") as jpg:
                    jpg.write(image)
            except IOError:
                print("IO Error\n")
            finally:
                jpg.close
            self.photo = PhotoImage(file='yzm.jpg')
            self.yzmphoto = Button(self, image=self.photo, relief='ridg', bd=0, width=72, height=27,command=self.break_photo)
            self.yzmphoto.grid(row=2, column=2)
        except:
            messagebox.showerror('警告', '请检查网络状况，确认网络链接正常再次重启本程序！')
            quit()


    def login(self):
        if self.zhanghaoInput.get()=='':
            messagebox.showinfo("警告","请输入账号！")
            return
        if self.mimaInput.get()=='':
            messagebox.showinfo("警告","请输入密码！")
            return
        if self.yanzhenmaInput.get()=='':
            messagebox.showinfo("警告","请输入验证码！")
            return
        xh=self.zhanghaoInput.get()
        ma=self.mimaInput.get()
        yanzhenma=self.yanzhenmaInput.get()
        url = 'http://117.35.118.209/default2.aspx'
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        __VIEWSTATE = soup.input.get('value')
        data = {
            '__VIEWSTATE': __VIEWSTATE,
            'txtUserName': xh,
            'Textbox1': '',
            'TextBox2': ma,
            'txtSecretCode': yanzhenma,
            'RadioButtonList1': '%D1%A7%C9%FA',
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': '',
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        r = s.post(url, data=data, headers=headers)
        b = str(r.url)
        if b[-6:].isdigit():
            '''---------------------------------------获取入学年份-------------------------------------------'''
            kbur = 'http://117.35.118.209/xsgrxx.aspx?xh=' + self.zhanghaoInput.get() + '&gnmkdm=N121501'
            headers = {
                'Referer': 'http://117.35.118.209/xs_main.aspx?xh=' + self.zhanghaoInput.get(),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
            }
            l = s.post(kbur, headers=headers)
            soup = BeautifulSoup(l.text, 'lxml')
            shijian = soup.find_all('span', attrs={"id": "lbl_dqszj"})
            result = re.match('^\[<span\sid="lbl_dqszj">(.*?)</span>\]', str(shijian))
            shijian = result.group(1)
            list_shijian=[]
            for x in range(int(time.strftime("%Y")) - int(shijian)):
                b = shijian + "-" + str(int(shijian) + 1)
                list_shijian.append(b)
                shijian = str(int(shijian) + 1)
            if len(list_shijian)>4:
                self.comboxlist_xuenian["values"] = list_shijian[0:4]
            else:
                self.comboxlist_xuenian["values"] = list_shijian
            '''--------------------------------------弹出提示-------------------------------------------'''
            messagebox.showinfo('警告', '登录成功！')
            self.comboxlist_xuenian.configure(state='readonly')
            self.comboxlist_xueqi.configure(state='readonly')
            self.loginButton.configure(state='disabled')
            self.selectButton.configure(state='normal',command=self.get_chenji)
            # self.loginButton = Button(self, text='登陆', state='disabled')
            # self.loginButton.grid(row=3, column=1)
            # self.selectButton = Button(self, text='查询', command=self.get_chenji)
            # self.selectButton.grid(row=5, column=2)
        else:
            messagebox.showinfo('警告', '登录失败！请重试！\n请检查账号和密码是否真确！')
            self.break_photo()


    def get_chenji(self):
        if self.comboxlist_xuenian.get()=='':
            messagebox.showinfo("警告","请选择学年！")
            return
        if self.comboxlist_xueqi.get()=='':
            messagebox.showinfo("警告","请选择学期！")
            return
        else:
            kburl = 'http://117.35.118.209/Xscjcx.aspx?xh=' +self.zhanghaoInput.get()+ '&gnmkdm=N121613'
            headers1 = {
                'Referer':'http://117.35.118.209/xs_main.aspx?xh='+self.zhanghaoInput.get(),
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
            }
            l = s.post(kburl, headers=headers1)
            soup = BeautifulSoup(l.text, 'lxml')
            __VIEWSTATE1 = soup.find_all('input', attrs={"name": "__VIEWSTATE"})[0]
            __VIEWSTATE1 = str(__VIEWSTATE1)
            result = re.match('^<input\sname="__VIEWSTATE"\stype="hidden"\svalue="(.*?)"/>', __VIEWSTATE1)
            __VIEWSTATE1 = result.group(1)

            headers2 = {
                'Referer': l.url,
                'Host': '117.35.118.209',
                'Origin': 'http://117.35.118.209',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
            }
            data1 = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': __VIEWSTATE1,
                'hidLanguage': '',
                'ddlXN': self.comboxlist_xuenian.get(),
                'ddlXQ': self.comboxlist_xueqi.get(),
                'ddl_kcxz': '',
                'btn_xq': '%D1%A7%C6%DA%B3%C9%BC%A8',
            }
            liebiao = []
            l = s.post(l.url, headers=headers2, data=data1)
            soup = BeautifulSoup(l.text, 'lxml')
            for tabb in soup.findAll('table')[1:2]:
                for trr in tabb.findAll('tr'):
                    for tdd in trr.findAll('td'):
                        str1 = (str(list(tdd)))
                        liebiao.append(str1)
            liebiao = liebiao[15:]
            chenji = ''
            achievement=''
            for x in range(1, len(liebiao) + 1):
                chenji1 = liebiao[x - 1]
                chenji = chenji + str(chenji1)
                if (x % 15 == 0):
                    result = re.match('^\[.*?\]\[.*?\]\[.*?\]\[\'(.*?)\'\]\[.*?\]\[.*?\]\[.*?\]\[.*?\]\[\'(.*?)\'\]\[.*?\]\[.*?\]\[.*?\]\[.*?\]\[.*?\]\[.*?\]',chenji)
                    achievement=achievement+result.group(1)+':'+result.group(2)+'\n'
                    chenji = ''
            messagebox.showinfo(self.comboxlist_xuenian.get()+'学年，第'+self.comboxlist_xueqi.get()+'学期成绩',achievement)

app = Application()
# 设置窗口标题:
# 设置窗口大小
app.center_window(310,160)
app.master.resizable(0, 0)
app.createWidgets()
app.master.title('登陆正方教务系统')
# 主消息循环:
app.mainloop()