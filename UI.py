from asyncio.windows_events import NULL
from tkinter import StringVar
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from random import randint
from tkinter import font as tkFont
from openpyxl import load_workbook
import pyautogui
import export
import pandas as pd
import os.path
import os
import pyexcel as p
import winreg
import shutil

import project3.project3 as pr3

from main import ans

questionToDes = ''
wantToDes = ''
ansToDes = ''

def cut(question,want,des,user_id):
    global questionToDes,wantToDes,ansToDes
    question_input = question.get("1.0", "end-1c")
    want = want.get("1.0", "end-1c")
    sql_question = question_input
    sql_want = want
    print(des)
    des.delete(1.0,END)
    ######取得TEXT
    fp = open('project1/input/Description'+".txt", "a")
    fp.truncate(0)
    fp.write(question_input)
    fp.close()
    fp = open('project1/input/Want'+".txt", "a")
    fp.truncate(0)
    fp.write(want)
    fp.close()
    ######斷詞 https://github.com/fxsjy/jieba
    
    ansToDes = ans()

    print('ans: ' + ansToDes)
    
    if(user_id != 'NULL'):
        db,cur = connect()
        sql = "INSERT INTO question (user_id,question,want,answer) VALUES (" + '"' + str(user_id) + '","' + str(sql_question) + '","' + str(sql_want) + '","' + str(ans) +'")'
        print(sql)
        cur.execute(sql)
        db.commit()
    print('text1',question_input)
    print('text2',want)
    des.insert(INSERT, ansToDes)
    questionToDes = question_input
    wantToDes = want
    return question_input,want

def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]

def clearAll(question,want,des):
    question.delete(1.0,END)
    want.delete(1.0,END)
    des.delete(1.0,END)

def saveAll():
    desktop = get_desktop()
    if not os.path.isdir(desktop + '/AI_DATA'):
        os.mkdir(desktop+'/AI_DATA')
    print(desktop)
    shutil.copyfile('Description.txt',desktop+'/AI_DATA/Description.txt')
    shutil.copyfile('Want.txt',desktop+'/AI_DATA/Want.txt')
    if os.path.isfile('句子語意網路.jpg'):
        shutil.copyfile('句子語意網路.jpg',desktop+'/AI_DATA/句子語意網路.jpg')
    if os.path.isfile('問題語意網路.jpg'):
        shutil.copyfile('問題語意網路.jpg',desktop+'/AI_DATA/問題語意網路.jpg')
    if os.path.isfile('命題語意網路.jpg'):
        shutil.copyfile('命題語意網路.jpg',desktop+'/AI_DATA/命題語意網路.jpg')

def printans(des):
    global ansToDes
    des.delete(1.0,END)
    des.insert(INSERT, ansToDes)

def printcut(des):
    global questionToDes,wantToDes
    des.delete(1.0,END)
    des.insert(INSERT, str(questionToDes) +  '\n')
    des.insert(INSERT, str(wantToDes))

def addData(name,listbox):
    name = name.get("1.0", "end-1c")
    
    listbox = listbox.get(listbox.curselection())
    print(name,listbox)
    fp = open('cutfunc/' + listbox +  ".txt", "a",encoding='UTF-8')
    fp.writelines("\n" + name + " " + listbox)
    fp.close()
    print('Finish')

def createNewWindow(app):
    newWindow = Toplevel(app)
    Label(newWindow,text="名稱").pack(side=TOP,anchor=W,pady=5,padx=10)
    name = Text(newWindow,height=5,width=40)
    name.pack(side=TOP,anchor=W,padx=10)
    Label(newWindow,text="詞性").pack(side=TOP,anchor=W,pady=5,padx=10)

    ######ListBox 
    listbox = Listbox(newWindow)
    listbox.pack()
    for item in ["v", "pv", "nv", "n", "adj", "adv", "equal", "name", "int" ,"total", "place", "range", "special", "total", "time" , "u", "unit"]:
        listbox.insert(END, item)

    ######Button
    buttonExample = Button(newWindow,command=lambda:addData(name,listbox), text = "新增")
    buttonExample.pack()

def save():
    desktop = get_desktop()
    if not os.path.isdir(desktop + '/AI_DATA'):
        os.mkdir(desktop+'/AI_DATA')
    print(desktop)
    shutil.copyfile('cutfunc/dict.txt',desktop+'/AI_DATA/dict.txt')

