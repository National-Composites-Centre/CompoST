
import numpy as np
from numpy.linalg import norm
import math


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

#TEST
'''
with open("D:\\CAD_library_sampling\\TestCad_SmartDFM\\X\\x_test_128.txt","r") as X:
    jstr = str(X.read())
    #print(jstr)
    clean_json(jstr)

'''