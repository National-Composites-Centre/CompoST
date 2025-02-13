import json
from jsonic import serialize, deserialize

import CompoST.CompositeStandard as cs

def testJSON():
    #TODO make dedicated testing module

    d = cs.CompositeDB()
    d.fileMetadata.lastModified = "23/09/2024"
    d.name = "new"

    # Convert dictionary to JSON string
    #print(d)
    json_str = serialize(d, string_output = True)

    # Print the JSON string
    print(json_str)

    #json_str = cleandict(json_str)

    #save as file
    with open('Test_CI_dump.json', 'w') as out_file:
        out_file.write(json_str)
        #json.dump(json_str, out_file, sort_keys = True,
        #        ensure_ascii = False)
        
    #open file
    with open('Test_CI_dump.json',"r") as in_file:
        json_str= in_file.read()
    
    
    print(json_str)
    D = deserialize(json_str,string_input=True)
    print(D)
    print(D.fileMetadata.lastModified)

testJSON()