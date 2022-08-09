import re

final_num = 0
sum_ = 0
total = []
quan = 0
m_num = 0
s_unit = ""


###############################影響計算的參數#####################################################
is_reverse = False  ##是否倒推計算
is_minus = False  ##是否用原本數字下去扣
is_plus = True   ##是否用一般計算，如果為False，且本身是+-，則要往下去找出=的項目做加減
is_differ = False  ##是否用兩個數字相減
is_total = False  ##判斷題目中是否有"一共"這類型詞彙，如果有，做倒推
is_remain = False  ##判斷題目中是否有"剩下"這類型詞彙，如果有，做倒推
change_plus = False   ##判斷題目中是否有"其中"這類型詞彙，如果有，做倒推
add_back = False  ##判斷題目中是否有"不夠"這類型詞彙，如果有，加回去
###############################影響計算的參數#####################################################

##解題時，遇到對應運算符號為"="，存入total(為list)，遇到"+"或"-"，則加到sum_(為int)，最後再合在一起做計算，得到final_num
##我有5顆蘋果，吃掉3顆。 剩下幾顆蘋果?  => 
## total = [5] ; sum_=-3 ，先把total裡面數字加總或全部倒扣(依照影響計算的參數而定)，之後再加上或扣掉sum_(依照影響計算的參數而定)


def attr(is_reverse_,is_minus_,is_plus_,is_differ_,is_total_,is_remain_,change_plus_,quan_,m_num_,s_unit_,add_back_):   ##設定解題時的變數

    global is_reverse,is_minus,is_plus,is_differ,is_total,is_remain,change_plus,quan,m_num,s_unit,add_back

    is_reverse = is_reverse_  ##是否倒推計算
    is_minus = is_minus_  ##是否用原本數字下去扣
    is_plus = is_plus_  ##是否用一般計算，如果為False，且本身是+-，則要往下去找出=的項目做加減
    is_differ = is_differ_   ##是否用兩個數字相減
    is_total = is_total_   ##判斷題目中是否有"一共"這類型詞彙，如果有，做倒推
    is_remain = is_remain_  ##判斷題目中是否有"剩下"這類型詞彙，如果有，做倒推
    change_plus = change_plus_ ##判斷題目中是否有"其中"這類型詞彙，如果有，做倒推
    quan = quan_  #額外計算的數字
    m_num = m_num_  #不會用到
    s_unit = s_unit_  #不會用到
    add_back = add_back_ ##判斷題目中是否有"不夠"這類型詞彙，如果有，加回去

    
    
def question1(people,name,item,unit,d1,d2,d3,quan,s_unit,m_num):     ##如果問題中，包含主事者,物品,單位。題目類型:總和

    print("題型 : 1.問總和(問題中，包含主事者,物品,單位)")
   # print()

    global final_num,sum_,total

    final_num= 0

    if is_plus==False:   ##如果是從比較中去找出數值，要再去找出一個=，做運算

        
        
        final_num = additional(name,item,unit,d1,d2)
            
        return final_num
    
    opr = ""   ##運算符號
    sum_ = 0  ##總和(原始)。當有=時，則指定值給sum_
    add = 0   ##數值(sum)增加的幅度
    total = []  ## 最後輸出的總和

    box = ["+","-","="]  ##+-=
    
    unit_item={"錢":"元"}
    if unit in unit_item:
        
        unit = unit_item[unit]   ##把單位轉換 ex : 錢轉為元




############跑迴圈，找出單位一樣的，找出數字和運算符號##################################

    ##total : 類型為list，存對應到=的數字
    ##sum_ : 整數，對應到+或-，直接先做計算
    
    for i in range(len(people)): #主事者最底層位置(單位)
        
        
        if people[i]in d2[unit][2] and people[i] in d2[item][0]:
            ##如果人最底層的位置跟物品最底層位置一樣，並且單位也一致(在這個句子中)
            
            opr = d2[name][1][i]   ##找出運算符號+-=
            
            
            if len(d2[name][3])!=0:   ##找出數字來做運算
                add = d2[name][3][i]  
                add = int(add)
            if opr =="=":  ##如果運算符號為=，則預設總和為此數字
                total.append(add)
            elif opr =="+":  ##如果運算符號為+，則sum增加
                        
                sum_+=add
                        
            elif  opr =="-":  ##如果運算符號為-，則sum減少
                       
                sum_-=add

    print()
    print(total,sum_)
    #print("初始值:",total)
    #print("增加幅度:",sum_)

    

    

############根據變數去做計算，得到一個final_num##################################  

    

    if is_minus==True and quan!= 0:   ##如果是做減法運算，且問題有提供數字，答案就是用這個數字扣掉已算好的數字
        ##如果問題裡有["就","不夠","就有","還要","就可以","才","找回"] 的關鍵字，且問題有包含數字，則會變成減法運算
        ##ex: 我有15張郵票。再收集幾張郵票就有20張?
                                        
        for i in total:
            final_num+=i
            
        final_num+=sum_
        final_num = quan-total

    elif is_reverse==True:

        ##做倒推運算，變成減法=> 問題裡面有["原本","原來","原先","起初","一開始","剛開始","最早","最初","原有"]的關鍵字
        ## ex : 我有一些糖果，吃了3顆後，剩下10顆。我原本有幾顆糖果?

        for i in total:
            final_num+=i
        
        final_num = final_num-sum_
        
    elif change_plus==True:
        
        ##如果題目中，有'其中'這個關鍵字，表示有一個總體值與幾個物品的值，問某一個的物品的值，則將所有值做減法
        ##ex : 我有10支筆，其中紅筆有2支，藍筆有3支。我有幾支鉛筆?
        if len(total)>1:
            for i in total:
                final_num = abs(final_num-i)
                
            final_num+=sum_
        else:

            return question5(unit,d1,d2,[],quan)

    elif is_remain==True:  ##如果題目有'剩下'等詞，則做倒推

        for i in total:

            final_num= abs(final_num-i)

            #
        final_num-=sum_
        
            
            

    else:   ##如果沒有符合上面的條件，則依照問題裡的數字與運算符號做計算
        for i in total:
            final_num+=i
            
        final_num+=sum_

    

    if total==[] and sum_==0:  ##如果加減幅度跟初始量都為0，再跑到question2去求解

        final_num =  question2(item,unit,d1,d2,d3,quan,s_unit,m_num)
        
    return abs(final_num)







def question2(item,unit,d1,d2,d3,quan,s_unit,m_num):     ##如果問題中，包含,物品,單位。題目類型:總和

    print("題型 : 2.問總和(問題中，包含物品,單位)")
    #print()

    global final_num,sum_,total

    final_num= 0
    
    opr = ""  
    sum_ = 0  ##總和(原始)。當有=時，則指定值給sum_
    add = 0   ##數值(sum)增加的幅度
    total = []  ## 最後輸出的總和
    opr = ""
    box = ["+","-","="]
    unit_item={"錢":"元"}

    final_num = 0 ##最後的結果

    #words = []
    
    count_people = 0  ##計算有幾個人

    items = []##暫存物品



    if is_plus==False:

        ##如果是從比較中去找出數值
        ## ex : 我有我有10顆糖果，小明比我多2顆。糖果共有幾顆? 

        final_num = additional("",item,unit,d1,d2)
                
        
        return abs(final_num)
     

    if unit in unit_item:
        
        unit = unit_item[unit]   ##把單位轉換 ex : 錢轉為元
        

    

    #for i in d2:  ##words把d2所有詞存進去
     #   words.append(i)


########### 先找出物品的單位存在於哪些位置 ############################################################
    

    if unit!="":  ##如果單位不為空，則找出和物品相對應位置

        for i in range(len(d2[item][0])):   ##物品跟單位出現重複
            
            if d2[item][0][i] in d2[unit][2]:
                
                items.append(d2[item][0][i])  ##items存入底層位置(單位)，計算時可與單位出現的位置做比對

        
        units = d2[unit][2]  ##單位在那些句子出現

    else:  ##如果單位為空，則找出最底層標籤，作為單位:

        for i in d2:
            
            if d2[i][0][0]=="none" and d2[i][2][0] not in ["a100","a101","a102","a103"]:  ##如果本身位置為最底層，但不是在["a100","a101","a102","a103"]中，將這個詞放到items中
                #print(i,d2[i][0][0],d2[i][2][0])
                
                items.append(d2[i][2][0])
        

    
    
    temp_people=[]  ##暫存詞彙。計算的過程中，如果有重複，就不做計算

    
    temp_p = [] ##暫存位置，做計算時，有重複的位置不可再做計算


