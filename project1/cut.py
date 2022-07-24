import os
import xlwt
import pyexcel as p
from . cutfunc import cutfuc

def xlsToxlsx():
    files = os.listdir('project1/process/')
    newlist = []
    ######篩選副檔名
    for names in files:
        if names.endswith(".xls"):
            newlist.append(names)
    num = len(newlist)
    ######用pyexcel執行轉換 可多個
    for i in range(num):
        path = 'project1/process/' + newlist[i]
        a = newlist[i].split('.')
        b = 'project1/process/' + a[0] + '.xlsx'
        p.save_book_as(file_name=path,dest_file_name=b)

def output(s1,s2):
    book = xlwt.Workbook(encoding="utf-8")
    #使用Workbook裡的add_sheet函式來建立Worksheet
    sheet1 = book.add_sheet("Sheet1")
    filename = "斷詞.xls"
    for i in range(len(s1)):
        for key, value in s1[i].items(): #對應name跟element 
            sheet1.write(i,0,key)
            sheet1.write(i,1,value)
    for i in range(len(s2)):
        for key, value in s2[i].items():
            sheet1.write(i,4,key)
            sheet1.write(i,5,value)
    #將Workbook儲存為原生Excel格式的檔案
    book.save('project1/process/' + filename)

def cut():
    fp1 = open('project1/input/Description'+".txt", "r+")
    question_input = fp1.read()
    fp1.close()
    fp2 = open('project1/input/Want'+".txt", "r+")
    want = fp2.read()
    fp2.close()
    ######斷詞 https://github.com/fxsjy/jieba
    question_input = cutfuc.cutall(question_input)
    want = cutfuc.cutall(want)
    question = '題目:'
    ask = '求解:'
    for i in range(len(question_input)):
        for key, value in question_input[i].items():
            question += '[' + key + ':' + value + '],'
    for i in range(len(want)):
        for key, value in want[i].items():
            ask += '[' + key + ':' + value + '],'
    question = question[:-1]
    ask = ask[:-1]
    #des.insert(INSERT, question +  '\n')
    #des.insert(INSERT, ask)
    output(question_input,want)
    xlsToxlsx()
    print('done cut.py')

if __name__ == '__main__':
    cut()