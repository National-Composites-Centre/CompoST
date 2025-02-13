import numpy as np
from numpy.linalg import norm
from numpy import (array, dot, arccos, clip)
import CompoST.CompositeStandard as cs

import inspect
import copy

"""This .py file holds utility scripts not part of the main installation. Either because of level stability or due to minimal utility."""

def rs(strin):
    #this is recursive function that searches through nested classes
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
                #print("deleted through list method")
                tbd.append(i)

        for i in tbd:
            del strin[i]

    #iftuple
    elif type(strin) == tuple:

        if (strin[0] in forRemove) and (strin[1] == None):
            #print("this would be deleted")
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