########### 跑迴圈，找出數字做計算 ############################################################

    ##total : 類型為list，存對應到=的數字
    ##sum_ : 整數，對應到+或-，直接先做計算
    

    for i in d2:  ##從所有詞，包含主事者接受者物品數量...等)中找出哪一個詞是主事者接受者(上一個元素為none時)


        
        if i not in temp_people:  ##判斷現在這個詞有沒有被處理過，如果有就跳過，沒有則進行處理


            temp_people.append(i)   ##暫存這個詞

            
            
            if d2[i][1][0]!="none":   ##如果對應到運算符號(+-=)不為none，則表示為最上層元素，可以試著找出數字

                

                peoples = d2[i][0]  ##這個詞最底層的位置(單位出現的位置)

                

########### 判斷這個物品是否能夠直接找出對應數字，如果不能，就要找出主事者與對應數字 ############################################################                
                

                if len(items)!=0 :   ##如果可以直接從物品-單位找出運算

                    sum_,total = check_item(i,d2,count_people,items,temp_p,sum_,total)
                    
                    print("直接從物品找數字做計算")


                        

                    if len(total)==0 and sum_==0:

                        sum_ = 0
                        total = []


                        sum_,total = change_to_people(i,d2,peoples,items,temp_p,units,sum_,total,count_people)

                        
                
                elif len(items)==0:  ##如果物品最底層位置數量為0(表示要從其他主事者位置去找)

                    
               
                    print("找出主事者再向下延伸")
                    sum_,total = change_to_people(i,d2,peoples,items,temp_p,units,sum_,total,count_people)



                    temp_people.append(i)   
                    count_people+=1

                    print(sum_,total)

            else:##如果+-=為none:

                #print("先找最上層元素，再往下延伸")
                temp_people.append(i)
                count_people+=1
            
                

########### 依照變數，去做計算，輸出一個final_num ###############################
    
    
    if is_remain==True:
        
        
        ##如果問題中有"剩下"，則做倒推
        ##ex : 我有一些糖果，吃了5顆，剩下3顆。蘋果原有幾顆?
        
        
        if len(total)==1 and sum_!=0:
            
            
            final_num = abs(total[0]-sum_)
            
            
            
        elif len(total)==2:
            final_num = abs(total[0]-total[1])
            final_num = abs(final_num+sum_)

        elif len(total)==0 :
            
            
            print(total)

        
            
        return final_num


    if add_back==True :

        new_list = ",".join(temp_people)
        num_list = re.findall(r"\d+",new_list)
        num_list_int = list(map(int,num_list))
        #print(num_list_int)
        add = int(num_list_int[0])
        final_num = sum_+add
                   
        print(total)
        print(add)
        print(sum_)
        print(temp_people)
        print(final_num)

        return final_num
    
    

    if len(total)==0:
        
        total.append(0)
    
    
    
    if is_minus==True and quan!= 0:

        
        
        ## 問題中有["就","不夠","就有","還要","就可以","才","找回"]的關鍵字
        ##用問題中的數字去扣
        ## ex : 我有10支筆。再多少支就有12支筆?

        
        total[0] += sum_
        if total[0]<0:
            final_num = quan+total[0]
        else:
            final_num = quan-total[0]

        

    elif is_minus==True :
        

        ## 問題中有["就","不夠","就有","還要","就可以","才","找回"]的關鍵字，但沒有數字
        ## 做倒推運算
        ## ex : 小明有10張郵票，想要收集到15張。還不夠幾張郵票?
        
        
        for i in total:
            final_num = abs(final_num-i)
        total[0] -= sum_

    elif change_plus==True:
        

        ##如果題目中，有'其中'這個關鍵字，表示有一個總體值與幾個物品的值，問某一個的物品的值，則將所有值做減法
        ##ex : 我有10支筆，其中紅筆有2支，藍筆有3支。黑筆有幾支?

        for i in total:
            
            final_num = abs(final_num-i)
        final_num = abs(final_num-sum_)

    elif add_back==True:


        for i in total:

            final_num = final_num+i

        

        
    else:

        
        
        if len(total)>1:   ##如果有兩個=，應該是有原本數量跟最後數量，要問花費多少

            

            if len(total)==2:    ##如果兩者一樣，條件也一樣
                
##                if count_people==1:
##                    a = total[0]
##                    b = total[1]
##                    print("有兩個=，所以有原本的值")
##                    if a>b:
##                        final_num = a-b
##                        final_num+=sum_
##                    else:
##                        final_num = b-a
##                        final_num+=sum_


                if "剩下" in d2:
                    a = total[0]
                    b = total[1]
                    #print("有1個剩下的值，和初始值")
                    ##ex : 我有10顆糖果，吃了一些，剩下3顆。糖果被吃了幾顆?
                    if a>b:
                        final_num = a-b
                        final_num+=sum_
                    else:
                        final_num = b-a
                        final_num+=sum_
                    

                else:
                    
                    if is_differ==True :#or d2[item][3][0]=="none":

                        a = total[0]
                        b = total[1]
                        #print("兩者相差")
                        ##問題裡包含["相差","差距","差"]的關鍵字
                        ## 我有3個蘋果，爸爸有10個蘋果。相差多少個蘋果?
                        
                        if a>b:
                            final_num = a-b
                            final_num+=sum_

                                
                        else:
                            
                            final_num = b-a
                            final_num+=sum_
                            
                    else:
                        #print("好幾個=，總和運算")
                        for i in total:
                            final_num+=i

            else:
                
                for x in total:
                    
                    final_num+=x
                    
                
        else:
            
            #print("直接根據裡面的值加減運算")

            

            if is_reverse==True:

                ##問題中包含["原本","原來","原先","起初","一開始","剛開始","最早","最初","原有"]的關鍵字，是倒推計算
                ## ex : 我有一些蘋果，我吃了2顆，剩下3顆。原來有幾顆蘋果?
                final_num=total[0]-sum_

            elif len(total)==1:
                
                final_num = total[0]+sum_
                
                return abs(final_num)
            else:
                
                for x in total:
                    final_num+=x
                
                final_num+=sum_
                return abs(final_num)
                
            
    
##    total += sum_
##
##    if is_minus==True and quan!= -1:
##
##        total = quan-total

    #print(4,"總增加幅度",sum_)
    #print(4,"初始量",total)

    
##    if m_num!=0 and is_mul==True:
##        final_num*=m_num
##       
    
    
    return abs(final_num)

def change_to_people(i,d2,peoples,items,temp_p,units,sum_,total,count_people):##從其他主事者位置去找出對應數字

    temp_p = []
   
    ##total : 類型為list，存對應到=的數字
    ##sum_ : 整數，對應到+或-，直接先做計算

    if len(items)==0 or len(total)==0:  ##如果物品最底層位置數量為0(表示要從其他主事者位置去找)

                    
               
        #print("找出主事者再向下延伸")
    

        for j in peoples:  ##從peoples去找(存放最底層位置的list)

            

            if j in units: ##如果主事者出現的句子跟單位一樣，進行計算


                
                if j not in temp_p:  ##如果沒有重複位置，則做計算

                    temp_p.append(j)  ##存入這個位置，之後計算不會再用這個位置

                    x = peoples.index(j)  ##找出目前peoples對應到的位置

                    
                    
                    opr = d2[i][1][x]  ##根據位置找出+-=

                    

                    

                    if opr =="=":     
                        y = d2[i][0][x]
                        if len(d2[i][3])!=0:
                            total.append(int(d2[i][3][x]))
                            #print(3,opr,int(d2[i][3][x]))
                        
                        

                    elif opr =="+" and count_people==0:
                        y = d2[i][0][x]
                        if len(d2[i][3])!=0:
                            sum_ += int(d2[i][3][x])
                            #print(3,opr,sum_)
                        

                    elif opr =="-" and count_people==0:
                        y = d2[i][0][x]
                        
                        if len(d2[i][3])!=0:
                            sum_ -= int(d2[i][3][x])
                            #print(3,opr,sum_)
    
    return sum_,total

