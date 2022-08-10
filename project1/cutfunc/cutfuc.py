import jieba

jieba.del_word("朵玫瑰")
jieba.del_word("白玫瑰")
jieba.del_word("白巧克力")
jieba.del_word("紫蝴蝶")
jieba.del_word("朵花")
jieba.del_word("泰比")
jieba.del_word("漁船")
jieba.del_word("黑熊")
jieba.del_word("白熊")
jieba.del_word("最少")
jieba.del_word("封信")
jieba.del_word("船長")
jieba.del_word("很多")
jieba.del_word("很少")
jieba.del_word("一本")
jieba.del_word("一件")
jieba.del_word("一箱")
jieba.del_word("一天")
jieba.del_word("往前")
jieba.del_word("二天")
jieba.del_word("三天")
jieba.del_word("一碗")
jieba.del_word("小黑")
jieba.del_word("一杯")
jieba.del_word("第一")
jieba.del_word("一綑")
jieba.del_word("一捆")
jieba.del_word("第二")
jieba.del_word("一枝")
jieba.del_word("手上")
jieba.del_word("十位")
jieba.del_word("一盒")
jieba.del_word("一支")
jieba.del_word("一次")
jieba.del_word("第三")
jieba.del_word("一排")
jieba.del_word("他家")
jieba.del_word("第一天")
jieba.del_word("一位")
jieba.del_word("二位")
jieba.del_word("三位")
jieba.del_word("第二天")
jieba.del_word("第三天")
jieba.del_word("小猴子")
jieba.del_word("安排")

jieba.load_userdict("project1/cutfunc/and.txt")
jieba.load_userdict("project1/cutfunc/range.txt")
jieba.load_userdict("project1/cutfunc/adj.txt")
jieba.load_userdict("project1/cutfunc/adv.txt")
jieba.load_userdict("project1/cutfunc/equal.txt")
jieba.load_userdict("project1/cutfunc/n.txt")
jieba.load_userdict("project1/cutfunc/v.txt")
jieba.load_userdict("project1/cutfunc/pv.txt")
jieba.load_userdict("project1/cutfunc/nv.txt")
jieba.load_userdict("project1/cutfunc/place.txt")
jieba.load_userdict("project1/cutfunc/time.txt")
jieba.load_userdict("project1/cutfunc/u.txt")
jieba.load_userdict("project1/cutfunc/int.txt")
jieba.load_userdict("project1/cutfunc/name.txt")
jieba.load_userdict("project1/cutfunc/special.txt")
jieba.load_userdict("project1/cutfunc/total.txt")
jieba.load_userdict("project1/cutfunc/passive.txt")
jieba.load_userdict("project1/cutfunc/bigger.txt")
jieba.load_userdict("project1/cutfunc/smaller.txt")
jieba.load_userdict("project1/cutfunc/after.txt")
jieba.load_userdict("project1/cutfunc/before.txt")
jieba.load_userdict("project1/cutfunc/p.txt")
jieba.load_userdict("project1/cutfunc/add.txt")
jieba.load_userdict("project1/cutfunc/sub.txt")
jieba.load_userdict("project1/cutfunc/unit.txt")
import jieba.posseg as psg

def cutall(text):
    #詞性標註
    seg = psg.cut(text,HMM=False)
    #將詞性標註結果打印出來
    result = list()
    lastresult = list()
    lastele = ''
    lastname = ''
    for name,ele in seg:
        if(ele == 'eng'):
            ele = 'int'
        if lastele == 'name' and name == '的':
            result.pop()
            name = lastname+name
            ele = 'adj'
        lastele = ele
        lastname = name
        result.append({name:ele})
    return result
