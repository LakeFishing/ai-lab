##畫出句子語意網路

##使用的function: draw(cv,sheet) => 整理excel的資料，把圖畫出來

##流程 :

##import p3_read，把excel的sheet，傳到p3_read.read這個function中，去處理excel的資訊

##p3_read.read 大致用途 : 把[主事者、接受者]、[物品、數量、單位、特點、時間點、發生地]、[+-=大小前後]等，進行分類，輸出5個list

## 讀取完畢後，根據前面return 出來的各個list開始畫圖



from tkinter import *
from random import randint
import pyautogui
from openpyxl import load_workbook
from . import p3_read

oval_w = 60 #橢圓的寬
oval_h = 30   #橢圓的高


def draw(cv,sheet):  ##畫出句子語意網路
    print()
    print("句子語意網路")
    
    ##主事者與接受者座標
    
    mid_x = 100 ##中間的x
    mid_y = 50  ##中間的y
    
    init_x = mid_x ##起始的x
    init_y = mid_y ##起始的y
    
    left_x = mid_x ##左邊的x
    left_y = mid_y ##左邊的y
    
    right_x = mid_x ##右邊的x
    right_y = mid_y ##右邊的y

    addx = 50 ##x座標增加幅度
    addy = 80 ##y座標增加幅度

    max_width = 0
    max_height = 50
    
    ##主事者與接受者座標

    keys1 = []  ##主事者或接受者名稱

    keys2 = []  ##物品 數量  單位  (名稱)
        
    keys3 = []  ##物品 數量  單位   (標籤)

    keys4 = []   ##+-=大小前後

    keys5 = []   ##+-=大小前後名稱

    name = ""  ##主事者接受者名稱(只有一人時)
    name1=""    ##主事者接受者名稱(兩人時)
    name2=""    ##主事者接受者名稱(兩人時)

    
    
    times = 0

    coor_name = []   ##紀錄人物標籤名稱與座標(用不到)

    coor_item = []   ##紀錄物品數量單位標籤名稱與座標(用不到)

    coor_plus = []  #(用不到)

    coor_x = 0
    coor_y = 0

    word1=word2=""  ##紀錄這句話的運算符號(+-=...)

    
    
    keys1,keys2,keys3,keys4,keys5,is_plus,is_remain,is_do,is_total,change_plus,plus_one,add_back,no_have = p3_read.read(keys1,keys2,keys3,keys4,keys5,sheet,"img")
    ##把excel的資料進行處理，return 出list(這邊除了keys1~keys5)，其他可以省略不看
    print("讀取excel，做處理")
    
    print("keys1",keys1)
    print("keys2",keys2)
    print("keys3",keys3)
    print("keys4",keys4)
    print()

    ##例子 : 小明有3顆蘋果，媽媽給他2顆。小明有幾顆蘋果?

    #keys1 : [['小明'], ['媽媽', '小明']]
    #keys2 : [['蘋果', 3, '顆'], ['蘋果', 2, '顆']]
    #keys3 : [['物品', '數量', '單位'], ['物品', '數量', '單位']]
    #keys4 : [['='], ['-']]
    #keys5 : [['有'], ['給']]

    for i in range(len(keys1)):  ##根據句數以及主事者接受者數量進行繪圖

        mid_y = init_y   ## 每一句話開始時，將起始的y，設為預設值
        
        count = 0 ##判斷是否要標註標籤

        item1 = keys2[i]       ##物品 數量  單位  (名稱)
        item2 = keys3[i]       ##物品 數量  單位  (標籤)
        
        print("第",str(i+1),"句")
        

        if len(keys1[i])==1 :   ##如果主事者接受者數量為1
            
            print("主事者接受者數量為1")
               
            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")   ##先畫出基底的圓
            
            
            name = keys1[i][0] 
            
                
            cv.create_text(mid_x,mid_y,text=name,font=("標楷體",10))   ##標註主事者
            
            print("畫出主事者:",name,"，座標 : ",str(mid_x),str(mid_y))
            
            
            cv.create_line(mid_x,init_y+oval_h/2,mid_x,init_y+oval_h/2+60)  ##先畫出直線
            cv.create_text((mid_x)-10,((init_y+oval_h/2)*2+60)/2,text=str(keys4[i][0]),font=("標楷體",10))  ##標註+-=
            
            print("標註運算符號:",keys4[i][0],"，座標 : ",str((mid_x)-10),str(((init_y+oval_h/2)*2+60)/2))
            
            mid_y = init_y+oval_h/2+60 ##y座標往下推
           
            print("y座標往下推，畫出物品數量單位特點時間點發生地等")

            for j in range(len(item1)):       ##把物品、數量、單位、特點...等畫出來
                
                if count==0: ##如果為0，則不須標註標籤，只需##先畫出圓、標註詞
                    if item1[j]!=name:
                        cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                        cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                        coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])   ##存下物品 數量  單位跟座標
                        count+=1
                else: ##如果不為0，則須標註標籤，接者畫出圓、標註詞
                    if item1[j]!=name:
                        cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                        cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[j],font=("標楷體",10))
                        
                        mid_y+=60
                        cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                        cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                        coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])   ##存下物品 數量  單位跟座標
                        
                
                
                print((item1[j]),"，座標:",str(mid_x+oval_w/2),str(mid_y))
                
                if max_width<= mid_x:
                    max_width = mid_x+50

                if max_height<=mid_y:
                    max_height=mid_y+100

                    

            ##1句話結束後，mid_x往右推，mid_y回到初始
            mid_x +=150
            right_x=mid_x
            mid_y = init_y+oval_h/2+60




        else:   ##如果主事者接受者數量為2

            print("主事者接受者數量為2")
            if len(keys1[i])==2 or (len(keys1[i])==0 and keys3[i].count("物品")==2):   ##如果主事者接受者有兩個
                
                ##如果第一個符號為+，則對應到第二個為-，如果第一個符號為-，則對應到第二個為+
                if keys4[i][0]=="+":
                    word1="+"
                    word2="-"
                elif keys4[i][0]=="-":
                    word1="-"
                    word2="+"
                else:
                    word1="="
                    word2="="
                    
                
                    
                ##如果第一個符號為大，則對應到第二個為小，如果第一個符號為小，則對應到第二個為大
                if keys4[i][0]=="大" or keys4[i][0]=="小":

                    if "數量" not in keys3[i]:

                        item1.insert(0,keys5[i][0])   ##> < 名稱
                        item2.insert(0,keys4[i][0])   ##> or < 
                    
                    if keys4[i][0]=="大":
                        word1="大"
                        word2="小"
                    else:
                        word1="小"
                        word2="大"
                
                

                if len(keys1[i])==2:
                    name1 = keys1[i][0]  ##主事者
                    name2 = keys1[i][1]  ##接受者

                cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")   ##先畫出基底的圓
                cv.create_text(mid_x,mid_y,text=name1,font=("標楷體",10))   ##標註主事者
                left_x = mid_x+oval_w/2
                
                print("主事者:",name1,"，對應到運算符號:",word1)
                print("接受者:",name2,"，對應到運算符號:",word2)
                

                count=0
                right_x=right_x+120
                mid_x = right_x-30

                item1 = keys2[i]       ##物品 數量  單位  (名稱)
                item2 = keys3[i]       ##物品 數量  單位  (標籤)


                cv.create_line(left_x,init_y,mid_x,init_y-100,mid_x,mid_y+oval_h/2+60,smooth="true")
                cv.create_text(mid_x-20,mid_y+oval_h/2+40,text=word1,font=("標楷體",10))     ##標註+-=...

                
                cv.create_oval(right_x-oval_w/2,right_y-oval_h/2,right_x+oval_w/2,right_y+oval_h/2,fill="white") ##先畫出基底的圓
                name2 = keys1[i][1]
                cv.create_text(right_x,right_y,text=name2,font=("標楷體",10))  ##標註接受者
                cv.create_line(right_x,right_y+oval_h/2,mid_x,mid_y+oval_h/2+60)
                cv.create_text(mid_x+20,mid_y+oval_h/2+40,text=word2,font=("標楷體",10))  ##標註+-=..
                

                


                if name1 in item1:  ##如果主事者或接受者有在物品 數量  單位出現，則要拿掉
                    item2.remove(item2[item1.index(name1)])
                    item1.remove(name1)
                    

                if name2 in item1:  ##如果主事者或接受者有在物品 數量  單位出現，則要拿掉
                    item2.remove(item2[item1.index(name2)])
                    item1.remove(name2)
                    
                

                
                mid_y += oval_h/2+60 
                
                print("y座標往下推，畫出物品數量單位特點時間點發生地等")

                ##往下畫圖(物品數量單位...)

                for j in range(len(item1)):
                    
                    if count==0:
                        
                        cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                        cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                        count+=1
                        

                    else:
                        cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                        cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[j],font=("標楷體",10))
                        mid_y+=60
                        cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                        cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                    print((item1[j]),"，座標:",str(mid_x),str(mid_y))
                    
                mid_x +=150
                right_x=mid_x

                if max_width<=right_x:

                    max_width=right_x+100
                    

                if max_height<=mid_y:
                    max_height=mid_y+150

                cv.configure(width=max_width,height=max_height)   #canvas重新調整大小
                
                mid_y = init_y+oval_h/2+60
        
            
        
        if max_width<=right_x:

            max_width=right_x+100
                    

        if max_height<=mid_y:
            max_height=mid_y+150


            
        cv.configure(width=max_width,height=max_height)   #canvas重新調整大小

        print()