def check_item(i,d2,count_people,items,temp_p,sum_,total):  ##直接從物品-單位找出運算

    ##total : 類型為list，存對應到=的數字
    ##sum_ : 整數，對應到+或-，直接先做計算

    peoples = d2[i][0]  ##這個詞最底層的位置(單位出現的位置)


    #print(items)
    if len(items)!=0 :   ##如果可以直接從物品-單位找出運算
        
        #print("直接從物品找數字做計算")

        for j in items:  ##從物品的最底層位置下去跑

            

            if j in d2[i][0]:  ##如果此位置有在目前的詞的最底層位置，則進行計算

                
                

                if j not in temp_p:  ##如果沒有重複位置，則做計算

                    temp_p.append(j)  ##暫存位置，之後如果遇到這個位置，就不重複做計算
                

                    x = d2[i]   ##d2的i索引list
                    

                    opr = x[1][x[0].index(j)]  ##找出+-=
                    add = int(x[3][x[0].index(j)])  ##找出數字

                    

                    if opr=="=":
                        
                        total.append(add)   ##如果是=，則將數字放到total中
                        #print(3,opr,add)
                    
                    elif opr =="+" and count_people==0:  ##如果是+，則sum_ 會加入這個值
                        
                        sum_+=(add)
                        #print(3,opr,add)
                            

                    elif opr =="-" and count_people==0:  ##如果是+，則sum_ 會扣掉這個值
                        
                        sum_-=(add)
                        #print(3,opr,add)
    return sum_,total

def question3(init_list,name,item,unit,d1,d2,d3,big,big_small,oppo,true_false):     ##如果問題中，包含主事者,物品,單位。題目類型:比大小

    global final_num,sum_,total

    opr = ""   ##運算符號
    sum_ = 0  ##總和(原始)。當有=時，則指定值給sum_
    add = 0   ##數值(sum)增加的幅度
    total = 0  ## 最後輸出的總和

    ans = ""  ##最後答案

    peoples = [] ##存題目的人名

    people_sort = [] ##將peoples排序後的list

    switch=""

    big_list=[]

    temp_list=[] ##暫存大小量詞

    num_list = [] ##存放數值    

    print("題型 : 3.比大小")
    #print()

    
    

############如果元素的上一項為none，表示為主事者接受者，存入peoples  ############
    for i in init_list:  

        if i[2][0]=="none":
            peoples.append(i[0])
    people_sort = peoples

    
    
############## 接者延伸，比大小 ###################################################

    

    if big in oppo:
        switch = oppo[big]  ##如果有相反詞，將switch指定
        
        if switch in d2:
            
            print("相反詞",switch)
      
    if len(peoples)>1:  ##如果題目的主事者個數>1，則去找出數字，存到num_list
        for i in peoples:
            if d2[i][3][0] not in ["none",0]: ##如果主事者對應到的數字不為none或0，則先存入這個數字
                num_list.append(d2[i][3][0])
        
    else:

        ##如果題目的人名數量為0，可能是物品，要去找其他值
        
        
        peoples = []
        
        if len(d2["="][2])<2:  ##如果包含=的物品太少<2個，則無法比較，會直接找數字做比大小(這個可能有bug)
            print("以數字去做比較")

            #biggest = 0
            #big_pos = 0
            
            for i in d2:

                if i.isdigit():
                   

                    if peoples==[]:

                        peoples.append(i)

                        num_list.append(int(i))

                        #biggest = int(i)
                        #big_pos = 0
                    else:

                        for j in range(len(num_list)):

                            if int(i)>=num_list[j]:

                                num_list.insert(j+1,int(i))
                                peoples.insert(j+1,i)
                                break

                

        else:

            print("以物品去做比較")

            ## 公園有3隻狗和5隻貓。哪一種比較多?

            ##把物品與對應到的數字存進去
        
            for i in d1:

                try:
                    num_list.append(int(d1[i][0]))
                    
                    pos = d1[i][1][0]  ##數字的前一個位置，即為物品

                    if d1[pos][0] not in ["+","-","="]:
                        peoples.append(d1[pos][0])
                    else:
                        pos = d1[pos][1][0]  ##數字的前一個位置，即為物品
                        if d1[pos][0] not in ["+","-","="]:
                            peoples.append(d1[pos][0])
                    
                except:
                    continue
                    

    print("名單:",peoples)
    #print("比",big)
    
############################ 如果裡面有數值，用數值來比較大小 ##########################
    
    if len(num_list)!=0:   
        
        output = []

        opr = ""
        add = 0

    ##########如果問題有數值，表示要問裡面的人是否可以達到這個數量
        
        if quan!=0 and unit in d2:  

            ##小明有50元，小美有60元。誰可以買55元的飲料?
            
            try:
            
                for i in peoples:

                    final_num= 0
                    add = 0
                    opr = ""

    ################################從人物裡去一個一個判斷是否可以達到此數字##########

                    for j in range(len(d2[i][1])):    

                        opr = d2[i][1][j]
                        add = d2[i][3][j]

                        if opr == "=" or opr == "+":
                            final_num+=add
                        else:
                            final_num-=add

                    
                    if final_num>=quan:  ##如果可以。則存入output
                        
                        output.append(i)
                
                
                for i in output:
                    
                    ans+=(i+",")
                ans = ans[:len(ans)-1] ##刪除最後一個逗點
                return ans   ##return 答案
            except:
                print()



################################如果是問數量的多寡##############################################

        ##小明有50元，小美有60元。誰的錢比較多?
        
        biggest = 0 ##設最大值
        smallest = 99999999999999999
        big_pos = 0 ##最大值的位置
        small_pos = 0

        
        
        for i in range(len(peoples)):

            if num_list[i]>=biggest:  ##如果比最大值大，則改變最大值
                
                biggest = num_list[i]
                big_pos = i
                
            if num_list[i]<=smallest:  ##如果比最大值小，則改變最小值
                
                smallest = num_list[i]
                small_pos = i

        if big_small=="大": ##如果是比大，則從最大值位置找出答案
            
                
            ans = peoples[big_pos]
            
        elif big_small=="小":  ##如果是比小，則從最小值位置找出答案
            
                
            ans = peoples[small_pos]

        
                

##########################如果裡面沒有數值，則去針對對應到的"大"、"小"做判斷##########################    

    else:
        
        ##ex : 小明比小美老，小美比小強老。誰最老?
        ## 小明:小美 = 大:小
        ## 小美:小強 = 大:小

        ##如果是比大，先找出大的位置，再找"大"出現的人或物，如果此人無"小"的部分，則最大
            
        if big_small=="大":
            
            

            for i in people_sort:   ##從人名去延伸

                temp_list=[]

                pos = d2[i][2][0]  ##找出人物位置

                big_list = d1[pos][2]  ##這個人物的下一個位置(大或小)

                for j in big_list :

                    next_pos = d1[j]  ##下一個位置
                    next_adj = d1[next_pos[2][0]]  ##比較的單位
                    

                    if next_adj[0]==big or next_adj[0]==switch: ##確認比較的單位一致(例如: 快慢)

                        temp_list.append(d1[j][0])  ##temp_list存入大或小
                      
                        

                   
                if "小" not in temp_list:  ##如果temp_list不包含"小"，則為最大的

                    ans = i

                    #print("正解: ",ans)

        elif big_small=="小":

            

            for i in people_sort:   ##從人名去延伸

                temp_list=[]

                pos = d2[i][2][0]  ##找出人物位置

                big_list = d1[pos][2]  ##這個人物的下一個位置(大或小)

                for j in big_list :

                    next_pos = d1[j]
                    next_adj = d1[next_pos[2][0]]
                    

                    if next_adj[0]==big or next_adj[0]==switch: ##確認比較的單位一致(例如: 快慢)

                        temp_list.append(d1[j][0])
                      
                        

                   
                if "大" not in temp_list:

                    ans = i
                    #print("正解: ",ans)

                
    if is_differ:  ##如果問相差，表示最大與最小相差

        ans = num_list[0]-num_list[len(num_list)-1]
        ans = abs(ans)
        ans = str(ans)
        
    return ans







