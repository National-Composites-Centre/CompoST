
import numpy as np
from numpy.linalg import norm
import math
import CompositeStandard as cs

import sys, inspect


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
    forRemove = ["batch",
                 "database",
                 "defects"
                 "length",
                 "mappedProperties",
                 "mappedRequirements"
                 "memberName",
                 "name",
                 "source",
                 "splineType",
                 "status",
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
                if S in strin:
                    if strin[S] == None:
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
            
    elif type(strin) in ac:
        #If object, turn dictionary, pass back in
        ds = strin.__dict__
        strin,delete = rs(ds)

    return(strin,delete)




#test remove_specific
from jsonic import serialize, deserialize
#with open("D:\\CompoST\Test_clean.json","r") as X:
with open("D:\\CAD_library_sampling\\TestCad_SmartDFM\\X\\x_test_136_layup.json","r") as X:
    json_str= X.read()

    D = deserialize(json_str,string_input=True)

    print("from here on")
    j,delete = rs(D)
    print("FINAL")
    print(j)

    json_str = serialize(j, string_output = True)
    json_str = clean_json(json_str)

    #save as file
    with open('Test_clean.json', 'w') as out_file:
        out_file.write(json_str)


#TEST
'''
with open("D:\\CAD_library_sampling\\TestCad_SmartDFM\\X\\x_test_128.txt","r") as X:
    jstr = str(X.read())
    #print(jstr)
    clean_json(jstr)

'''