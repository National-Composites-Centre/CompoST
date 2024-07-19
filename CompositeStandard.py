from pydantic import BaseModel, Field, ConfigDict, ValidationError, SerializeAsAny
import numpy as np
from typing import Optional, Tuple, Union, Annotated
from datetime import date, time, timedelta


from enum import Enum
from pydantic import BaseModel, Field, TypeAdapter
from pydantic.config import ConfigDict

import json
from jsonic import serialize, deserialize

#### VERSION 0.63 ####
#https://github.com/National-Composites-Centre/CompoST

#potentially replace by JSON parser for Pydantic
#However, for now largely bespoke scripted breakdown for good control of format

#"CompositeElement" type objects include: Piece, Ply, SolidComponent, CompositeComponent

#anything that can be referenced must have an ID, this ID should correspond to the order in which it is stored. 
#Therefore for now ID is not directly specified but is inherent in the list it belongs to)

class GeometricElement(BaseModel):
    #child of Geometric elements
    memberName: Optional[str] = Field(default = None)
    source: Optional[object] = Field(default = None)

class Point(GeometricElement):
    #value: np.array = Field(np.asarray[0,0,0])
    #memberName: Optional[str] = Field(None) #can point out specific points for reference - group points for unexpected reasons...
    x: float = Field(default = 0)
    y: float = Field(default = 0)
    z: float = Field(default = 0)

class AxisSystem(BaseModel):
    #^^ point + 3x vector ==> implement check that the 3 axis are perpendicular to each other

    #Axis system on default uses root axis system values - upon initionation any changes must be applied on all axes

    #point of origin
    pt: Point = Field(default=Point())

    # 1st asxis of axis system (adjusted x) - expressed in global
    v1x: float = Field(default = 1)
    v1y: float = Field(default = 0)
    v1z: float = Field(default = 0)

    # 1st asxis of axis system (adjusted y) - expressed in global
    v2x: float = Field(default = 0)
    v2y: float = Field(default = 1)
    v2z: float = Field(default = 0)

    # 1st asxis of axis system (adjusted z) - expressed in global
    v3x: float = Field(default = 0)
    v3y: float = Field(default = 0)
    v3z: float = Field(default = 1)

    memberName: Optional[str] = Field(default=None)


class FileMetadata(BaseModel):
    #the below might be housed in specialized class
    lastModified: Optional[str] = Field(default=None) #Automatically refresh on save - string for json parsing
    lastModifiedBy: Optional[str] = Field(default=None) #String name
    author: Optional[str] = Field(default=None) #String Name
    version: Optional[str] = Field(default= "0.63") #eg. - type is stirng now, for lack of better options
    layupDefinitionVersion: Optional[str] = Field(default=None)

    #external file references - separate class?
    cadFile: Optional[str] = Field(default=None)
    cadFilePath: Optional[str] = Field(default=None)

class CompositeDB(BaseModel):

    #model_config = ConfigDict(title='Main')
    name: str = Field(default = "test")

    #All elements and all geometry are all stored here and used elsewhere as refrence
    #Points are stored withing those, as referencing is not efficient

    rootElements: Optional[list['CompositeElement']] = Field(default=None)   #List of "CompositeElement" type objects
    allEvents: Optional[list] = Field(default=None) #List of "events" objects - all = exhaustive list
    allGeometry: Optional[list['GeometricElement']] = Field(default=None) # list of "GeometricElement" objects - all = exhaustive list
    allStages: Optional[list] = Field(default=None) #??? manuf process - all = exhaustive list
    allMaterials: Optional[list['Material']] = Field(default=None) #List of "Material" objects - all = exhaustive list
    allAxisSystems: Optional[dict[str, 'AxisSystem']] = Field(default= AxisSystem(pt=Point()))
    fileMetadata: FileMetadata = Field(default = FileMetadata()) #list of all "axisSystems" objects = exhaustive list


class CompositeElement(BaseModel):
    database: Optional[object] = Field(None) #can there be multiple of these dbItems in one file? if so ==> list???
    subComponent: Optional[list['CompositeElement']] = Field(None) # list of subComponents -- all belong to the CompositeElement family
    mappedProperties: Optional[list['CompositeComponent|Sequence|Ply|Piece']] = Field(None) #list of objects - various allowed: Component, Sequence, Ply, Piece
    mappedRequirements: Optional[list] = Field(None) # list of objects - "Requirement"
    defects: Optional[list] = Field(None) #list of objects - "defects"
    axisSystemIDs: Optional[list[str]] = Field(None) #list of "axisSystems" references, numbered according to allAxisSystems
    referencedBy: Optional[list[int]] = Field(None) # list of int>
    status: Optional[str] = Field(None) #TODO