def question4(people,name,item,unit,d1,d2,d3,quan,s_unit,m_num):     ##如果問題中，包含主事者,單位。題目類型:總和

    print("題型 : 4.問總和(問題中，包含主事者,單位)")

    global final_num,sum_,total
    

    if is_plus==False:

        ##如果是從比較中去找出數值
        ##我有10元，你比我多5元。你有多少元?   
        
        final_num = additional(name,"",unit,d1,d2)
        

            
        return abs(final_num)

    final_num = 0
    
    opr = ""

    

    total = []

    sum_ = 0

    add = 0

    box = ["+","-","="]

    unit_item={"錢":"元"}
    if unit in unit_item:
        
        unit = unit_item[unit]   ##把單位轉換 ex : 錢轉為元


##################如果人名所對照的+-=數量為1，且對應之數字為0，則移到question5做計算##################
    
    if len(d2[name][1])==1 and d2[name][3][0]==int(0):   
        final_num = question5(unit,d1,d2,d3,quan)
        return final_num


############跑迴圈，找出單位一樣的，找出數字和運算符號###################################################
    
    for i in range(len(people)):  #主事者出現在那些句子
        
        
        if people[i] in d2[unit][2]: ##如果人出現的位置跟單位位置一樣(在這個句子中)
            
            opr = d2[name][1][i]  ##找出+-=

              
            if len(d2[name][3])!=0:
                add = d2[name][3][i] ##從d3去找出這句話相對應的數字
                add = int(add)
            if opr =="=":  ##如果運算符號為=，則預設總和為此數字
                total.append(add)
            elif opr =="+":  ##如果運算符號為+，則sum增加
                           
                sum_+=add
                            
            elif  opr =="-":  ##如果運算符號為-，則sum增加
                           
                sum_-=add

            #print(opr,add)


##    is_mul = check_mul(name,item,unit,d1,d2)
##
##    if is_mul==True:
##        
##        find_m_num(name,item,unit,d1,d2,d3,is_reverse,quan,is_minus,is_differ,is_plus,False,is_remain,s_unit,m_num)
##        
##    
    
    

    if len(total)==1 and total[0]==0:  ##如果total長度為1，且值為0，則移到question5去算
        
        final_num = question5(unit,d1,d2,d3,quan)
        return final_num
    

    if is_remain==True:

        print(total,sum_)
        
        ##如果題目中有剩下，則做倒推運算
        ##ex : 我有30元，花了一些錢後，剩下20元。我花了多少元?
        
        if len(total)==1:
            final_num = total[0]-sum_
        else:
            for i in range(len(total)):
                final_num += total[i]
            final_num-=sum_
                
            
        return abs(final_num)
        

    if len(total)==0:
        total.append(0)

    
    if is_minus==True and quan!= 0:

        ##問題中有["就","不夠","就有","還要","就可以","才","找回"] 的關鍵字。
        ##用問題中的數字去扣
         ## 我存了100元。我還要再存多少才有300元?
        
        total[0] += sum_
        final_num = quan-total[0]

    elif is_differ==True and len(total)>1:

        ##問題中包含["相差","差距","差"]的關鍵字
        ## 則用兩個初始值去做減法
        ## ex : 我有20元，想存到100元。我還差多少元?

        a = total[0]
        b = total[1]

        if a>b:
            final_num = a-b
        else:
            final_num = b-a


    elif change_plus==True:
        
        for i in total:

            final_num=abs(final_num-i)
            #print(final_num)
        final_num-=sum_

    
                
    else:
        
        if len(total)>1 and is_reverse==False:  ##做一般的加法
            for i in range(len(total)):
                
                final_num+=total[i]
            final_num+=sum_
        elif is_reverse==True:

            ##倒推
            ##["原本","原來","原先","起初","一開始","剛開始","最早","最初","原有"]
            ## ex : 我有一些錢，花了30元後，剩下10元。我原本有多少錢?
            a = 0
            for i in (total):
                a+=i
            
            b = sum_
            
            final_num = a-b
        else:
            if len(total)>0:
                
                final_num = total[0]+sum_
            else:
                final_num = sum_

    
    
    return abs(final_num)


def additional(name,item,unit,d1,d2):
    print('additional')
    global final_num,sum_,total

    opr = ""  ##+=

    add = 0 ##暫存增加幅度

    total = []  ##總和(初始值)

    sum_ = []  ##存增加幅度

    add= 0

    temp_pos = []  ##暫存最底層位置，如果有重複，則不做計算

    final_pos = []  ##終點位置list

    botton_pos = []  ##單位出現的位置，可做對照用(沒用到)

    point = ""  ## 當作指標

    count = 0  ##算人數

    final_num = 0

    temp_name = []   ##暫存名稱，用過不可以再用

    eq_  = False  ## '='存在的list只有一個元素

    
    ## 找出終點list#########################################
    if name!="":  ##如果主事者不為空值，存入終點位置
        if name in d2:
            final_pos = d2[name][0]
        
    elif item!="" and '=' in d2[item][1] and len(d2[item][1])>1:

        
        
        for j in range(len(d2[item][0])):
            
            if d2[item][0][j] in temp_pos:
                break
            else:
                
                opr = d2[item][1][j]
                add = d2[item][3][j]

                if opr=="+" :
                    add = 0-add
                    sum_.insert(0,add)
                    
                elif opr=="-" :
                    
                    sum_.insert(0,add)
                    
                elif opr=="=" :
                    total.append(add)
                    
                    break
                
                temp_pos.append(d2[item][0][j])
        
        for i in total:

            final_num+=i
        for i in sum_:
            final_num+=i
                
        return abs(final_num)

    
    elif item!="" and '=' in d2 and len(d2[item][1])>1 and (d2[item][1][0])!='none':

        final_pos = d2[item][0]

    elif item!="" and item in d2 and len(d2[item][1])==1 and (d2[item][1][0])!='none':
        final_pos = d2[item][0]
        
    else:  ##如果沒有主事者，則找到一個+-=數量為1的，存入位置
        
        for i in d2:
            if d2[i][1][0]!="none" and len(d2[i][0])==1:
           
                final_pos = d2[i][0]

                break

        if len(final_pos)==0:

            for i in d2:
                if d2[i][1][0]!="none" and "=" not in d2[i][1][0]:
               
                    final_pos = d2[i][0]

                    break


                

    
    
     
                
    units = d2[unit][2]   ##存單位存在的位置
    
    
    
##    if item!="" and unit!="":  ##如果物品和單位最底層一樣，則botton_pos存入此位置
##
##        items = d2[item][0]  ##存入物品最底層位置(單位)
##        
##
##        for i in items:
##            if i in units:
##                botton_pos.append(i)  ##物品底層位置和單位存在位置一樣，則存入
##
##    elif item=="" and unit!="":  ##如果物品為空，單位不為空，則botton_pos 指定為單位存在位置
##        botton_pos = units

    
    ## 找出起始位置################################################ 
    
    if len(final_pos)>0:

        if len(final_pos)==1 and final_pos[0] in d2[unit][2]:
        
            point = final_pos[0]  ##預設指標指向終點第一個位置
        else:
            list_ = final_pos[::-1]

            
            for i in list_:

                if i in d2[unit][2]:
                    point =i
                    break   
        
    else:
        for i in final_pos:
            if i in d2[unit][2]:
                point = i  ##預設指標指向終點第一個位置

                

