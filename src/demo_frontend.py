from email.base64mime import body_encode
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import psycopg2
import random


def get_rand():
    cur.execute("select key from modesearch where list_id=%(x)s",
                {'x': random.randint(0, 228274)})  # 从数据库中查询
    info = cur.fetchall()
    key = info[0][0]
    cur.execute("select * from modesearch where key=%(x)s",
                {'x': key})  # 从数据库中查询
    info = cur.fetchall()
    if info:
        key = tk.Tk()
        key.title('随机查询结果')
        key.config(background='MintCream')
        key.state('zoomed')
        tk.Label(key, text='\n随机查询结果如下表所示:\n', font=(
            11), background='MintCream').pack()
        scrollbar = tk.Scrollbar(key)
        scrollbar.pack(side='right', fill='y')
        columns = ('id', 'antecedent', 'consequent',
                   'confidence', 'lift', 'support')
        headers = ('id', 'antecedent', 'consequent',
                   'confidence', 'lift', 'support')
        widthes = (100, 350, 200, 200, 200, 200)
        res_list = ttk.Treeview(
            key, show='headings', columns=columns, height=30, yscrollcommand=scrollbar.set)
        for (column, header, width) in zip(columns, headers, widthes):
            res_list.column(column, width=width, anchor='center')
            res_list.heading(column, text=header, anchor='center')
        for i, admin in enumerate(info):
            x = admin[1]
            x = x.split('+')
            key = ','.join(x)
            value = []
            value.append(admin[0])
            value.append(key)
            for j in admin[2:]:
                value.append(j)
            res_list.insert('', i, values=value)
        res_list.pack()
        scrollbar.config(command=res_list.yview)
        key.mainloop()
    else:
        tkinter.messagebox.showinfo(title='无结果', message='搜索结果为空')
        return


def get_data(x):
    x = x.split()
    x.sort()
    key = '+'.join(x)
    cur.execute("select * from modesearch where key=%(x)s",
                {'x': key})  # 从数据库中查询
    info = cur.fetchall()
    if info:
        key = tk.Tk()
        key.title('查询结果')
        key.config(background='MintCream')
        key.state('zoomed')
        tk.Label(key, text='\n查询结果如下表所示：\n', font=(
            11), background='MintCream').pack()
        scrollbar = tk.Scrollbar(key)
        scrollbar.pack(side='right', fill='y')
        columns = ('id', 'antecedent', 'consequent',
                   'confidence', 'lift', 'support')
        headers = ('id', 'antecedent', 'consequent',
                   'confidence', 'lift', 'support')
        widthes = (100, 350, 200, 200, 200, 200)
        res_list = ttk.Treeview(
            key, show='headings', columns=columns, height=30, yscrollcommand=scrollbar.set)
        for (column, header, width) in zip(columns, headers, widthes):
            res_list.column(column, width=width, anchor='center')
            res_list.heading(column, text=header, anchor='center')
        for i, admin in enumerate(info):
            x = admin[1]
            x = x.split('+')
            key = ','.join(x)
            value = []
            value.append(admin[0])
            value.append(key)
            for j in admin[2:]:
                value.append(j)
            res_list.insert('', i, values=value)
        res_list.pack()
        scrollbar.config(command=res_list.yview)
        key.mainloop()
    else:
        tkinter.messagebox.showinfo(title='无结果', message='搜索结果为空')
        return


if __name__ == '__main__':
    # 与数据库建立连接
    try:
        conn = psycopg2.connect(host="127.0.0.1",
                                database="bigdata_demo",
                                user="postgres",
                                password="psql")
        cur = conn.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

        # 用户登录页面
    windows = tk.Tk()
    windows.title('频繁模式查询')
    windows.config(background='MintCream')
    windows.state('zoomed')
    tk.Label(windows, text='\n\n请输入以下信息\n\n', font=(50),
             background='MintCream').pack()
    # 变量定义
    x = tk.StringVar()
    # 账号
    tk.Label(windows, text='啦 巴 视频 魔仙 \n', font=(20),
             background='MintCream').pack()
    tk.Entry(windows, show=None, font=(20),
             textvariable=x).pack(ipadx=150, ipady=10)
    tk.Label(windows, text='\n\n\n', font=(50),
             background='MintCream').pack()
    # 查询按键
    tk.Button(windows, text='查询', font=(30), height=2,
              width=6, command=lambda: [get_data(x.get())]).place(x=600, y=250)
    tk.Button(windows, text='随机查询', font=(50), height=2,
              width=10, command=get_rand).place(x=750, y=250)
    # 显示窗口
    windows.mainloop()

    # 断开与数据库的连接
    conn.close()
