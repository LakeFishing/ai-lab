##把資料結構讀入，並建立dictionary

##line : word.txt (原本句子的資料結構)
##line2 : question.txt (問題的詞和標籤)

## create_table(line,line2) : 處理資料結構，並建立d1、d2


## d1 : 
## a0 => ['小明', ['none'], ['a1', 'b1']]
## a1 => ['=', ['a0'], ['a2']]
## b1 => ['-', ['a0'], ['b2']]
## a2 => ['蘋果', ['a1'], ['a3']]
## a3 => ['5', ['a2'], ['a4']]
## a4 => ['顆', ['a3'], ['none']]
## b2 => ['蘋果', ['b1'], ['b3']]
## b3 => ['3', ['b2'], ['b4']]
## b4 => ['顆', ['b3'], ['none']]

## d2 :
## 小明 =>     [[‘a4’, ‘b4’], [‘=’, ‘-’], [‘a0’], [5, 3]]
## =        =>     [[‘a4’], [‘none’], [‘a1’], [‘none’]]
## -         =>     [[‘b4’], [‘none’], [‘b1’], [‘none’]]
## 蘋果  =>    [[‘a4’, ‘b4’], [‘none’], [‘a2’, ‘b2’], [‘none’]]
## 5        =>    [[‘a4’], [‘none’], [‘a3’], [‘none’]]
## 顆      =>    [['none', 'none'], ['none'], ['a4', 'b4'], ['none']]
## 3        =>    [['b4'], ['none'], ['b3'], ['none']]






def create_table(line,line2):##建立資料結構與字典


    

    init_list = []  ##語意網路需要使用的list，包含1.名稱，2.位置，3.前一個或多個元素位置，4.後一個或多個元素位置

    temp_list=[]  ##暫存list(讀取用)

    ##讀取問題標籤
    q1 = line2[0].split()   ##問題標籤(名稱)
    q2 = line2[1].split()   ##問題標籤(種類)
    ##讀取問題標籤
    
    if q2==[]:
        for i in range(100):        
            try:
                q2 = line2[i+1].split()
                if q2!=[]:
                    break
            except:
                print("讀取失敗")
        
    
    add = 0  ##沒用到
    sum_ = 0  ##沒用到

    d1 = {} ##建立字典，作為索引用，例如:輸入"a1"，可以取得a1這個位置的名稱，以及前面元素位置及後面元素位置
    d2 = {} ##建立另一個字典，輸入名稱，找出名稱在那些句子存在
    d3 = {} ##輸入第幾句，取得裡面的文字(不太會用到)

    index = [] ##建立索引list，存放存在的位置 ex:a0,a1,a2...
    names = [] ##存入詞彙與屬性(名稱.第幾句.+-=.位置.底層位置.數字)，供之後建立table用

    #clause = [["a",[],[]],["b",[],[]],["c",[],[]],["d",[],[]],["e",[],[]],["f",[],[]],["g",[],[]]] ##將文字跟數字區隔

    
    count_people = 0

    
    ###把原本p3_output的資料結構讀進來#####################################################

    for i in range(0,len(line),4):   ##讀取語句標籤

        temp_list=[]   ##暫存屬性，供之後儲存到init_list用

        name = line[i].replace("\n","")  ##暫存詞的名稱
        
        addr = line[i+1].replace("\n","") ##暫存標籤位置
        
        pre = line[i+2].split()  ##暫存這個標籤的前一個或多個位置

        if len(pre)==0:
            pre.append("none")
        
        nex = line[i+3].split()  ##暫存這個標籤的後一個或多個位置
        if len(nex)==0:
            nex.append("none")

        temp_list.append(name)
        temp_list.append(addr)
        temp_list.append(pre)
        temp_list.append(nex)
        
        init_list.append(temp_list)   ##把暫存的list存到之後處理會用到的list中




    
    ###################建立字典d1，index存入位置，存入詞彙名稱#################################
        
    for i in init_list:  

        is_same = 0  ##判斷是否有重疊
        x = [i[0],i[2],i[3]]  ##暫存名稱，前面元素位置，後面元素位置
        d1[i[1]]=x   ##指定字典d1的索引值。i[1]為標籤的位置
        index.append(i[1])  ##存入位置

        
        for j in names:
            
            if i[0]==j[0]:  ##如果names中的元素跟init_list中的元素有重疊，則is_same=1
                is_same=1

        if is_same==0:  
            names.append([i[0],[],[],[],[],[]])   ##如果is_same=0，則代表names要加入[i[0],[],[],[],[],[]]

    
    

    index.sort()  ##將索引list排序(由a到g)


################################################處理d2(先用names做處理，之後指定到d2)####################################################

    
    for i in init_list:   ##這裡將init_list跟names做比較(init_list中，元素會有重複，而names不會重複)
        
        for j in names:   ##names : 1.名稱，2.位置，3.前一個或多個元素位置，4.後一個或多個元素位置

            

            next_pos = ""  ##下一個位置
            current = ""

            if i[0]==j[0]:  ##如果名稱(詞彙)相同，進行下一步處理

                
                    
                j[3].append(i[1])   ##names的元素目前位置放入init_list的元素目前位置
                
                if i[2][0]=="none":  ##如果是主事者接受者(前一個元素為none)