#####################如果total長度為空，則跑迴圈，讓total填入數字##################

    x = 0
   
    while len(total)==0:   


        if "=" not in d2 or len(total)!=0:  ##如果沒有=，嘗試用+-找答案
        
            if item !="" and item in d2:
                
                point = d2[item][2][0]
                
                point = d1[point][2][0]
                
                
                if d1[point][0].isdecimal():  ##如果前一個位置的值可以轉為整數，則return這個數字
                    total.append(int(d1[point][0])) 
                else:
                    final_num = 0
                
                
                    

            if point!="":
                past = d1[point][1][0]
                if d1[past][0].isdecimal():  ##如果前一個位置的值可以轉為整數，則return這個數字
                    final_num = int(d1[past][0])
                else:
                    final_num = 0
            
            break

        else:
            

            for i in d2:   

                if '=' in d2[i][1] and len(d2[i][1])==1:

                    total.append(d2[i][3][0])
                    
                    eq_ = True
                  
            
            for i in d2:

                

                if d2[i][1][0]=="none":  ##如果+=數量為空，則退出
                    break

                
                pos = d2[i][0]  ##底層位置
                
                #print(pos,point)
                
                if point in pos and point not in temp_pos and point in d2[unit][2]: #and len(pos)>1  如果point位置沒有在temp_pos中，則做計算
                    
                    x = pos.index(point)  ##指標在這個位置的第幾項

                    opr = d2[i][1][x]  ##找出+-
                    add = d2[i][3][x]

                    
                    #if i not in temp_name:  ##如果這個名字還沒有處理過，則遇到+-=都進行計算

                        
                    if opr=="+" and eq_==False:
                        sum_.insert(0,add)
                    elif opr=="-" and eq_==False:
                        add = 0-add
                        sum_.insert(0,add)
                        
                    elif opr=="+" and eq_==True:
                        add = 0-add
                        sum_.insert(0,add)
                    elif opr=="-" and eq_==True:
                        
                        sum_.insert(0,add)
                    
                    elif opr=="=":
                        
                        total.append(add)

                    temp_name.append(i)
                    
                    temp_pos.append(point) ##存入位置，之後不再用此位置計算

                    

                    if x>=1:  ##找出下一個位置
                        
                        point = d2[i][0][x-1]

                        break
                    else:
                        break
                            
                  
                else:
                    
                    if d2[i][1][x]=="=" and point not in d2[unit][2]:
                        
                        if len(sum_)>1:
                          total.append(-sum_[0])
                          del sum_[0]
                        else:
                            total.append(0)
                        
                        break
                    
                    if x>=1:
                        point = d2[i][0][x-1]
                        
                        x-=1
                        break
                    #else:
                        
                        #break
##                    print(x,d2[i][0],i)
##                    if x>=1:  ##找出下一個位置
##                        if d2[i][0][x-1] in d2[unit][2]:
##                            point = d2[i][0][x-1]
     
    if len(total)==0:
        total.append(0)

    count = 0

    
################################################## 算出答案 #########################################
    
    if name!="" or (item!="" and d2[item][1][0]!="none") :  ##如果主事者不為空或是物品不為空(且+-=不為none)，則只要做一次計算

        

        for i in range(len(sum_)):
            final_num+=sum_[i]
            print(final_num)

        final_num+=total[0]
            
    else:
            ##如果上面不符合，則要做迴圈一直計算
        
        final_num+=total[0]
        #print("初始值",final_num)

        
        while count<len(sum_):
            final_num+=total[0]  ##每次計算都要用這個數值再去做計算
            for j in range(0,count+1):
            
                final_num+=sum_[j]
                #final_num+=total[0]
                #print(sum_[j],final_num)
            count+=1
       
            
    
            
    return abs(final_num)

    

def question5(unit,d1,d2,d3,quan):     ##如果問題中，包含單位。題目類型:總和

    print("題型 : 5.問總和(問題中，只有單位)")

    global final_num,sum_,total
    
    opr = ""

    total = []

    sum_ = 0

    add = 0

    box = ["+","-","="]

    unit_item={"錢":"元","位":"號","個":"人","人":"個"}

    words = []

    temp_name = [] ##暫存名稱

    main = False  ##判斷主角

    temp_unit = []##暫存單位
  

    if unit in unit_item and unit not in d2:
        
        unit = unit_item[unit]   ##把單位轉換 ex : 錢轉為元

    name = "" ##紀錄主事者

    item = ""  ##紀錄物品

    final_num = 0

    for i in range(len(d2[unit][2])):

        prev = d2[unit][2][i]   ##找出單位目前位置

        prev = d1[prev][1]  ##找出單位的前一個位置(數量)

        for j in prev:
            words.append(j)##words存入數量的位置
    
    

    ##先從單位，向上找出存在於第幾句

##    for i in range(len(d2[unit][2])):
##
##        c = d2[unit][2][i]   ##這個單位的位置
##
##        words.append(d1[c][1][0])  ##單位存在的位置
##
##    
##    words = prev

    sentense = []
    
    for i in d2:
        sentense.append(i)  ##sentense存入詞彙



############跑迴圈，找出是否有主角(對應到的數字不只一個)。如果沒有特定主角，則每一個主事者對到的數字要做處理##################################
    

    for n in words:   

        
        ##sentense = d3[n[0]][0]

        temp_unit = []

        

        if main == False:  ##如果沒有特定主角，則跑一次就結束

            

######################從這句話的詞彙中，找出主事者#######################################################

            for x in sentense:   

                
                
                if d2[x][1][0]!="none" and x not in temp_name:   ##+-=不為空值，表示x為主事者接受者

                    
                    temp_name.append(x)  ##temp_name存入主事者接受者

                    for i in d2[x][0]:
                        if i in d1:
                            if d1[i][0] ==unit:  ##暫存單位
                                temp_unit.append(i)

                    


                    if len(d2[x][1])>1 and main!=True and len(temp_unit)>1:  

                        
                        name = x
                        print(2,"主角",x)

                        main = True

                        for i in range(len(d2[x][1])):  ##以此主角往下找出+-=與數字

                            

                            opr = d2[x][1][i]  ##+-=
                            s = d2[x][0][i]  

                            

                            

                            #if len(d3[s[0]][1])!=0:
                                  
                            add =int(d2[x][3][i])

                            if d2[x][0][i] in d2[unit][2]:

                                if opr=="=":
                                    total.append(add)
                                    print(3,opr,add)

                                elif opr=="-":
                                    sum_+= add
                                    print(3,opr,add)
                                        
                                elif opr=="+":
                                        
                                    sum_-= add
                                    print(3,opr,add)
                                
                                    
                        break

###################################如果沒有特定主角，則每一個對應到的數字都做處理##########################################
                    
                    else:  



                        #s = d2[x][2][0]  ##主事者(位置)

                        
                        name = x

                        #if len(d3[s[0]][1])!=0 :

                        for i in range(len(d2[x][0])):

                            s = d2[x][0][i]

                            if s not in d1:
                                continue

                            if d1[s][0]==unit: 

                                add =int(d2[x][3][i])

                                opr = d2[x][1][i]

                                if opr=="=":
                                    total.append(add)
                                    print(3,opr,add)

                                elif opr=="-":
                                    sum_+= add
                                    print(3,opr,add)
                                elif opr=="+":
                                    
                                    sum_-= add
                                    print(3,sum_,add)
                                
    


###################################依照變數去做計算######################################################                   
    
    
    if len(total)==0:
        total.append(0)

    if unit=="層" or unit=="樓":
        for i in total:
            final_num-=i
        final_num-=sum_
        return final_num

    if is_plus==False:

        ##如果是從比較中去找出數值，找出全體總和
        ##ex : 我有10顆蘋果，你比我多5顆蘋果。則蘋果共有幾顆?
        
        
        final_num = additional("","",unit,d1,d2)

        
            
        return abs(final_num)

    
    
    if is_remain==True:

        
        
        if len(total)>=1:
            for i in total:
                final_num = abs(final_num-i)

             
            final_num-=sum_

            
        else:
            
            final_num-=sum_

            

        
        return abs(final_num)

    if is_minus==True :

        ##用問題中的數字去扣
        ##如果問題中包含["就","不夠","就有","還要","就可以","才","找回"]的關鍵字，則用減法運算
        ##ex : 我有10張郵票。還要幾張就有20張?
        
        if quan!= 0:
            total[0]+=sum_
            if total[0]<0:
                final_num = quan+total[0]
                
            else:
                final_num = quan-total[0]
        elif len(total)>1:
            a = total[0]
            b = total[1]
            final_num = abs(a-b)
        elif len(total)==1:
            
            a = total[0]
            b = sum_
            if a<0:
                final_num = abs(a+b)

            elif a>0 and abs(a)<abs(b) and b<0:
                final_num = abs(a+b)
            else:
                final_num = abs(a-b)

    

    elif is_minus==True and quan==0:

        ##用問題中的數字去扣
        ##如果問題中包含["就","不夠","就有","還要","就可以","才","找回"]的關鍵字，則用減法運算
        ##ex : 我有30元，想要買一杯50元的飲料。還要再多少元?
            ## 
