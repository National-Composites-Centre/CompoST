
import numpy as np
from numpy.linalg import norm
from numpy import (array, dot, arccos, clip)
import math
import CompositeStandard as cs

import sys, inspect
import copy

def clean_json(strin):
    #strin = input json string to clean
    s = strin.replace("{","\n{\n")
    s = s.replace("}","\n}\n")


    tabs = 0
    new_str = ""
    for line in s.split("\n")[:]:
        
        if "}" in line:
            tabs = tabs - 1

        for ii in range(0,tabs):
            new_str += "   "
        new_str += line+"\n"

        if "{" in line:
            tabs = tabs + 1
    #returns a human readable JSON
    return(new_str)

# def make3rdAxis(po,pt1,pt2):
#     #po origin poitn, pt1 point in x, pt2 point in y
#     u = np.asarray([pt1.x-po.x,pt1.y-po.y,pt1.z-po.z])
#     v = np.asarray([pt2.x-po.x,pt2.y-po.y,pt2.z-po.z])
#     c = dot(u,v)/norm(u)/norm(v)
#     angle = arccos(clip(c,-1,1))*180/math.pi
#     print(angle)

po = cs.Point(x=3,y=3,z=3)
px = cs.Point(x=4,y=3,z=3)
py = cs.Point(x=3,y=4,z=6)
axisA = cs.AxisSystem(o_pt =po,x_pt=px,y_pt=py)
axisA.x_pt = cs.Point(x=15,y=3,z=3)
print(axisA.z_pt)
# make3rdAxis(po,px,py)



def rs(strin):
    #this is recursive function that digs through nested classes
    #It identifies classes listed below, and deletes them from dictionaries if their value is None

    #This is so that inheritence can be built into classes, but JSON files are not too bloated.


    delete = False
    ac = []
    for name, obj in inspect.getmembers(cs):
        if inspect.isclass(obj):
            ac.append(obj)  

    #list of all classes that should not be stored if corresponding value is "None"
    #Please keep alphabetic. This list will be growing a lot as the scope of standard expands.

    forRemove = ["additionalParameters","additionalProperties",
                 "batch",
                 "database","defects",
                 "length",
                 "mappedProperties",
                 "mappedRequirements",
                 "memberName",
                 "referencedBy",
                 "source",
                 "splineType",
                 "stageIDs","status",
                 "subComponent"]

    #if list
    if type(strin) == list:
        tbd = []
        for i,O1 in enumerate(strin):
            O1, delete = rs(O1)
            if delete == True:
                print("DELETED THROUGH METHOD 3")
                tbd.append(i)

        for i in tbd:
            del strin[i]

    #iftuple
    elif type(strin) == tuple:

        if (strin[0] in forRemove) and (strin[1] == None):
            print("this would be deleted")
            delete = True

    #if dictionary
    elif type(strin) == dict: 
        #create a list of dict members to delete
        tbd = []
        for S in strin.keys():

            if (S in forRemove):
                
                if (strin[S] == None):
                    #Most common deletion comes from this section
                    tbd.append(S)
                        
            else:
                #discard end values: str
                if type(strin) != str:
                    #discard end values: floats
                    if type(strin[S]) == float:
                        pass
                    elif strin[S] != None:
                        strin[S],delete = rs(strin[S])
                        if delete == True:
                            #rare - if at all possible TODO : check if needed
                            tbd.append(S)

        #remove identified members
        for i in tbd:
            if i in strin:
                del strin[i]

    #!!! this not good, it keeps the format as dictionary when saving!!!    
    elif type(strin) in ac:
        #If object, turn dictionary, pass back in
        ds = strin.__dict__
        strin,delete = rs(ds)
        print("this happens now")

    return(strin,delete)




#test remove_specific
# from jsonic import serialize, deserialize
# #with open("D:\\CompoST\Test_clean.json","r") as X:
# with open("C:\code\CompoST_examples\WO4502_minimized_v067\WO4502_layup.json","r") as X:
#     json_str= X.read()

#     D = deserialize(json_str,string_input=True)

#     print("from here on")
#     j,delete = rs(D)
#     #print("FINAL")
#     #print(j)

#     json_str = serialize(j, string_output = True)
#     json_str = clean_json(json_str)

#     #save as file
#     with open('C:\code\CompoST_examples\WO4502_minimized_v067\Test_clean.json', 'w') as out_file:
#         out_file.write(json_str)


def findDupID(loc_obj,temp,dup):
    #acceptable list names
    list_names = ["subComponents","defects","nodes","points","meshElements"]

    #recursively looks through object

    #if ID is specified
    if loc_obj.ID != None:

        #if ID already exists in temp, duplicate was found
        if loc_obj.ID in temp:
            #if ID already in dup add counter
            if loc_obj.ID in dup[:,0]:
                for i in range(0,np.size(dup,0)):
                    if loc_obj.ID == dup[i,0]:
                        dup[i,1] == dup[i,1] + 1
            #if ID not in dup, add new row
            else:
                dup = np.concatenate((dup,np.asarray([[loc_obj.ID,2]])),axis = 0)
        #if ID doesnt exist in TEMP, add it, and look inside
        else:
            temp.append(loc_obj.ID)

            #specific lists accepted only for housing more nested objects
            for any_atr in dir(loc_obj):
                if any_atr in list_names:
                    new_obj = getattr(loc_obj,any_atr)
                    if new_obj != None:
                        for o in new_obj:
                            temp, dup = findDupID(o,temp,dup)
    #if ID is not specified
    else: 
        
        for any_atr in dir(loc_obj):
            if any_atr in list_names:
                new_obj = getattr(loc_obj,any_atr)
                if new_obj != None:
                    for o in new_obj:
                        temp, dup = findDupID(o,temp,dup)
            
    return(temp,dup)