################################################處理主事者的運算符號(+-=...)####################################################

                    
                    for x in range(len(i[3])):

                        
                       
                        pos = i[3][x]  ##第幾個後面元素

                        

                        check_ = False  ##判斷是否有數字
                        
                        if pos in i[3]:   

                            
                            
                            
                            j[2].append(d1[pos][0])   ##存放+-=(主事者的下一個位置+-=)
                            
                            temp_plus = d1[pos][0] ##暫存+-=

                            usd_tmp = False  ##是否使用過temp_plus

                            next_pos = pos  ##重新指定next_pos

                            current=next_pos  ##重新指定current

################################################處理主事者所對應到的數字####################################################                            
                            
                            while next_pos!="none":  ##如果next_pos不為空，則試著找出有沒有數字，以供之後解題計算用

                                

                                if next_pos in d1:
                                    if count_people<=len(d1[next_pos][2])-1:
                                        next_pos = d1[next_pos][2][count_people]
                                        if next_pos!="none":
                                            current=next_pos
                                    else:
                                        next_pos = d1[next_pos][2][0]
                                        if next_pos!="none":
                                            current=next_pos
                                

                                try:  ##try:如果這個元素處以1的餘數為0，則代表這個是數字，可以存入j[5]
                                    if int(d1[next_pos][0])%1==0:

                                        
                                        
                                        j[5].append(int(d1[next_pos][0]))    ##存數字
                                        check_ = True  ##表示有數字
                                        
                                        j[4].append(d1[next_pos][2][0])  ##存單位位置

                                        if usd_tmp == True:
                                            j[2].append(temp_plus)   ##存放+-=(主事者的下一個位置+-=)
                                        usd_tmp = True
                                        
                                        
                                except:
                                    current=current   ##如果無法，則目前位置照舊
                                    

                            if check_==False:    ##如果無數字，則數字那邊存入0
                                j[5].append(0)
                                j[4].append(current)    ##存入最底層位置
                            

                             
                                
                    count_people+=1       ##人數+1 
                    
 
                      
                else:  ##如果不是主事者接受者
                    s = i[1]  ##位置(a1,a2...)
                    j[1].append(s[0])   ##存入第幾句(不太會用到)

                    

                    for x in range(len(d1[s][2])):   ##這個位置的下一個位置(可能不只一個)
                       

                        next_pos = d1[s][2][x]  ##指定下一個位置

                        
                        current = next_pos  ##指定目前位置
                        
                        
                        while next_pos!="none":

                            if next_pos in d1:
                                next_pos = d1[next_pos][2][0]
                                if next_pos!="none":
                                        current = next_pos  
                        
                        j[4].append(current)  ##指定下一個位置



##指定字典d2的值(1.顯示最底層的詞彙(如果自己就是最底層則是none)，2.顯示+-=(如果為主事者接受者)，3.顯示這個詞存在的位置，4.數字)###

    for i in names:
        
        if len(i[2])==0:  ##如果+-=為空，則填入none
            i[2].append("none")
        if len(i[5])==0:  ##如果數字為空，則填入none
            i[5].append("none")
        
        d2[i[0]]=[i[4],i[2],i[3],i[5]]   


            

##    for i in names:   ##比較沒有用到
##
##        clau = i[1]
##        
##        for j in clau:
##
##            for k in clause:
##
##                if j==k[0]:  ##如果句子一樣
##
##                    try:
##                        if int(i[0])%1==0:
##                            k[2].append(i[0])  ##clause加入這個數字
##                    except:
##                        k[1].append(i[0])  ##clause加入這個詞

    

    #for i in clause:   ##d3比較沒有用到

        #d3[i[0]]=[i[1],i[2]]   #將d3中的詞彙跟數量分開 ex: 第a句，[['我', '=', '蘋果', '個'], ['10']]
        

    
    d2 = check_plus_num(d2)
    

    for i in d1:
        print(i,"=>",d1[i])


    return init_list,q1,q2,d1,d2,d3



def check_bottom(d1,d2):  ##判斷底層是否正確(目前沒用到)

    for i in d2:  

        item = d2[i]

        it_bottom = item[0]  ##底層
        it_pos = item[2]

        it_plus = item[1]
        it_num = item[3]


        d2[i] = [it_bottom,it_plus,it_pos,it_num]

        return  d2
    
    
def check_plus_num(d2):  ##判斷運算符號(+-=)數量是否跟數字數量一致，如果沒有，則要補到一致，使用暫存的運算符號

    

    for i in d2:  

        item = d2[i]

        it_bottom = item[0]
        it_pos = item[2]

        it_plus = item[1]
        it_num = item[3]

        if len(it_plus)<len(it_num) and len(it_plus)>0:  

            temp_plus = it_plus[0]

            times = len(it_num)-len(it_plus)

            

            for j in range(times):
                
                it_plus.append(temp_plus)

                
        

        d2[i] = [it_bottom,it_plus,it_pos,it_num]

        
        
        return  d2
    