##        if len(total)==0:
##            total.append(0)
        total[0] -= sum_
        final_num = abs(total[0])

        
        
    elif is_reverse==True:

        ##如果問題中包含["原本","原來","原先","起初","一開始","剛開始","最早","最初","原有"]的關鍵字
        ##則用初始量與變化量相減
        ##ex : 我有一些錢，花了10元，剩下20元。原本有多少元?
        if sum_!= 0 :
            total[0] -= sum_
            final_num = abs(total[0])
            
        elif sum_==0:
            units = d2[unit][2]
            for i in units:
                pos = i
                back = d1[pos][1][0]
                if int(d1[back][0]) not in total:
                    total.append(int(d1[back][0]))
            for i in total:
                final_num = abs(final_num+i)
        

    elif is_differ==True and len(total)>1:  ##相差

        ## 問題中包含["相差","差距","差"]的關鍵字
        ## 且初始量數量大於一個，則用兩個初始量去做減法
        ## ex : 我有10元，你有20元。相差多少元?

        a = total[0]
        b = total[1]

        if a>b:
            final_num = a-b
        else:
            final_num = b-a

    
    elif change_plus==True:

        
        
        for i in total:
             final_num = abs(final_num-i)
            
        final_num-=sum_

        print(final_num)
    else:
        
        
        if len(total)>1:
            #print("好幾個=")
            if is_minus==True:
                a = total[1]
                b = total[0]
                if a>b:
                    
                    final_num = a-b
                else:
                    final_num = b-a
            else:
                for i in range(len(total)):
                    final_num+=total[i]
                final_num+=sum_
        else:
            #print("依照原始數量跟加減幅度做計算")
            if len(total)==0:
                total.append(0)
            
            final_num = total[0]+sum_

    #print("初始值:",total)
    #print("增加幅度:",sum_)
    
    
    return abs(final_num)
    

   
def question6(people,obj,name,item,unit,d1,d2,d3,quan,peoples):

    print("題型 : 6.多個主事者或接受者(問題中，包含主事者,接受者,物品,單位)")
    print()
    global final_num,sum_,total
    
    total = []

    u1 = 0
    u2 = 0

    final_num=0



######如果問題裡面有主事者和接受者，則找出相對應的數字#############################

    if obj!="":

        u1 = d2[name][3][0]##主事者對應的數字

        u2 = d2[obj][3][0]##接受者對應的數字

        
######如果問題裡面有兩個主事者，找出相對應的數字#############################
        
    elif len(peoples)==2:

        u1 = additional(peoples[0],item,unit,d1,d2)
        u2 = additional(peoples[1],item,unit,d1,d2)

######如果問題裡面有主事者和接受者超過兩個，則找出相對應的數字，做計算#############################

    elif len(peoples)>2:

        for i in peoples:

            final_num+=additional(i,item,unit,d1,d2)
            
        return final_num
            
    
    items = [name,obj]

    if u1=="none" and u2=="none":  ##如果都是物品，則改用question9去解題
        final_num = question9(items,unit,d1,d2,d3,quan)


##############################依照變數去做計算###################################

    if item!="" or unit!="":##如果物品跟單位不為空值
        
        
        if is_plus==False :

            ##例如 : 我有20元，你比我多10元。你和我共有多少元?

            u1 = additional(name,item,unit,d1,d2)
            u2 = additional(obj,item,unit,d1,d2)

            if is_differ==True:
                final_num = abs(u1-u2)
            else:
                final_num = abs(u1+u2)
            return abs(final_num)

        elif is_differ==True:
            
            ##相差，做減法
            ####題目包含["相差","差距","差"] 的關鍵字
            ##則用兩數做減法
            final_num = abs(u1-u2)
            return final_num


        elif u2!=0 and u1!=0:  ##作加法運算
            final_num = abs(u1+u2)
            return final_num

##############如果u1跟u2其中一個為0，則要判斷要從主事者或接受者那邊找數字做計算######################################
        
        elif u1==0 or u2==0:   

            ##ex: 我有10元，媽媽給我一些錢，我現在有15元。媽媽給我多少錢?

            
            if u1==0 and len(d2[obj][3])>1:  ##如果u1為0，則從接受者那邊去找出數字做運算
                
                for i in range(1,len(d2[obj][3])):

                    u1 = d2[obj][3][i]
                    

                    if u1!=0:
                        final_num = abs(u1-u2)
                        #print(u1,u2)
                        return final_num
                
            elif u2==0 and  name in d2 and len(d2[name][3])>1:  ##如果u2為0，則從主事者那邊去找出數字做運算

                

                for i in range(1,len(d2[name][3])):

                    if name in d2:

                        u2 = d2[name][3][i]
                        
                        if u2!=0:
                            #print(u1,u2)
                            final_num = abs(u1-u2)
                            return final_num


            else:
                final_num = abs(u1+u2)
                
    return final_num
        
        
        
def question7(items,unit,d1,d2,d3,is_reverse,quan,is_minus,is_differ,is_plus,is_total):     ##如果問題中，包含,兩個物品,單位。題目類型:總和

    print("題型 : 7.問總和(問題中，包含2個物品,單位)")
    #print()


    #問題中，包含:兩個物品、數量、單位，這類題型，會有一個物品位於語意網路最上方，因此會對應到數字，則將這個物品視為主事者，進行計算

    #ex : 盤子有10個蘋果，媽媽拿了3個。則盤子剩下幾個蘋果?
    
    global final_num,sum_,total

    opr = ""  
    sum_ = 0  ##總和(原始)。當有=時，則指定值給sum_
    add = 0   ##數值(sum)增加的幅度
    total = []  ## 最後輸出的總和
    opr = ""
    box = ["+","-","="]
    unit_item={"錢":"元"}

    final_num = 0 ##最後的結果

    words = []

    count_people = 0  ##計算有幾個人

  
#######################判斷物品哪一個為主事者，找出對應到數字不為none的那一個即為主事者###########################################
    
    a = items[0]  ##第一個物品
    
#############如果第一個物品對應的數字不為none，做迴圈，找出對應的數字#############

    if d2[a][3][0]!="none": 
        
        for i in range(len(d2[a][3])):   
            
            opr = d2[a][1][i]
            if opr =="=":
                total.append(int(d2[a][3][i]))
            elif opr =="+" and "=" in d2[a][1]:
                add+=int(d2[a][3][i])
            elif opr =="-" and "=" in d2[a][1]:
                add-=int(d2[a][3][i])

            #print(opr,int(d2[a][3][i]))
    else:
            a = "none"
    
    
    b = items[1]  ##第二個物品

#############如果第二個物品對應的數字不為none，做迴圈，找出對應的數字#############
    
    if d2[b][3][0]!="none": 
        
        
        for i in range(len(d2[b][3])):  ##如果對應的數字不為none，開始計算
            
            opr = d2[b][1][i]
            if opr =="=":
                total.append(int(d2[b][3][i]))
            elif opr =="+" and "=" in d2[b][1]:
                add+=int(d2[b][3][i])
            elif opr =="-" and "=" in d2[b][1]:
                add-=int(d2[b][3][i])
            #print(opr,int(d2[a][3][i]))
    else:
        b = "none"

    #print(a,b)
    #print(total)
    
####################################依照變數做計算######################################
    
    if is_plus==False or is_differ==True:

        if is_differ==True:
            #print("算出相差")
            for i in total:
                
                final_num = abs(final_num-i)

        elif is_plus==False:
            #print("算出總和")
            final_num = abs(total[0]+total[0]+add)
        

    else:
        #print("算出總和")
        for i in total:
          final_num+=i  
        final_num = abs(final_num+add)
        

    return final_num