def createDict(app):
    newWindow = Toplevel(app)
    newWindow.geometry('200x750')
    Label(newWindow,text="詞性").pack(side=TOP)
    Label(newWindow,text="v 一般動詞").pack(side=TOP)
    Label(newWindow,text="pv 正向動詞").pack(side=TOP)
    Label(newWindow,text="nv 負向動詞").pack(side=TOP)
    Label(newWindow,text="n 名詞").pack(side=TOP)
    Label(newWindow,text="u 虛詞").pack(side=TOP)
    Label(newWindow,text="adv 副詞").pack(side=TOP)
    Label(newWindow,text="int 整數").pack(side=TOP)
    Label(newWindow,text="adj 形容詞").pack(side=TOP)
    Label(newWindow,text="name 名字").pack(side=TOP)
    Label(newWindow,text="time 時間").pack(side=TOP)
    Label(newWindow,text="unit 單位").pack(side=TOP)
    Label(newWindow,text="equal 等於").pack(side=TOP)
    Label(newWindow,text="place 地方").pack(side=TOP)
    Label(newWindow,text="range 範圍").pack(side=TOP)
    Label(newWindow,text="total 總和").pack(side=TOP)
    Label(newWindow,text="special 特殊詞").pack(side=TOP)
    Label(newWindow,text="bigger 大").pack(side=TOP)
    Label(newWindow,text="smaller 小").pack(side=TOP)
    Label(newWindow,text="passive 被動詞").pack(side=TOP)

    Button(newWindow,command=lambda:save() ,text = "另存新檔").pack()

def main(account,user_id):
    ######Frame規劃
    window = Tk()
    L = Frame(window)
    R = Frame(window)
    window.title('人工智慧數學應用問題解題系統')
    window.geometry('900x900')
    helv36 = tkFont.Font(family='Helvetica', size=30, weight='bold')
    Label(L,text="題目",fg="RED").pack(side=TOP,anchor=W,pady=5,padx=10)
    question = Text(L,height=4,font=helv36,width=20)
    question.pack(side=TOP,anchor=W,padx=10)

    Label(L,text="求解").pack(side=TOP,anchor=W,pady=5,padx=10)
    want = Text(L,height=4,font=helv36,width=20)
    want.pack(side=TOP,anchor=W,padx=10)

    Label(L,text="說明").pack(side=TOP,anchor=W,pady=5,padx=10)
    des = scrolledtext.ScrolledText(L,height=4,width=20,font=helv36,bg='white')
    des.pack(side=TOP,anchor=W,pady=5,padx=10)
    Button(L,command=lambda:cut(question,want,des,user_id),text="執行",font=helv36,width=5).pack(side=LEFT,padx=16)
    Button(L,text="返回",command=lambda:clearAll(question,want,des),font=helv36,width=5).pack(side=LEFT,padx=16)
    Button(L,command=lambda:saveAll(),font=helv36,text="輸出",width=5).pack(side=LEFT,padx=16)
    L.pack(side=LEFT, fill=BOTH)
    
    Button(R,command=lambda:printans(des),font=helv36,text="答案",width=20).pack(side=TOP,pady=10,padx=10)
    Button(R,command=lambda:printcut(des),font=helv36,text="斷詞",width=20).pack(side=TOP,pady=20,padx=10)
    Button(R,command=lambda:pr3.new_page("句子語意網路"),font=helv36,text="句子",width=20).pack(side=TOP,pady=10,padx=10)
    Button(R,command=lambda:pr3.new_page("命題語意網路"),font=helv36,text="命題",width=20).pack(side=TOP,pady=10,padx=10)
    Button(R,command=lambda:pr3.new_page("問題語意網路"),font=helv36,text="問題",width=20).pack(side=TOP,pady=10,padx=10)
    #Button(R,command=lambda:createNewWindow(window),text="說明",width=20,height=2).pack(side=TOP,pady=20,padx=10)
    Button(R,command=lambda:createNewWindow(window),font=helv36,text="辭庫新增",width=20).pack(side=TOP,pady=10,padx=10)
    Button(R,command=lambda:createDict(window),font=helv36,text="詞性對照表",width=20).pack(side=TOP,pady=10,padx=10)
    # Button(R,command=lambda:history(user_id),font=helv36,text="歷史紀錄",width=20).pack(side=TOP,pady=10,padx=10)
    R.pack(side=RIGHT, fill=BOTH)
    window.mainloop()

main('terry', 'NULL')