#IS THIS EVEN NEDED TODO
class CompositeDBItem(BaseModel):
    #ID: int = Field(None) #implied for now
    name: Optional[str]
    additionalParameters: Optional[dict] # dictionary of floats
    additionalProperties: Optional[dict] # dictionary of strings
    stageIDs: Optional[list] #list of references to stages


class Piece(CompositeElement):
    #CompositeElement type object
    #In practical terms this is section of ply layed-up in one (particulartly relevant for AFP or similar)
    placementRosette: int = Field(None) # reference number to rosette in allAxisSystems
    batch: int = Field(None) #?
    memberName: Optional[str] = Field(None) #?
    splineRelimitation: Optional[object] = Field(None) #spline object

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field(None) #compositeElement class in here

class Ply(CompositeElement):
    #CompositeElement type object
    cutPieces: Optional[list] = Field(None) #list of Piece objects
    material: Optional[str] = Field(None) #ref to material in allMaterials
    placementRosette: Optional[int] = Field(None)
    memberName: Optional[str] = Field(None) #?
    orientation: Optional[float] = Field(None)
    #ID: int = Field() #implied for now

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field(None) #compositeElement class in here

class Sequence(CompositeElement):
    #CompositeElement type object

    #sequences -- just not for now

    plies: Optional[list] = Field([]) #list of reference numbers for plies
    components: Optional[list] = Field([]) #list of reference numbers for "Component" objects
    memberName: Optional[str] = Field(None) #?

    #not sure if the below works, test?
    compositeElement: Optional[CompositeElement] = Field(None) #compositeElement class in here

class CompositeComponent(CompositeElement):
    sequence: Optional[list['Sequence']] = Field() # list of int refrences to Sequence type variables
    memberName: Optional[str] = Field() #?

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field() #compositeElement class in here

class SolidComponent(CompositeElement):
    memberName: Optional[str] = Field() #?

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field() #compositeElement class in here


class Material(BaseModel):
    #this will be extended over time - it should allow for storing different level materials (i.e. stack vs ply)
    materialName: Optional[str] = Field(None)
    E1: Optional[float] = Field(None)
    E2: Optional[float] = Field(None)
    G12: Optional[float] = Field(None)
    G23: Optional[float] = Field(None)
    v12: Optional[float] = Field(None)
    infoSource: Optional[str] = Field(None)
    thickness: Optional[float] = Field(None)
    density: Optional[float] = Field(None)
    permeability: Optional[float] = Field(None)
    type: Optional[str] = Field(None) #TODO eventually limit to list! , CFRP/GFRP/kevlar - set keywords...

    #add other related values

    #might need sublacces for materials as relevant for manuf. processes. 


class SourceSystem(BaseModel):
    softwareName: Optional[str] = Field()


class Line(GeometricElement):
    #potentially also give options to keep the points directly here in a matrix?

    nodeRef: Optional[list[int]] = Field() #list of reference inetegers, linking to points

#TODO not used rn, not sure if individual elements need element (Area/volume mesh instead)
class Element(BaseModel):
    #3 or 4 points, check?
    nodes: list['Point'] = Field(None) # only accept Point classes

class AreaMesh(GeometricElement):
    elements: list['Element'] = Field(None) # requires element classes only
    
class Spline(GeometricElement):
    #can either be defined directly here as 3xX array, or can be defined as a list of points (not both)
    splineType: Optional[int] = Field(None)  #types of splines based on OCC line types?
    points: Optional[list['Point']] = Field(None) #list of point objects
    length: Optional[float] = Field(None)


#unused rn
def cleandict(d):
    if isinstance(d, dict):
        return {k: cleandict(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [cleandict(v) for v in d]
    else:
        return d


def generate_json_schema(file_name:str):
    with open(file_name, 'w') as f:
        f.write(json.dumps(CompositeDB.model_json_schema(), indent=4))

generate_json_schema('compostSchema.json')




def test():

    d = CompositeDB()
    d.fileMetadata.lastModified = "10/07/2024"
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

#test()