def reLinkRec(D,o,f,i,nestS,nestN,NS_c,NN_c):
    #acceptable list names
    list_names = ["subComponents","defects","nodes","points","meshElements"]

    #f is the number of copies that still need to be identified
    if f > 0:
        #this is the ID I know is duplicated
        if i == o.ID:
            #if this is the first instance of ID - make a note of object to copy
            if NS_c == []:
                NS_c = copy.deepcopy(nestS)
                NN_c = copy.deepcopy(nestN)
                f = f - 1
            #if object is stored in for_copy this object is than copied into the location of current object - to re link
            else:
                #reconstruct the reference to edit D ####

                buildF = "D"
                for ii, st in enumerate(nestS):
                    buildF += "."+st +"["+str(nestN[ii])+"]"

                buildF += " = D"
                for ii, st in enumerate(NS_c):
                    buildF += "."+st +"["+str(NN_c[ii])+"]"           

                #not the cleanest, but wasn't able to make this work with getattr
                #(feel free to rework)
                print(buildF)     
                exec(buildF)
                f = f - 1
                                
        #move to other lists
        else:
            for any_atr in dir(o):
                #if next object has any accepted list nested
                if any_atr in list_names:
                    new_obj = getattr(o,any_atr)
                    if new_obj != None:
                        for ii, oo in enumerate(new_obj):
                            #objects within are also run-through
                            nestS.append(any_atr)
                            nestN.append(ii)
                            D,f,nestS,nestN,NS_c,NN_c = reLinkRec(D,oo,f,i,nestS,nestN,NS_c,NN_c)
                            nestN = nestN[:-1]
                            nestS = nestS[:-1]

    return(D,f,nestS,nestN,NS_c,NN_c)

def reLink(D):

    #Minimal testing done so far. 

    temp = []
    #first number of dup array is ID, second is number of copies
    dup = np.asarray([[0,0]])
    if D.allComposite != None:
        for o in D.allComposite:
            temp, dup = findDupID(o,temp,dup)
    if D.allGeometry != None:
        for o in D.allGeometry: 
            temp, dup = findDupID(o,temp,dup)
    if D.allDefects != None:
        for o in D.allDefects:
            temp, dup = findDupID(o,temp,dup)
    if D.allTolerances != None:
        for o in D.allTolerance:
            temp, dup = findDupID(o,temp,dup)

    #now iterate to find the objects and re-write with copy

    #nested strings
    nestS = []
    #nested object position
    nestN = []
    #object string nest for copy
    NS_c = []
    #object number nest for copy
    NN_c = []
    
    for count, i in enumerate(dup[:,0]):
        f = dup[count,1]
        #Go through all known groups of objects that could be shared and contain IDs
        #Can definitely be streamlined.
        if D.allComposite != None:
            for ii, o in enumerate(D.allComposite):
                nestS.append("allComposite")
                nestN.append(ii)
                D,f,nestS,nestN,NS_c,NN_c = reLinkRec(D,o,f,i,nestS,nestN,NS_c,NN_c)
                nestN = nestN[:-1]
                nestS = nestS[:-1]
        if D.allGeometry != None:
            for ii, o in enumerate(D.allGeometry): 
                nestS.append("allGeometry")
                nestN.append(ii)
                D,f,nestS,nestN,NS_c,NN_c = reLinkRec(D,o,f,i,nestS,nestN,NS_c,NN_c)
                nestN = nestN[:-1]
                nestS = nestS[:-1]
        if D.allDefects != None:
            for ii, o in enumerate(D.allDefects):
                nestS.append("allDefects")
                nestN.append(ii)
                D,f,nestS,nestN,NS_c,NN_c = reLinkRec(D,o,f,i,nestS,nestN,NS_c,NN_c)
                nestN = nestN[:-1]
                nestS = nestS[:-1]
        if D.allTolerances != None:
            for ii,o in enumerate(D.allTolerance):
                nestS.append("allTolerance")
                nestN.append(ii)
                D,f,nestS,nestN,NS_c,NN_c = reLinkRec(D,o,f,i,nestS,nestN,NS_c,NN_c)
                nestN = nestN[:-1]
                nestS = nestS[:-1]

    return(D)


#TEST
'''
with open("D:\\CAD_library_sampling\\TestCad_SmartDFM\\X\\x_test_128.txt","r") as X:
    jstr = str(X.read())
    #print(jstr)
    clean_json(jstr)

'''