def question8(name,item,unit,d1,d2,d3,quan):     ##如果問題中，包含,物品,單位。題目類型:總和

    print("題型 : 8.問數量(問題中，包含主事者,物品,單位...，原本句子裡面有'總共'")
   # print()
    global final_num,sum_,total

    ## ex : 小明和小美共有100元，小美有70元。則小明有幾元?
    
    opr = ""  
    sum_ = 0  ##總和(原始)。當有=時，則指定值給sum_
    add = 0   ##數值(sum)增加的幅度
    total = []  ## 最後輸出的總和
    opr = ""
    box = ["+","-","="]
    unit_item={"錢":"元"}

    final_num = 0 ##最後的結果

    units = d2[unit][2]



    words = []

    count_people = 0  ##計算有幾個人

    first_total = 0##第一個總和

    #if name!="" or item!="":
       
    unit_list = [] ##暫存單位的位置


########################在d2中，做迴圈，找出數字和運算符號#########################################
    
    for i in d2:

##########################找到的詞跟問題的主事者不一樣，但能對到數字，先存數字###################################################
            
        if d2[i][1][0]!="none" and i != name and len(d2[i][3])!=0:  

            
            x =  d2[i][3] ##數字
            y = d2[i][1]  ##+-=

            for j in range(len(x)):
                    
                opr = y[j]  ##+-=

                num = x[j]  ##數量

                if d2[i][0][j] in units and d2[i][0][j] not in unit_list:  ##如果沒有在unit_list，則做計算
                    unit_list.append(d2[i][0][j])
                    if opr == "=":
                        #print("=",int(num))
                        total.append(int(num))

                    elif opr in ["+","-"]:
                        add += int(num)

                    #print(opr,add)


##########################找出有數量的部分，存進去###################################################       

        elif d2[i][1][0]!="none" and d2[i][0][0]!="none" :  

            #print(i)
                
            x =  d2[i][3] ##數字(list形式)
            y = d2[i][1]  ##+-=(list形式)
            

            for j in range(len(x)):
                    
                opr = y[j]

                num = x[j]

                if d2[i][0][j] in units and d2[i][0][j] not in unit_list:   ##如果沒有在unit_list，則做計算
                    unit_list.append(d2[i][0][j])
                    if opr == "=":
                        #print("=",int(num))
                        total.append(int(num))

                    elif opr in ["+","-"]:
                        add += int(num)

                    #print(opr,add)


#####################算出答案#################################################
    
    for i in total:
        final_num = abs(final_num-i)
        #print(final_num)


    
    
    final_num+=add

    

    

    return abs(final_num)


def question9(items,unit,d1,d2,d3,quan):     ##如果問題中，包含,兩個物品,單位。題目類型:總和

##################################兩個對應到的數字都為none#####################################

##小明有2個蘋果和3個番茄。則蘋果和番茄共有幾個?

    print("題型 : 9.問題中，包含兩個物品")
    #print()
    global final_num,sum_,total
    opr = ""  
    sum_ = 0  ##總和(原始)。當有=時，則指定值給sum_
    add = 0   ##數值(sum)增加的幅度
    total = []  ## 最後輸出的總和
    opr1 = ""
    opr2 = ""
    box = ["+","-","="]
    unit_item={"錢":"元"}

    final_num = 0 ##最後的結果

    words = []

    count_people = 0  ##計算有幾個人

    #items = []##暫存物品

    t1 = 0
    t2 = 0

    
    
    if is_plus==False:   ##如果是從比較中去找出數值，要再去找出一個=，做運算

        ##我有小明有2個蘋果，番茄比蘋果多3個。則蘋果和番茄共有幾個?


        t1 = additional("",items[0],unit,d1,d2)
        
        t2 = additional("",items[1],unit,d1,d2)
        
        
            
        #return final_num


##################################找出最上層元素(主事者)，之後才能往下找出物品對應到的數字####################################
##        
##    for i in d1:
##        
##        if d1[i][1][0]=="none":  ##如果前一個位置為none，表示為最上層
##
##            name = d1[i][0]
##            break
##
##
#################################找出兩個物品最底層位置，接者由主事者往下跑，如果對應的位子和物品一樣，則可以找出數字######################
##        
##    pos1 = d2[items[0]][0][0] #兩個物品最底層位置
##    pos2 = d2[items[1]][0][0] #兩個物品最底層位置
##
##    for i in d2[name][0]:  ##主事者最底層位置
##        if i==pos1:  ##位置和物品最底層位置一樣，可以找出數字
##            pos = d2[name][0].index(i)
##            opr1 = d2[name][1][pos]  ##+-=
##
##            if d2[name][0][0] in d2[unit][2] and t1==0:
##                t1 = d2[name][3][pos]  ##數字
##
##                
##        elif i==pos2:##位置和物品最底層位置一樣，可以找出數字
##            pos = d2[name][0].index(i)
##            opr2 = d2[name][1][pos]  ##+-=
##
##            if d2[name][0][1] in d2[unit][2]and t2==0: 
##                t2 = d2[name][3][pos]  ##數字
##
##    #opr1 = d2[name][1][0]  ##+-=
##    #opr2 = d2[name][1][1]  ##+-=
##
##
##    print(items[0],t1)
##    print(items[1],t2)
##
##    
##

    t1 =  question2(items[0],unit,d1,d2,d3,quan,s_unit,m_num)
    print(items[0],t1)
    t2 =  question2(items[1],unit,d1,d2,d3,quan,s_unit,m_num)
    print(items[1],t2)
####################依照變數做出計算#####################################################    
    
    if is_differ==True:
        ##問題有包含["相差","差距","差"]的關鍵字
        ##將兩數做減法運算
        ##例如 : 小明有2個蘋果和3個番茄。則蘋果和番茄差幾個?
        final_num = abs(t1-t2)
    elif is_remain==True:
        
        final_num = abs(t1-t2)
    elif change_plus==True:
        final_num = abs(t1-t2)
        

    else:
        final_num = abs(t1+t2)
    
    
    
    return final_num


def question10(name,unit,d1,d2,d3,quan):     ##如果問題中，包含第

    print("題型 : 10.問總和(問題中，包含'第')")

    global final_num,sum_,total
    opr = ""

    total = []

    sum_ = 0

    add = 0

    box = ["+","-","="]

    unit_item={"錢":"元","個":"階"}

    words = []

    temp_name = [] ##暫存名稱

    main = False  ##判斷主角

    temp_unit = []##暫存單位


    if unit in unit_item:

        if unit_item[unit] in d2 and unit not in d2:
        
            unit = unit_item[unit]   ##把單位轉換 ex : 錢轉為元，個轉為階


    final_num = 0


    for i in range(len(d2[unit][2])):

        prev = d2[unit][2][i]  ##單位目前位置

        prev = d1[prev][1]  ##前一個位置(數量)

        for j in prev:
            words.append(j)
    
    sentense = []

    for i in d2:
        sentense.append(i)




################################找出主角######################################################

    for n in words: 

        temp_unit = []

        print(1,sentense)

        if main == False:  

            for x in sentense:   ##從這句話的詞彙中，找出主事者

#####################+-=不為空值，表示x為主事者接受者##########################################
                
                if d2[x][1][0]!="none" and x not in temp_name:   

                    
                    temp_name.append(x)

                    for i in d2[x][0]:
                        
                       # if d1[i][0] ==unit:
                        temp_unit.append(i)

####################如果找到一個主事者，+-=數量大於1，表示為主角###########################################                   

                    if len(d2[x][1])>1 and main!=True and len(temp_unit)>1:  

                        

                        print(2,"主角",x)

                        name=x

                        main = True

                        break

        elif main==True:
            break

    if name not in d2:

        name = temp_name[0]

##############################從主事者往下對應數字########################################
    
    for i in range(len(d2[name][1])):

        opr = d2[name][1][i]

        if opr=="=":
            total.append(d2[name][3][i])
        elif opr=="+":
            sum_+=(d2[name][3][i])
        elif opr=="-":
            sum_-=(d2[name][3][i])
    

    
    
    if len(total)==0:
        total.append(0)

##############################依照變數做計算########################################


##    if unit=="層" or unit=="樓":
##        for i in total:
##            final_num-=i
##        print(i)
##        print(sum_)
##        final_num-=sum_
##        print(final_num)
##        return final_num

    if is_plus==False:   ##如果是從比較中去找出數值，找出全體總和

        
        
        if  len(total)!=0:
            
            if "=" in d2:
                p = d2["="][0][0]
                s = d1[p][1][0]
                total.append(int(d1[s][0]))
                final_num = total[0]+(sum_)+total[0]
