##畫出問題語意網路

##使用的function: draw(cv,sheet) => 整理excel的資料，把圖畫出來

##流程 :

##import p3_read，把excel的sheet，傳到p3_read.read這個function中，去處理excel的資訊

##p3_read.read 大致用途 : 把[主事者、接受者]、[物品、數量、單位、特點、時間點、發生地]、[+-=大小前後]等，進行分類，輸出5個list

## 讀取完畢後，根據前面return 出來的各個list開始畫圖。

##和p3_show2不同處: 會記錄每句話的詞和標籤座標，並且判斷是否能連結。

##會存
## 1. coor_name : 主事者接受者的名稱與座標
## 2. coor_plus : 運算符號(+-=大小)
## 3.


from tkinter import *
from random import randint
import pyautogui
from openpyxl import load_workbook
from . import p3_read

oval_w = 60 #橢圓的寬
oval_h = 30   #橢圓的高


def draw(cv,sheet):
    
     ##主事者與接受者座標
    print()
    print("問題語意網路")
    print()
    
    mid_x = 100
    mid_y = 50
    init_x = mid_x
    init_y = mid_y
    left_x = mid_x
    left_y = mid_y
    right_x = mid_x
    right_y = mid_y
    addx = 50
    addy = 80
    max_width = 0
    max_height = 50
    ##主事者與接受者座標

    keys1 = []  ##主事者或接受者名稱

    keys2 = []  ##物品 數量  單位  (名稱)
        
    keys3 = []  ##物品 數量  單位   (標籤)

    keys4 = []   ##+-=

    keys5 = []   ##+-=名稱

    name = ""  ##主事者接受者名稱(只有一人時)
    name1=""    ##主事者接受者名稱(兩人時)
    name2=""    ##主事者接受者名稱(兩人時)

    
    
    times = 0

    coor_name = []   ##紀錄人物標籤名稱與座標

    coor_item = []   ##紀錄物品數量單位標籤名稱與座標

    coor_plus = []  ##紀錄+-=...名稱與座標

    coor_x = 0
    coor_y = 0

    word1=word2=""  ##紀錄這句話的運算符號(+-=...)

    

    keys1,keys2,keys3,keys4,keys5,is_plus,is_remain,is_do,is_total,change_plus,plus_one,add_back,no_have = p3_read.read(keys1,keys2,keys3,keys4,keys5,sheet,"img")
    
    print("讀取excel，做處理")
    
    print("keys1",keys1)
    print("keys2",keys2)
    print("keys3",keys3)
    print("keys4",keys4)
    print()
    
    ##把excel的資料進行分類，return 出list和變數
    

    ##例子 : 小明有3顆蘋果，媽媽給他2顆。小明有幾顆蘋果?

    #keys1 : [['小明'], ['媽媽', '小明']]
    #keys2 : [['蘋果', 3, '顆'], ['蘋果', 2, '顆']]
    #keys3 : [['物品', '數量', '單位'], ['物品', '數量', '單位']]
    #keys4 : [['='], ['-']]
    #keys5 : [['有'], ['給']]
    

    for i in range(len(keys1)):  ##根據句數以及主事者接受者數量進行繪圖

        

        count = 0

        item1 = keys2[i]       ##物品 數量  單位  (名稱)
        item2 = keys3[i]       ##物品 數量  單位  (標籤)

        print("第",str(i+1),"句話")

        if len(coor_name)==0:   ##如果list中還沒有存座標(第一句話)，則要完整畫出所有東西

            
            print("尚未存任何座標")
            
            if len(keys1[i])==1 or (len(keys1[i])==0 and keys3[i].count("物品")==1):   ##如果主事者接受者數量為1
                
                

                cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")   ##圓形(x1, y1, x2, y2)
                
                if len(keys1[i])==1:
                    name = keys1[i][0]  ##主事者為人
                #else:
                    #name = keys2[i][0]  ##主事者為物品，則主事者為物品
                    #keys1[i].append(name)
                cv.create_text(mid_x,mid_y,text=name,font=("標楷體",10))   ##先畫出基底的圓

                coor_name.append([name,[mid_x+oval_w/2,mid_y]])   ##存下主事者名稱跟座標
                
                print("畫出主事者:",name,"，","座標:",str(mid_x),str(mid_y))

                cv.create_line(init_x,init_y+oval_h/2,init_x,init_y+oval_h/2+60)
                cv.create_text((init_x+mid_x)/2-10,((init_y+oval_h/2)*2+60)/2,text=str(keys4[i][0]),font=("標楷體",10))  ##+-=
                mid_y = init_y+oval_h/2+60
                coor_plus.append(keys4[i][0])   ##存下+-=
                print("畫出運算符號:",keys4[i][0],"，","座標:",str(mid_x),str(mid_y))

                print("y座標往下推，畫出物品數量單位特點時間點發生地等")

                for j in range(len(item1)):       ##把物品 數量  單位  特點 時間點 發生地等畫出來
                    
                    if count==0:
                        if item1[j]!=name:
                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                            cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                            coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])   ##存下物品 數量  單位  特點 時間點 發生地，以及對應座標
                            count+=1
                    else:
                        if item1[j]!=name:
                            cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                            cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[j],font=("標楷體",10))
                            
                            mid_y+=60
                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                            cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                            coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])   ##存下物品 數量  單位跟座標
                    
                    print(item1[j],"，座標 : ",str(mid_x+oval_w/2),str(mid_y))
                    
                    if max_width<= mid_x:
                        max_width = mid_x+50

                    if max_height<=mid_y:
                        max_height=mid_y+100

                        

                    
                mid_x +=150
                right_x=mid_x
                mid_y = init_y+oval_h/2+60

            else: #主事者接受者數量為2

                
                

                if len(keys1[i])==2 or (len(keys1[i])==0 and keys3[i].count("物品")==2):   ##如果主事者接受者有兩個

                    print("主事者接受者數量為2")

                    
                    cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")   ##圓形(x1, y1, x2, y2)
                    if len(keys1[i])==2:
                        name1 = keys1[i][0]  ##主事者為人
                        name2 = keys1[i][1]
                    
                    print("名單:",name1,",",name2)
                        
                    # else:  ##用不到
                    #     name1 = keys2[i][0]  ##主事者為物品
                    #     name2 = keys2[i][1]
                    #     keys1[i].append(name1)
                    #     keys1[i].append(name2)
                        
                    
                        
                    cv.create_text(mid_x,mid_y,text=name1,font=("標楷體",10))   ##主事者
                    coor_name.append([name1,[mid_x+oval_w/2,mid_y]])   ##存下主事者名稱跟座標
                    print("主事者:",name1,"，座標 : ",str(mid_x+oval_w/2),str(mid_y))

                    count=0
                    right_x=right_x+120
                    mid_x = right_x-30

                    item1 = keys2[i]       ##物品 數量  單位  (名稱)
                    item2 = keys3[i]       ##物品 數量  單位  (標籤)

                    ##先畫主事者與接受者的部分
                    cv.create_oval(right_x-oval_w/2,right_y-oval_h/2,right_x+oval_w/2,right_y+oval_h/2,fill="white")
                    name2 = keys1[i][1]
                    cv.create_text(right_x,right_y,text=name2,font=("標楷體",10))
                    coor_name.append([name2,[right_x+oval_w/2,right_y]])   ##存下主事者名稱跟座標
                    
                    print("接受者:",name2,"，座標 : ",str(right_x+oval_w/2),str(right_y))
                    
                    if keys4[i][0]=="+":
                        word1="+"
                        word2="-"
                    elif keys4[i][0]=="-":
                        word1="-"
                        word2="+"
                    else:
                        word1="="
                        word2="="
                    
                    
                    if keys4[i][0]=="大" or keys4[i][0]=="小":

                        

                        if "數量" not in item2:

                            item1.insert(0,keys5[i][0])   ##> < 名稱
                            item2.insert(0,keys4[i][0])   ##> or < 
                        
                        if keys4[i][0]=="大":
                            word1="大"
                            word2="小"
                        else:
                            word1="小"
                            word2="大"
                    
                        
                    cv.create_line(init_x,init_y-oval_h/2,mid_x,init_y-100,mid_x,mid_y+oval_h/2+60,smooth="true")
                    cv.create_text(mid_x-20,mid_y+oval_h/2+40,text=word1,font=("標楷體",10))     
                    cv.create_line(right_x,right_y+oval_h/2,mid_x,mid_y+oval_h/2+60)
                    cv.create_text(mid_x+20,mid_y+oval_h/2+40,text=word2,font=("標楷體",10))
                    
                    print("主事者對應到的運算符號:",word1,"，座標 : ",str(mid_x-20),str(mid_y+oval_h/2+40))
                    print("接受者對應到的運算符號:",word2,"，座標 : ",str(mid_x+20),str(mid_y+oval_h/2+40))

                    coor_plus.append(word1)
                    coor_plus.append(word2)


                    if name1 in item1:
                        item2.remove(item2[item1.index(name1)])
                        item1.remove(name1)
                        

                    if name2 in item1:
                        item2.remove(item2[item1.index(name2)])
                        item1.remove(name2)
                        
                    

                    
                    mid_y += oval_h/2+60 

                    ##往下畫圖(物品數量單位...)
                    
                    print("y座標往下推，畫出物品數量單位特點時間點發生地等")

                    for j in range(len(item1)):
                        
                        if count==0:
                            
                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                            cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                            count+=1
                            coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]]) 

                        else:
                            cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                            cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[j],font=("標楷體",10))
                            
                            coor_plus.append(item2[j])
                            
                            mid_y+=60
                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                            
                            cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                            coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])
                            
                        print(item1[j],"，座標 : ",str(mid_x+oval_w/2),str(mid_y))
                        
                    mid_x +=150
                    right_x=mid_x

                    if max_width<=right_x:

                        max_width=right_x+100
                        

                    if max_height<=mid_y:
                        max_height=mid_y+150

                    cv.configure(width=max_width,height=max_height)   #canvas重新調整大小
                    
                    mid_y = init_y+oval_h/2+60


            
            print()


        else: ##接下來要從已經儲存的list中進行比對

            
            
            if len(keys1[i])==1 :  ##如果主事者接受者數量為1
            
                print("主事者接受者數量為1")
                
                name = keys1[i][0] ##主事者
                
                    


                ##進行比對

                for j in range(len(coor_name)):
                    coor_x = 0
                    coor_y = 0

                    if coor_name[j][0] == name:   ##如果有找到相同名稱的
                        
                        print("連結:",name,"，主事者接受者數量為1，不須再畫主事者")
                        
                        coor = coor_name[j][1]

                        coor_x = coor[0]-oval_w/2
                        coor_y = coor[1]+oval_h/2


                        #cv.create_line(coor_x,coor_y,mid_x,init_y+oval_h/2+60)
                        cv.create_line(coor_x+oval_w/2,coor_y-oval_h/2,mid_x,init_y-100,mid_x,init_y+oval_h/2+60,smooth="true")
                        cv.create_text(mid_x-30,init_y+oval_h/2+40,text=str(keys4[i][0]),font=("標楷體",10))
                        
                        print("運算符號:",keys4[i][0],"，座標 : ",str(mid_x-30),str(init_y+oval_h/2+40))
                        
                        coor_plus.append(str(keys4[i][0]))
                        
                        mid_y = init_y+oval_h/2+60
                        
                        print("y座標往下推，畫出物品數量單位特點時間點發生地等")

                        for k in range(len(item1)):       ##把物品數量單位特點時間點發生地畫出來
                    
                            if count==0:
                                if item1[k]!=name:
                                    cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                                    cv.create_text(mid_x,mid_y,text=item1[k],font=("標楷體",10))
                                    coor_item.append([item1[k],[mid_x+oval_w/2,mid_y]])
                                    count+=1
                            else:
                                if item1[k]!=name:
                                    cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                                    cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[k],font=("標楷體",10))
                                    
                                    mid_y+=60
                                    cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                                    cv.create_text(mid_x,mid_y,text=item1[k],font=("標楷體",10))
                                    coor_item.append([item1[k],[mid_x+oval_w/2,mid_y]])

                            print(item1[k],"，座標 : ",str(mid_x+oval_w/2),str(mid_y))

                        mid_x +=150
                        right_x=mid_x

                        if max_width<=right_x:

                            max_width=right_x+100
                        

                        if max_height<=mid_y:
                            max_height=mid_y+150

                        cv.configure(width=max_width,height=max_height)   #canvas重新調整大小
                        
                        mid_y = init_y+oval_h/2+60
                        
                        break


                if coor_x==coor_y==0:   ##如果沒有從主事者的list中找出，就從物品數量單位list中找
                    
                    print("沒有從主事者接受者的list中取得連結，往下找")
                        
                    
                    count=0
                    right_x=right_x+120
                    mid_x = right_x-30
                    mid_y = init_y+oval_h/2+60

                    item1 = keys2[i]       ##物品數量單位特點時間點發生地  (名稱)
                    item2 = keys3[i]       ##物品數量單位特點時間點發生地  (標籤)

                    print(item1,item2)

                    if len(keys1[i])==1 or (len(keys1[i])==0 and keys3[i].count("物品")==1):
                        
                        cv.create_oval(mid_x-oval_w/2,right_y-oval_h/2,mid_x+oval_w/2,right_y+oval_h/2,fill="white")
                        
                        if len(keys1[i])==1:
                            name = keys1[i][0]
                        else:
                            name = keys2[i][0]
                        cv.create_text(mid_x,right_y,text=name,font=("標楷體",10))
                        coor_name.append([name,[mid_x+oval_w/2,right_y]])
                        
                        print("畫出主事者:",name,"，座標 : ",str(mid_x+oval_w/2),str(right_y))
                            
                        ##如果是物品相連

                        for j in (coor_item):   ##從物品數量單位list中找出匹配的

                            

                            if j[0]==item1[0] and item2[0]=="物品":   ##如果是物品相連

                                print("物品連結: ",item1[0])
                                

                                coor_x = j[1][0]
                                coor_y = j[1][1]

                                cv.create_line(coor_x,coor_y,mid_x,right_y+oval_h/2)
                                cv.create_text((mid_x+coor_x)/2-10,(coor_y+right_y+oval_h/2)/2,text=keys4[i],font=("標楷體",10))
                                
                                print("畫出運算符號:",name,"，座標 : ",str((mid_x+coor_x)/2-10),str((coor_y+right_y+oval_h/2)/2))
                                
                                mid_y+=60
                                coor_plus.append(keys4[i])

                                for k in range(len(item1)):

                                    if item2[k]!="物品":

                                        if count==0:
                                            
                                            cv.create_line(coor_x,coor_y,mid_x,mid_y-oval_h/2)
                                            cv.create_text((mid_x+coor_x)/2-10,(coor_y+mid_y-oval_h/2)/2,text=item2[k],font=("標楷體",10))
                                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                                            cv.create_text(mid_x,mid_y,text=item1[k],font=("標楷體",10))
                                            coor_item.append([item1[k],[mid_x+oval_w/2,mid_y]])
                                            #mid_y+=60
                                            count+=1
                                            
                                        else:
                                            cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                                            cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[k],font=("標楷體",10))
                                            mid_y+=60
                                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                                            cv.create_text(mid_x,mid_y,text=item1[k],font=("標楷體",10))
                                            coor_item.append([item1[k],[mid_x+oval_w/2,mid_y]])

                                        print(item1[k],"，座標 : ",str(mid_x+oval_w/2),str(mid_y))

                                mid_x +=150
                                right_x=mid_x

                                if max_width<=right_x:

                                    max_width=right_x+100
                                

                                if max_height<=mid_y:
                                    max_height=mid_y+150

                                cv.configure(width=max_width,height=max_height)   #canvas重新調整大小

                                
                                break
                                        
                                            
                        for j in coor_item:
                            if count!=0:
                                break
                           
                            
                            elif count==0 and j[0]==item1[len(item1)-1]:     ##如果單位相連

                                
                                print("單位連結:",j[0])

                                coor_x = j[1][0]
                                coor_y = j[1][1]

                                cv.create_line(mid_x,init_y+oval_h/2,mid_x,init_y+oval_h/2+60)
                                cv.create_text(mid_x-10,((init_y+oval_h/2)*2+60)/2,text=str(keys4[i][0]),font=("標楷體",10))  ##+-=
                                
                                print("畫出運算符號:",keys4[i][0],"，座標 : ",str(mid_x-10),str(((init_y+oval_h/2)*2+60)/2))
                                
                                for k in range(len(item1)):

                                    if count==0:
                                        if name!=item1[k]: 
                                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                                            cv.create_text(mid_x,mid_y,text=item1[k],font=("標楷體",10))
                                            coor_item.append([item1[k],[mid_x+oval_w/2,mid_y]])
                                            count+=1
                                                
                                    else:
                                        if item1[k]!= j[0]:
                                            
                                            if name!=item1[k]:
                                                
                                                cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                                                cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[k],font=("標楷體",10))
                                                mid_y+=60
                                                cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                                                cv.create_text(mid_x,mid_y,text=item1[k],font=("標楷體",10))
                                                coor_item.append([item1[k],[mid_x+oval_w/2,mid_y]])
                                        else:
                                            if name!=item1[k]: 
                                                cv.create_line(coor_x,coor_y,mid_x,mid_y+oval_h/2)
                                                cv.create_text((coor_x+mid_x)/2-10,(2*mid_y+60)/2,text=item2[k],font=("標楷體",10))
                                    print(item1[k],"，座標 : ",str(mid_x+oval_w/2),str(mid_y))

                                mid_x +=150
                                right_x=mid_x

                                if max_width<=right_x:

                                    max_width=right_x+100
                                

                                if max_height<=mid_y:
                                    max_height=mid_y+150

                                cv.configure(width=max_width,height=max_height)   #canvas重新調整大小
                                
                                break
                                    

                        
            
                              
            elif len(keys1[i])==2 or (len(keys1[i])==0 and keys3[i].count("物品")==2):   ##如果主事者接受者數量為2
               
                print("主事者接受者數量為2")
            
                mid_y = 50
                item1 = keys2[i]       ##物品 數量  單位  (名稱)
                item2 = keys3[i]       ##物品 數量  單位  (標籤)

                if len(keys1[i])==2:
                    name1 = keys1[i][0]
                    name2 = keys1[i][1]
                else:
                    name1 = keys2[i][0]
                    name2 = keys2[i][1]
                
                
                print("名單 : ",name1,"，name2")
                
                print("往下判斷是否有連結")
                
                connect = False  ##判斷是否有連結
                
                for j in coor_name:   ##從暫存主事者接受者找出有聯結的關鍵字和座標
                    
                    if name1==j[0]:
                        
                        connect = True
                        name = name2
                        coor_x = j[1][0]
                        coor_y = j[1][1]
                        print("連結:",name1)
                        

                        if keys4[i][0] == "+":
                            word1 = "+"
                            word2 = "-"
                        elif  keys4[i][0] == "-":
                            word1 = "-"
                            word2 = "+"
                        else:
                            word1 = "="
                            word2 = "="

                        if keys4[i][0] == "大" or keys4[i][0] == "小":
                            if "數量" not in item2:

                                item1.insert(0,keys5[i][0])   ##> < 名稱
                                item2.insert(0,keys4[i][0])   ##> or < 
                            if keys4[i][0] == "大":
                                word1 = "大"
                                word2 = "小"
                            else:
                                word1 = "小"
                                word2 = "大" 
                        print("運算符號",word1,"，",word2)
                        
                        
                        break
                    
                    elif name2==j[0]:
                        connect = True
                        name = name1
                        coor_x = j[1][0]
                        coor_y = j[1][1]
                        print("連結:",name2)

                        if keys4[i][0] == "+":
                               
                            word1 = "-"
                            word2 = "+"
                        elif keys4[i][0] == "-":
                            word1 = "+"
                            word2 = "-"
                        else:
                            word1 = "="
                            word2 = "="

                        if keys4[i][0] == "大" or keys4[i][0] == "小":

                            if "數量" not in item2:

                                item1.insert(0,keys5[i][0])   ##> < 名稱
                                item2.insert(0,keys4[i][0])   ##> or < 
                            
                            

                            if keys4[i][0] == "大":
                               
                                word1 = "小"
                                word2 = "大"
                            else:
                                word1 = "大"
                                word2 = "小"
                        print("運算符號",word1,"，",word2)
                        
                        
                        break


                if  connect == False:  ##如果從暫存主事者接受者沒有找出有聯結的關鍵字和座標
                    print("主事者接受者沒有連結，往下找")
                    for j in coor_item:   ##從暫存物品數量單位等找出有聯結的關鍵字和座標
                        
                        
                        if name1==j[0]:
                            
                            connect = True
                            name = name2
                            coor_x = j[1][0]
                            coor_y = j[1][1]
                            print("連結:",name1)
                           # 

                            if keys4[i][0] == "+":
                                word1 = "+"
                                word2 = "-"
                            elif keys4[i][0] == "-":
                                word1 = "-"
                                word2 = "+"
                            else:
                                word1 = "="
                                word2 = "="

                            if keys4[i][0] == "大" or keys4[i][0] == "小":
                                if "數量" not in item2:

                                    item1.insert(0,keys5[i][0])   ##> < 名稱
                                    item2.insert(0,keys4[i][0])   ##> or < 
                                if keys4[i][0] == "大":
                                    word1 = "大"
                                    word2 = "小"
                                else:
                                    word1 = "小"
                                    word2 = "大" 
                            print("運算符號",word1,"，",word2)
                            
                            
                            break
                        
                        elif name2==j[0]:
                            connect = True
                            name = name1
                            coor_x = j[1][0]
                            coor_y = j[1][1]
                            print("連結:",name2)

                            if keys4[i][0] == "+":
                                   
                                word1 = "-"
                                word2 = "+"
                            elif keys4[i][0] == "-":
                                word1 = "+"
                                word2 = "-"
                            else:
                                word1 = "="
                                word2 = "="

                            if keys4[i][0] == "大" or keys4[i][0] == "小":

                                if "數量" not in item2:

                                    item1.insert(0,keys5[i][0])   ##> < 名稱
                                    item2.insert(0,keys4[i][0])   ##> or < 
                                
                                

                                if keys4[i][0] == "大":
                                   
                                    word1 = "小"
                                    word2 = "大"
                                else:
                                    word1 = "大"
                                    word2 = "小"
                            print("運算符號",word1,"，",word2)
                            
                            
                            break
                        



                
                mid_x = right_x-30

                
                
                cv.create_oval(right_x-oval_w/2,right_y-oval_h/2,right_x+oval_w/2,right_y+oval_h/2,fill="white")
                cv.create_text(right_x,right_y,text=name,font=("標楷體",10))   ##畫出主事者
                coor_name.append([name,[right_x+oval_w/2,right_y]])
                
                print("畫出主事者:",name,"，座標 : ",str(right_x+oval_w/2),str(right_y))
                
                cv.create_line(coor_x,coor_y,mid_x,init_y-100,mid_x,mid_y+oval_h/2+60,smooth="true")
                cv.create_text(mid_x-20,mid_y+oval_h/2+40,text=word1,font=("標楷體",10))   ##標記+-=
                
                print("畫出運算符號:",word1,"，座標 : ",str(mid_x-20),str(mid_y+oval_h/2+40))
                    
                cv.create_line(right_x,right_y+oval_h/2,mid_x,mid_y+oval_h/2+60)
                cv.create_text(mid_x+20,mid_y+oval_h/2+40,text=word2,font=("標楷體",10))  ##標記+-=
                
                print("畫出運算符號:",word2,"，座標 : ",str(mid_x+20),str(mid_y+oval_h/2+40))

                mid_y += oval_h/2+60

                
                
                for j in range(len(item1)):  ##物品數量單位特點時間點發生地
                    
                    if count==0: ##如果為0，則不須標註標籤，只需##先畫出圓、標註詞
                        if name1 not in item1 and name2 not in item1:
                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                            cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                            coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])
                            count+=1
                        elif connect==True:
                            names = [name1,name2]
                            if item1[j] not in names:  ##如果這個詞不為主事者接受者才畫
                                cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                                cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                                coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])
                                count+=1
                                

                    else:  ##如果不為0，則須標註標籤，接者畫出圓、標註詞
                        if name1 not in item1 and name2 not in item1:
                            cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                            cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[j],font=("標楷體",10))
                            mid_y+=60
                            cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                            cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                            coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])

                        elif connect==True:
                            names = [name1,name2]
                            if item1[j] not in names:  ##如果這個詞不為主事者接受者才畫
                                cv.create_line(mid_x,mid_y+oval_h/2,mid_x,mid_y+60)
                                cv.create_text(mid_x-10,(2*mid_y+60)/2,text=item2[j],font=("標楷體",10))
                                mid_y+=60
                                cv.create_oval(mid_x-oval_w/2,mid_y-oval_h/2,mid_x+oval_w/2,mid_y+oval_h/2,fill="white")
                                cv.create_text(mid_x,mid_y,text=item1[j],font=("標楷體",10))
                                coor_item.append([item1[j],[mid_x+oval_w/2,mid_y]])
                    
                    print(item1[j],"，座標 : ",str(mid_x+oval_w/2),str(mid_y))
                                
                
                mid_x +=150
                right_x=mid_x

                if max_width<=right_x:

                    max_width=right_x+100
                                

                if max_height<=mid_y:
                    max_height=mid_y+150

                cv.configure(width=max_width,height=max_height)   #canvas重新調整大小
                      


        
##            print(coor_name)
##            print(coor_item)
##            print(coor_plus)




           
                
            if max_width<=right_x:

                max_width=right_x+100
                

            if max_height<=mid_y:
                max_height=mid_y+150  

   
    

        
    cv.configure(width=max_width,height=max_height)   #canvas重新調整大小
