import numpy as np
from numpy.linalg import norm
from numpy import (array, dot, arccos, clip)
import CompoST.CompositeStandard as cs

import inspect
import copy

def clean_json(strin):
    #This function creates spaces between objects, to make the JSON file more human readable
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



def findDupID(loc_obj,temp,dup):
    #acceptable list names
    #TODO share the list between two functions, and how do these get updated? -- possibly currently missing some specific point/spline usage
    list_names = ["subComponents","defects","tolerances","nodes","points","meshElements","splineRelimitation","material","axisSystem","manufMethod","initialDrapePoint"]

    #recursively looks through object



    #if ID is specified

    if loc_obj.ID != None:

        #if ID already exists in temp, duplicate was found
        if loc_obj.ID in temp:
            #if ID already in dup add counter
            if loc_obj.ID in dup[:,0]:
                for i in range(0,np.size(dup,0)):
                    if loc_obj.ID == dup[i,0]:
                        dup[i,1] = dup[i,1] + 1
            #if ID not in dup, add new row
            else:
                dup = np.concatenate((dup,np.asarray([[loc_obj.ID,2]])),axis = 0)
        #if ID doesnt exist in TEMP, add it, and look inside
        else:
            temp.append(loc_obj.ID)

    #always look through children, regardless whether this had ID    
        

    for any_atr in dir(loc_obj):
        if any_atr in list_names:
            new_obj = getattr(loc_obj,any_atr)
            if new_obj != None:
                if type(new_obj) == list:
                    for o in new_obj:
                        temp, dup = findDupID(o,temp,dup)
                else:
                    #accounts for when not a list but child object is the next level
                    temp, dup = findDupID(new_obj,temp,dup)
            

    return(temp,dup)

def reLinkRec(D,o,f,i,nestS,nestN,NS_c,NN_c,ITE,build_list):
    #acceptable list names
    #TODO share the list between two functions, and how do these get updated?
    list_names = ["subComponents","defects","tolerances","nodes","points","meshElements","splineRelimitation","material","axisSystem","manufMethod","initialDrapePoint"]

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

                #The build code-lines are cumbersome, and should be replaced by object referencing eventually TODO

                buildF = "D"
                for ii, st in enumerate(nestS):
                    if nestN[ii] == 999:
                        #No number if object instead of list is part of the chain
                        buildF += "."+st
                    else:
                        buildF += "."+st +"["+str(nestN[ii])+"]"

                buildF += " = D"
                for ii, st in enumerate(NS_c):
                    if NN_c[ii] == 999:
                        #No number if object instead of list is part of the chain
                        buildF += "."+st
                    else:
                        buildF += "."+st +"["+str(NN_c[ii])+"]"      
                
                build_list.append(buildF)  

                f = f - 1

                                
        #move to other lists
        else:
            for any_atr in dir(o):
                #if next object has any accepted list nested
                if any_atr in list_names:
                    new_obj = getattr(o,any_atr)
                    if new_obj != None:
                        if type(new_obj) == list:
                            for ii, oo in enumerate(new_obj):
                                #objects within are also run-through
                                nestS.append(any_atr)
                                nestN.append(ii)

                                ITE = ITE + 1

                                D,f,nestS,nestN,NS_c,NN_c, build_list = reLinkRec(D,oo,f,i,nestS,nestN,NS_c,NN_c,ITE,build_list)
                                nestN = nestN[:-1]
                                nestS = nestS[:-1]
                        else:

                            nestS.append(any_atr)
                            nestN.append(999)

                            ITE = ITE + 1

                            D,f,nestS,nestN,NS_c,NN_c, build_list = reLinkRec(D,new_obj,f,i,nestS,nestN,NS_c,NN_c,ITE,build_list)
                            nestN = nestN[:-1]
                            nestS = nestS[:-1]
    
    return(D,f,nestS,nestN,NS_c,NN_c,build_list)

def reLink(D):
    #This function is to be used following deserialization. It translates objects with same ID into the same object. 
    #This compensates for serialization in JSON losing object links in Python.
    #This prevenets one copy of object from accidentally being edited without the details propagating to all it's other instances.

    temp = []
    #first number of dup array is ID, second is number of copies

    #relevant lists 
    #TODO add to changes required when major new developments are added
    #It is key to include all lists that require re-linking between each other.
    reLists = [D.allComposite,D.allGeometry,D.allDefects,D.allTolerances,D.allMaterials]
    reSTR = ["allComposite","allGeometry","allDefects","allTolerances","allMaterials","allManufMethods","allSimulations"]

    #find duplicate 
    dup = np.asarray([[0,0]])
    for RL in reLists:
        if RL != None:
            for o in RL:
                temp, dup = findDupID(o,temp,dup)

    #now iterate to find the objects and re-write with copy

    build_list = []
    for count, i in enumerate(dup[:,0]):
        f = dup[count,1]

        #nested strings
        nestS = []
        #nested object position
        nestN = []
        #object string nest for copy
        NS_c = []
        #object number nest for copy
        NN_c = []

        #Go through all known groups of objects that could be shared and contain IDs 
        for iii, RL in enumerate(reLists):
            if RL != None:
                for ii, o in enumerate(RL):
                    nestS.append(reSTR[iii])
                    nestN.append(ii)
                    D,f,nestS,nestN,NS_c,NN_c, build_list = reLinkRec(D,o,f,i,nestS,nestN,NS_c,NN_c,0,build_list)
                    nestN = nestN[:-1]
                    nestS = nestS[:-1]


    #TODO replace the build function with simple object=object... it should work as long as that all linked objects are being linked to same main one
    for BLT in build_list:
        #print(BLT)
        exec(BLT)

    return(D)