##        else:
##            
##            final_num = total
            
        return final_num
    
    

    if is_minus==True :   ##用問題中的數字去扣

        if quan!= 0:
            total[0] += sum_
            
            if total[0]<0:
                final_num = quan+total[0]
            else:
                final_num = quan-total[0]
                
        elif len(total)>1:
            a = total[0]
            b = total[1]
            final_num = abs(a-b)
        elif len(total)==1:
            a = total[0]
            b = sum_
            final_num = abs(a-b)

    

    elif is_minus==True and quan==0:

        
##        if len(total)==0:
##            total.append(0)
        total[0] -= sum_
        final_num = abs(total[0])

        
        
    elif is_reverse==True:
        if sum_!= 0 :
            total[0] -= sum_
            final_num = abs(total[0])
            
        elif sum_==0:
            units = d2[unit][2]
            for i in units:
                pos = i
                back = d1[pos][1][0]
                if int(d1[back][0]) not in total:
                    total.append(int(d1[back][0]))
            for i in total:
                final_num = abs(final_num+i)
        

    elif is_differ==True and len(total)>1:  ##相差

        
        

        a = total[0]
        b = total[1]

        if a>b:
            final_num = a-b
        else:
            final_num = b-a

         

         
    else:
        
        
        if len(total)>1:
            print("好幾個=")
            if is_minus==True:
                a = total[1]
                b = total[0]
                if a>b:
                    
                    final_num = a-b
                else:
                    final_num = b-a
            else:
                
                for i in range(len(total)):
                    
                    final_num+=total[i]

                

            #final_num+=sum_
        else:
            print("依照原始數量跟加減幅度做計算")
            if len(total)==0:
                total.append(0)
            for i in total:
                
                final_num+=i
            if quan!=0:
                final_num+=quan
        final_num = final_num+sum_

    print("初始值:",total)
    print("增加幅度:",sum_)
    
    
    return abs(final_num)
    

def question11(name,places,unit,d1,d2,d3,quan):     ##如果問題中，包含,兩個發生地,單位。題目類型:總和

    ##例子 : 
    ##安安從家裡經過早餐店到學校，要走92公尺，早餐店到學校距離36公尺。
    ##安安從家裡走到早餐店，要走幾公尺？
    
    print("題型 : 11.問題中，包含兩個發生地")
    #print()

    global final_num,sum_,total
    
    opr = ""  
    sum_ = 0  ##總和(原始)。當有=時，則指定值給sum_
    add = 0   ##數值(sum)增加的幅度
    total = []  ## 最後輸出的總和
    opr1 = ""
    opr2 = ""
    box = ["+","-","="]
    unit_item={"錢":"元"}

    final_num = 0 ##最後的結果



    place1 = places[0] #第一個發生地名稱
    place2 = places[1] #第二個發生地名稱

    if place1 not in d2 or place2 not in d2:  ##如果有一個發生地不在d2中，則直接用question5解

        return question5(unit,d1,d2,[],quan)

    pos1 = d2[place1][0]  #第一個發生地位置
    pos2 = d2[place2][0]  #第二個發生地位置

    same = []  ##重複的位置


##############先找出是否有重複的位置##################################
    
    for i in pos2:

        if i in pos1:

            same.append(i)   ##如果有重複位置，則存入


##############由第一個發生地往前找##################################  

    for i in d2[place1][2]:  

        x = d1[i][1][0]  ##第一個發生地的前一個位置


######如果上一個位置不為+-=，則表示前面可能還有發生地，不做下面判斷#######

        if d1[x][0] not in ["+","-","="]:  
            
            continue
        
        pos = d1[i][2]   ##第一個發生地的下一個位置


##############如果第一個發生地下一個位置為第二個發生地所在位置，繼續向下找數字##############
        
        for j in pos:  

            if j in d2[place2][2]:  ###如果第一個發生地下一個位置為第二個發生地所在位置

                next_pos = d1[j][2][0]   ##下一個位置

                
##################如果直接找出數字，則當作答案，return出來######################
                
                if d1[next_pos][0].isdigit():   
                    final_num = int(d1[next_pos][0])
                
                    return final_num
                elif d1[next_pos][0]=="距離":   ##如果找出距離這個詞，則繼續向下
                    next_pos = d1[next_pos][2][0]   ##下一個位置
                    if d1[next_pos][0].isdigit():   ##如果找出數字，則當作答案
                        final_num = int(d1[next_pos][0])
                        return final_num

########如果第一個發生地的下一個位置不為第二個發生地所在位置，繼續往下判斷是否有#################

            elif j not in d2[place2][2]:  

                next_pos = d1[j][2][0]   ##下一個位置
                
########################繼續向下找是否有第二發生地之位置##########################################
                while next_pos!="none":  

                    if next_pos in d2[place2][2]:  ##如果第一個發生地下一個位置為第二個發生地所在位置，繼續向下

                        next_pos = d1[next_pos][2][0]   ##下一個位置

                        if d1[next_pos][0].isdigit():   ##如果找出數字，則當作答案
                            final_num = int(d1[next_pos][0])
                        
                            return final_num
                        elif d1[next_pos][0]=="距離":   ##如果找出距離這個詞，則繼續向下
                            next_pos = d1[next_pos][2][0]   ##下一個位置
                            if d1[next_pos][0].isdigit():   ##如果找出數字，則當作答案
                                final_num = int(d1[next_pos][0])
                                return final_num

                    next_pos = d1[next_pos][2][0]   ##下一個位置



#######################如果有重複位置，要做減法#############################################
                    
    if len(same)>0:  


        if name!="":  ##如果有主事者，則從主事者那邊向下延伸

            pos = d2[name][0]  ##主事者最底層位置

            minus = False  ##預設減法為false

            for i in range(len(pos)):

                if pos[i] in pos1 or pos[i] in pos2:   ##主事者位置有在發生地出現的位置才計算

                    opr = d2[name][1][i]
                    add = d2[name][3][i]

                    if opr=="=":   ##如果為"="

                        if minus == False:

                            total.append(add)
                        elif minus==True:

                            sum_-=add
                            
                            minus = False

                        if pos[i] in same:  ##如果遇到重複，則下次計算是做減法

                            minus = True
                        
                    elif opr in ["+","-"]:

                        if opr=="+":

                            sum_+=add
                        else:
                            sum_-=add

##################如果沒有重複位置，則不會特別減法##################################

    else:   

        if name!="":  ##如果有主事者，則從主事者那邊向下延伸

            pos = d2[name][0]

            

            for i in range(len(pos)):

                if pos[i] in pos1 or pos[i] in pos2:   ##主事者位置有在發生地出現的位置才計算

                    opr = d2[name][1][i]
                    add = d2[name][3][i]

                    if opr=="=":   ##如果為"="

                        total.append(add)

                        
                        
                    elif opr in ["+","-"]:

                        if opr=="+":

                            sum_+=add
                        else:
                            sum_-=add


###################################算出答案##############################################        

    for i in total:

        final_num+=i
    final_num+=sum_
    
    
    return final_num

    
def question12(name,item,unit,d1,d2):  ##是非題

    
    print("題型 : 12.可不可以")

    ##遊覽車有45個座位，現在有29個小朋友。可以一次載完嗎？

    global final_num,sum_,total

    opr = ""
    add = 0

    output = ""##輸出答案


#################################找出主角###################################

    if name  == "":
    
        for i in d2:

            print(i,d2[i][1])

            if len(d2[i][1])>1 and d2[i][1][0]!="none":

                name = i

                
                break
                
#################################找出數字和運算符號###################################
            
    for i in range(len(d2[name][1])):

        opr = d2[name][1][i]

        add = d2[name][3][i]
        
        if opr =="=":
            total.append(add)
        elif opr =="+":
            sum_+=add
        else:
            sum_-=add

    for i in total:
        final_num = abs(final_num-i)

    final_num+=sum_

    if final_num>=0:
        output ="可以"
    else:
        output ="不可以"

        
    return output

    
