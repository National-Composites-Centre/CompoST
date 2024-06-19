import json

with open("Laminate_Definition_Complete.json") as fl:
    all = json.load(fl)

#print(all)
    
print(list(all))

#print(all["Author"])

#print(all["RootElements"])
#print(list(all["Materials"]))
row1 = list(all["Materials"][0])
#print(row1)
#print(list(row1[0]["additionalProperties"]["Manufacturer"]))

#print(list(all["Materials"]))

print(list(all["RootElements"][0]))

#print(list(all["RootElements"]))

print(all["RootElements"][0]["mappedRequirements"])

print(all["RootElements"][0]["stageIDs"])

print(list(all["RootElements"][0]["sequences"][0]))

print((all["RootElements"][0]["sequences"][0]["sequences"]))

print((all["RootElements"][0]["sequences"][0]["ID"]))

print((all["RootElements"][0]["sequences"][0]["name"]))

print(list(all["RootElements"][0]["sequences"][0]["plies"][0]))

print(list(all["RootElements"][0]["sequences"][0]["plies"][0]["pieces"][0]))

print((all["RootElements"][0]["sequences"][0]["plies"][0]["pieces"][0]['ID']))

print(list(all["RootElements"][0]["sequences"][0]["plies"][0]["pieces"][0]['geometry'][0]))

#print((all["RootElements"][0]["sequences"][0]["plies"][0]["pieces"][0]['geometry'][0]['ElementNodeIndices']))

#elements_ = (all["RootElements"][0]["sequences"][0]["plies"][0]["pieces"][0]['geometry'][0]['ElementNodeIndices'])
sequences = (all["RootElements"][0]["sequences"])

'''
import win32com.client.dynamic
import numpy as np
import win32com.client.dynamic
import os
import statistics

CATIA = win32com.client.Dispatch("CATIA.Application")
#record deletion of product....
documents1 = CATIA.Documents
partDocument1 = documents1.Add("Part")
part1 = partDocument1.Part
#Shape factory provides generating of shapes
ShFactory = part1.HybridShapeFactory
# Starting new body (geometrical set) in part1
bodies1 = part1.HybridBodies
# Adding new body to part1
body1 = bodies1.Add()
# Naming new body as "wireframe"
body1.Name="XXX"



bodyF = bodies1.Add()
bodyF.Name= "piece_"+str("XXXX") 
'''

print("______________STARTING HERE_________________")
'''
kek = ""
def take_appart(something,lvl):
    #input something has to be a list
    try:

        for g in something:

            lx = list(g)
            print("LVL " + str(lvl))
            print(list(g))

            try:
                for str_obj in lx:
                    print(str_obj)
                    lvl = lvl + 1
                    kek = str(str_obj)
                    lvl = take_appart(g[str(str_obj)],lvl)
                    lvl = lvl - 1
            except:
                print(kek+" is not an object,")
                lvl = lvl -1
        
    except:
        print("g is not an object,")
    
    return(lvl)

take_appart(sequences,0)
'''


kek = ""
def take_appart(something,lvl):
    #input something has to be a list

    if type(something) is object:
        print("OBJ")
        for g in something:

            lx = list(g)
            print("LVL " + str(lvl))
            print(list(g))

            for str_obj in lx:
                #print(str_obj)
                lvl = lvl + 1
                kek = str(str_obj)
                lvl = take_appart(g[str(str_obj)],lvl)
                lvl = lvl - 1

    elif type(something) is list:
        print("LIST")
        
        for str_obj in something:
            #print(str_obj)
            lvl = lvl + 1
            kek = str(str_obj)
            lvl = take_appart(str_obj,lvl)
            lvl = lvl - 1

    elif type(something) is dict:
        print("DICT")
        

        lx = list(something)
        print("LVL " + str(lvl))
        print(list(something))

        for str_obj in lx:
            #print(str_obj)
            lvl = lvl + 1
            kek = str(str_obj)
            lvl = take_appart(something[str(str_obj)],lvl)
            lvl = lvl - 1

    else:
        print("something is "+str(type(something)))

    
    return(lvl)

take_appart(sequences,0)



'''
for ii, g in enumerate(sequences):
    #print(e)
    # Adding new body to part1
    #body1 = bodies1.Add()
    #bodyF.Add(body1)
    # Naming new body as "wireframe"
    #body1.Name= "X"+str(ii) 


    elements_ = all["RootElements"][0]["sequences"][ii]["plies"][0]["pieces"][0]['geometry'][0]['ElementNodeIndices']
    print(ii)
    for i,e in enumerate(elements_):

        
        ccoo = all["RootElements"][0]["sequences"][ii]["plies"][0]["pieces"][0]['geometry'][0]['NodeCoords'][e[0]]
        point=ShFactory.AddNewPointCoord(ccoo[0],ccoo[1],ccoo[2])
        body1.AppendHybridShape(point) 
        ref1 = part1.CreateReferenceFromObject(point)

        ccoo = all["RootElements"][0]["sequences"][ii]["plies"][0]["pieces"][0]['geometry'][0]['NodeCoords'][e[1]]
        point=ShFactory.AddNewPointCoord(ccoo[0],ccoo[1],ccoo[2])
        body1.AppendHybridShape(point) 
        ref2 = part1.CreateReferenceFromObject(point)

        ccoo = all["RootElements"][0]["sequences"][ii]["plies"][0]["pieces"][0]['geometry'][0]['NodeCoords'][e[2]]
        point=ShFactory.AddNewPointCoord(ccoo[0],ccoo[1],ccoo[2])
        body1.AppendHybridShape(point)  
        ref3 = part1.CreateReferenceFromObject(point)

        l1 = ShFactory.AddNewLinePtPt(ref1, ref2)
        body1.AppendHybridShape(l1)
        r4 = part1.CreateReferenceFromObject(l1)
        l1 = ShFactory.AddNewLinePtPt(ref2, ref3)
        body1.AppendHybridShape(l1)
        r5 = part1.CreateReferenceFromObject(l1)
        l1 = ShFactory.AddNewLinePtPt(ref3, ref1)
        body1.AppendHybridShape(l1)
        r6 = part1.CreateReferenceFromObject(l1)

        fll = ShFactory.AddNewFill()
        fll.AddBound(r4)
        fll.AddBound(r5)
        fll.AddBound(r6)
        fll.Continuity = 1
        fll.Detection = 2
        fll.AdvancedTolerantMode = 2
        body1.AppendHybridShape(fll)
        
'''

    
nodes_up = []

#print((all["RootElements"][0]["sequences"][0]["plies"][0]["pieces"][0]['geometry'][0]['NodeCoords'][56]))

#node_c = (all["RootElements"][0]["sequences"][0]["plies"][0]["pieces"][0]['geometry'][0]['NodeCoords'])


