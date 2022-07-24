f = open('project3/word.txt','r',encoding='utf-8')

line = f.readlines()

init_list = []  ##語意網路需要使用的list，包含1.名稱，2.位置，3.前一個或多個元素位置，4.後一個或多個元素位置

temp_list=[]  ##暫存list(讀取用)

##讀取問題標籤
q1 = line[0].split()   ##問題標籤(名稱)
q2 = line[1].split()   ##問題標籤(種類)
##讀取問題標籤



add = 0
sum_ = 0

d1 = {} ##建立字典，作為索引用，例如:輸入"a1"，可以取得a1這個位置的名稱，以及前面元素位置及後面元素位置
d2 = {} ##建立另一個字典，輸入名稱，找出名稱在那些句子存在
d3 = {} ##輸入第幾句，取得裡面的文字

index = [] ##建立索引list，存放存在的位置 ex:a0,a1,a2...
names = [] ##存入詞彙

clause = [["a",[],[]],["b",[],[]],["c",[],[]],["d",[],[]],["e",[],[]],["f",[],[]],["g",[],[]]] ##將文字跟數字區隔





for i in range(2,len(line),4):   ##讀取語句標籤

    temp_list=[]

    name = line[i].replace("\n","")  ##暫存標籤名稱
    addr = line[i+1].replace("\n","") ##暫存標籤位置
    
    pre = line[i+2].split()  ##暫存這個標籤的前一個或多個位置
    nex = line[i+3].split()  ##暫存這個標籤的後一個或多個位置

    temp_list.append(name)
    temp_list.append(addr)
    temp_list.append(pre)
    temp_list.append(nex)
    
    init_list.append(temp_list)   ##把暫存的list存到之後處理會用到的list中



    
for i in init_list:  ##建立字典d1，index存入位置，存入詞彙名稱

    is_same = 0
    x = [i[0],i[2],i[3]]  ##暫存名稱，前面元素位置，後面元素位置
    d1[i[1]]=x   ##指定字典d1的索引值。i[1]為標籤的位置
    index.append(i[1])  ##存入位置

    
    for j in names:
        
        if i[0]==j[0]:
            is_same=1

    if is_same==0:
        names.append([i[0],[],[]])



index.sort()  ##將索引list排序(由a到g)





for i in init_list:
    
    for j in names:   ##1.名稱，2.位置，3.前一個或多個元素位置，4.後一個或多個元素位置

        if i[0]==j[0]:  ##如果名稱相同，進行下一步處理

            
            
            if i[2][0]=="none":  ##如果是主事者接受者(前一個元素為none)

                

                for k in i[3]:

                    s = k ##位置的第一個字，即為第幾句(a~g)
                    j[1].append(s[0])  ##存入第幾句


                for x in range(len(init_list)):##+-=
                    pos = init_list[x][1]  ##位置
                    if pos in i[3]:
                        j[2].append(init_list[x][0])
                
                    
            else:  ##如果不是主事者接受者
                s = i[1]  ##位置的第一個字，即為第幾句(a~g)
                j[1].append(s[0])   ##存入第幾句

for i in names:
    if len(i[2])==0:
        i[2].append("none")
    d2[i[0]]=[i[1],i[2]]   ##指定字典d2的值(第幾句 ex:a,b,c....)
        

for i in names:

    clau = i[1]
    
    for j in clau:

        for k in clause:

            if j==k[0]:  ##如果句子一樣

                try:
                    if int(i[0])%1==0:
                        k[2].append(i[0])  ##clause加入這個詞
                except:
                    k[1].append(i[0])  ##clause加入這個詞


for i in clause:

    d3[i[0]]=[i[1],i[2]]
    
            




 
   
def solve(q1,q2,d1,d2,d3):  ##解題

    name = ""  ##人名
    item = ""  ##物品
    add=0  ##數量
    unit="" ##單位
    sum_ = 0
    total = 0

    pos = [] ##人物在第幾句存在
    opr = []  ##+-=
    

    for i in q2:
        if i=="主事者":
            
            name=q1[q2.index(i)]
            

        elif i=="物品":
            item=q1[q2.index(i)]

        elif i=="單位":
            unit=q1[q2.index(i)]

    people = d2[name][0]
    for i in range(len(people)):
        if people[i] in d2[item][0]: ##如果人出現的位置跟物品位置一樣
            opr = d2[name][1][i]
            add = d3[people[i]][1][0]  ##從d3去找出這句話相對應的數字
            add = int(add)
            if opr =="=":  ##如果運算符號為=，則預設總和為此數字
                total=add
            elif opr =="+":  ##如果運算符號為+，則sum增加
                
                sum_+=add
                
            elif  opr =="-":  ##如果運算符號為-，則sum增加
               
                sum_-=add
    

    total+=add
    
        
    


    
    
    print("解題")
    print(q1)
    print("人名:",name,"物品:",item,"單位:",unit)
    print("答案:",total,unit)
    



        

print("資料結構(一開始讀進來的格式)=>list : 1.詞彙2.位置3.前面位置(如果沒有則為none)4.後面位置(如果沒有則為none)")
for x in init_list:  ##資料結構(list)
    print(x)
##
##print()
##print("索引(位置)")
##for i in index:
##    print(i)
##
print()


print()
print("dictionary1 : 1.名稱，2.前面元素位置(如果沒有則為none)，3.後面元素位置(如果沒有則為none)")
for i in index:
    print(i,'=>',d1[i])   ##印出索引，以及索引對印到的值(1.名稱，2.前一個或多個元素位置，3.後一個或多個元素位置)

print()   
print("dictionary2 : 1.顯示第幾句(a-g)，2.顯示+-=(如果為主事者接受者)")
for i in d2:
    print(i,'=>',d2[i])
print()
print("dictionary3 : 句子:a-g ")
for i in d3:
    print(i,'=>',d3[i])




#solve(q1,q2,d1,d2,d3)



                
            














