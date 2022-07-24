##把指定的類別移到前面

##move_item(list2,list3):  ##物品移動到數量前面
##move_adj(list2,list3): ##"特點","發生地","時間點"移動到數量前面

## 邏輯 :

## 根據

import random

def move_item(list2,list3):  ##物品移動到數量前面

    if "物品" not in list3: ##這句話如果沒物品，直接return
        return list2,list3

    t2 = ""

    t3 = ""
    
    #word = ''

    ids = []  ##存物品id，亂碼

    check_id = [] ##符合條件之清單

    #moved = [] ##存已經放過的物品

    pos = len(list2)-1 ##list2最後一個位置



######################在ids存放各個詞的亂數id#################
    for i in range(pos+1):  

        id_ = random.randint(0,100)

        while id_ in ids:

            id_ = random.randint(0,100)

        ids.append(id_)

    
        
##########如果這個id對到的詞，標籤為物品，check_id存入此id######
    for i in range(len(ids)): 

        if list3[i] in ["物品"]:

            
            check_id.append(ids[i])

    print("p3_move")
    print(list2)
    print(list3)
    print(ids)
    print(check_id)

    #[5, '顆', '蘋果']  list2
    #['數量', '單位', '物品']  list3
    #[10, 3, 100]  ids_
    #[100]  check_id


    length = len(list2)-1 ##找到list2的最後一個位置(長度1)


    

    
    if list3[length]!="單位" :  

##########   從check_id裡面開始，把物品移動到數量前面   ######
        
        for i in range(len(check_id)):

            

            item = check_id[i]  #亂數id

            pos = ids.index(item)  ##根據check_id位置，對應到亂數id位置

            t2 = list2[pos] ##根據id位置，找到list2元素
            t3 = list3[pos] ##根據id位置，找到list3元素
            #t4 = ids[pos] 

            
##########   從list2、list3往前推，如果找到標籤為數量的，則把物品放到數量前面  ######
            
            for j in range(pos,-1,-1):

                if list3[j]=="數量":

                    del list3[pos]
                    del list2[pos]
                    del ids[pos]

                    list2.insert(j,t2)
                    list3.insert(j,t3)
                    ids.insert(j,pos)

                    
                    break
                    
                  

      
    
    return list2,list3



def move_adj(list2,list3):

    t2 = ""

    t3 = ""
    
    #word = ''

    #adj_list = []

    ids = []  ##存物品id，亂碼

    check_id = [] ##符合條件之清單

    #moved = [] ##存已經放過的物品

    pos = len(list2)-1 ##list2最後一個位置


    for i in range(0,pos+1):

        id_ = random.randint(0,100)

        while id_ in ids:

            id_ = random.randint(0,100)

        ids.append(id_)

    for i in range(len(ids)):

        if list3[i] in ["特點","發生地","時間點"]:

            
            check_id.append(ids[i])
    

    for i in range(len(check_id)):

        

        it = check_id[i]

        pos = ids.index(it)

        t2 = list2[pos]
        t3 = list3[pos]
        #t4 = ids[pos]
        
        
        if '單位' in list3[:pos] and '單位' in list3[pos+1:]:  ##如果這個特點，前後有單位，則不移動位置
            
            continue
        else:   ##否則將位置移動到數量前面
            for j in range(pos,-1,-1):
    
                if list3[j]=="數量":
                    
                    del list3[pos]
                    del list2[pos]
                    del ids[pos]
                    
                    
                    list2.insert(j,t2)
                    list3.insert(j,t3)
                    ids.insert(j,pos)
                    
                    
                    
                    break
        
    

    return list2,list3
