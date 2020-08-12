'''
本模块的功能为从树中搜寻频繁项集
author：胡觉文
'''
import fp_growth
import reader

def findPrefixPath(basePat, myHeaderTab):#创建前缀路径
    treeNode = myHeaderTab[basePat][1]
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):#递归功能
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(frozenset(newFreqSet))
        condPattBases = findPrefixPath(basePat, headerTable)
        myCondTree, myHead = fp_growth.createTree(condPattBases, minSup)
        if myHead != None:
            # 用于测试
            #print('conditional tree for:', newFreqSet)
            #myCondTree.disp()
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def fpGrowth(dataSet, minSup):#集成fp功能
    initSet = fp_growth.createInitSet(dataSet)
    myFPtree, myHeaderTab = fp_growth.createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return [freqItems]

if __name__ == '__main__':
    idlist, goodslist, _ = reader.search()
    dataSet = reader.data_handle(idlist, goodslist)
    print(fpGrowth(dataSet,10))