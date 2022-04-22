import tkinter
from functools import partial


def com(top, n, list1):
    top.destroy()
    n = str(n)
    list1.append(n)


def login():
    n = []
    top = tkinter.Tk()
    top.title('登录选项')
    top.geometry('200x150')
    l1 = tkinter.Label(top, text='选择登录方式')
    b1 = tkinter.Button(top, text='账号表中的账号', width=15, height=1, command=partial(com, top, 1, n))
    b2 = tkinter.Button(top, text='上一次登录用的账号', width=15, height=1, command=partial(com, top, 3, n))
    b3 = tkinter.Button(top, text='临时账号', width=15, height=1, command=partial(com, top, 2, n))
    l1.place(x=60, y=0)
    b1.place(x=40, y=30)
    b2.place(x=40, y=70)
    b3.place(x=40, y=110)
    top.mainloop()
    return n[0]


def choice(zh):
    try:
        top = tkinter.Tk()
        top.title('账号')
        top.geometry('200x'+str(30+len(zh)*30))
        l1 = tkinter.Label(top, text='选择登录账号', font=12)
        l1.pack()
        n = []
        for i in range(len(zh)):
            t = tkinter.Button(top, text=str(zh[i]), width=15, height=1, command=partial(com, top, i, n))
            t.pack()
        top.mainloop()
        return n[0]
    except:
        return


def com1(top, e, list1):
    n = e.get()
    list1.append(n)
    top.destroy()


def input_str():
    top = tkinter.Tk()
    top.title('验证码')
    top.geometry('200x100')
    l = tkinter.Label(top, text="验证码", font=12)
    l.pack()
    e = tkinter.Entry(top)
    e.pack()
    n = []
    b = tkinter.Button(top, text="确定", command=partial(com1, top, e, n))
    b.pack()
    top.mainloop()
    return n[0]


def show():
    n = []
    top = tkinter.Tk()
    top.title('counting')
    top.geometry('300x100')
    l = tkinter.Label(top, text='没有默认的cookie,你可以选择', font=12)
    l.pack()
    b = tkinter.Button(top, text="cookie登录（免验证码）", command=partial(com, top, 1, n))
    b.place(x=20, y=50)
    c = tkinter.Button(top, text="账号密码登录", command=partial(com, top, 2, n))
    c.place(x=190, y=50)
    top.mainloop()
    return n[0]

