from pydantic import BaseModel, Field, ConfigDict, ValidationError, SerializeAsAny
import numpy as np
from typing import Optional, Tuple, Union, Annotated
from datetime import date, time, timedelta


from enum import Enum
from pydantic import BaseModel, Field, TypeAdapter
from pydantic.config import ConfigDict

import json
from jsonic import serialize, deserialize

#### VERSION 1.0 ####

#potentially replace by JSON parser for Pydantic
#However, for now largely bespoke scripted breakdown for good control of format


#"CompositeElement" type objects include: Piece, Ply, SolidComponent, CompositeComponent

#anything that can be referenced must have an ID, this ID should correspond to the order in which it is stored. 
#Therefore for now ID is not directly specified but is inherent in the list it belongs to)

#This class is required to store nested classes in JSON (for some reason)
class VsBaseErrorSchema(BaseModel):
    """Base for all error responses. Represents a JSON serializable version of VsBaseError"""
    detail: str = Field(title="Human readable string describing the error message")
    context: SerializeAsAny[BaseModel] | dict | None = Field(title="Context about the error")
    error_code: str = Field(title="Combination of the service name & error code")

class Point(BaseModel):
    #value: np.array = Field(np.asarray[0,0,0])
    memberName: Optional[str] = Field() #can point out specific points for reference - group points for unexpected reasons...
    x: float = Field()
    y: float = Field()
    z: float = Field()

class axisSystem(BaseModel):
    #^^ point + 3x vector ==> implement check that the 3 axis are perpendicular to each other

    #numpy array 4:3 --- or the below to break appart

    #point of origin
    pt: object = Field(Point)

    # 1st asxis of axis system (adjusted x) - expressed in global
    v1x: float = Field(default = 1)  
    v1y: float = Field(default = 0)
    v1z: float = Field(default = 0)

    # 1st asxis of axis system (adjusted y) - expressed in global
    v1x: float = Field(default = 0)  
    v1y: float = Field(default = 1)
    v1z: float = Field(default = 0)

    # 1st asxis of axis system (adjusted z) - expressed in global
    v1x: float = Field(default = 0)  
    v1y: float = Field(default = 0)
    v1z: float = Field(default = 1)

    memberName: Optional[str] = Field()


class FileMetadata(BaseModel):
    #the below might be housed in specialized class
    lastModified: Optional[date] = Field(None) #Automatically refresh on save?
    lastModifiedBy: Optional[str] = Field(None) #String name
    author: Optional[str] = Field(None) #String Name
    version: Optional[str] = Field(None) #eg. 1.0.3 - type is stirng now, for lack of better options

class CompositeDB(BaseModel):

    #model_config = ConfigDict(title='Main')
    name: str = Field("test")

    rootElements: Optional[list] = Field(None)   #List of "CompositeElement" type objects
    allEvents: Optional[list] = Field(None) #List of "events" objects - all = exhaustive list
    allGeometry: Optional[list] = Field(None) # list of "GeometricElement" objects - all = exhaustive list
    allStages: Optional[list] = Field(None) #??? manuf process - all = exhaustive list
    allMaterials: Optional[list] = Field(None) #List of "Material" objects - all = exhaustive list
    allAxisSystems: Optional[list] = Field([axisSystem])
    fileMetadata: object = Field(FileMetadata()) #list of all "axisSystems" objects = exhaustive list


class CompositeElement(BaseModel):
    database: Optional[object] = Field #can there be multiple of these dbItems in one file? if so ==> list???
    mappedProperties: Optional[list] = Field(None) #list of objects - various allowed: Component, Sequence, Ply, Piece
    mappedRequirements: Optional[list] = Field(None) # list of objects - "Requirement"
    defects: Optional[list] = Field(None) #list of objects - "defects"
    axisSystemIDs: Optional[list] = Field(None) #list of "axisSystems" references, numbered according to allAxisSystems
    referencedBy: Optional[list] = Field(None) # list of int?

    
class compositeDBItem(BaseModel):
    #ID: int = Field(None) #implied for now
    name: Optional[str] = Field(None)
    additionalParameters: Optional[dict] = Field(None) # dictionary of floats
    additionalProperties: Optional[dict] = Field(None) # dictionary of strings
    stageIDs: Optional[list] = Field(None) #list of references to stages


class Piece(BaseModel):
    #CompositeElement type object
    #In practical terms this is section of ply layed-up in one (particulartly relevant for AFP or similar)
    placementRosette: int = Field() # reference number to rosette in allAxisSystems
    batch: int = Field() #?
    memberName: Optional[str] = Field() #?

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field() #compositeElement class in here

class Ply(BaseModel):
    #CompositeElement type object
    cutPieces: Optional[list] = Field() #list of Piece objects
    material: Optional[int] = Field() #ref to material in allMaterials
    placementRosette: Optional[int] = Field()
    memberName: Optional[str] = Field() #?
    #ID: int = Field() #implied for now

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field() #compositeElement class in here

class Sequence(BaseModel):
    #CompositeElement type object

    #sequences -- just not for now

    plies: Optional[list] = Field() #list of reference numbers for plies
    components: Optional[list] = Field() #list of reference numbers for "Component" objects
    memberName: Optional[str] = Field() #?

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field() #compositeElement class in here

class CompositeComponent(BaseModel):
    sequence: Optional[list] = Field() # list of int refrences to Sequence type variables
    memberName: Optional[str] = Field() #?

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field() #compositeElement class in here

class SolidComponent(BaseModel):
    memberName: Optional[str] = Field() #?

    #not sure if the below works, test?
    compositeElement: Optional[object] = Field() #compositeElement class in here


class Material(BaseModel):
    memberName: Optional[str] = Field()
    #add other related values

    #might need sublacces for materials as relevant for manuf. processes. 

class geometricElement(BaseModel):
    #child of Geometric elements
    memberName: Optional[str] = Field()
    #source: ???


class Line(BaseModel):
    #potentially also give options to keep the points directly here in a matrix?

    nodeRef: Optional[list] = Field() #list of reference inetegers, linking to points
    memberName: Optional[str] = Field()

'''
class AreaMesh(BaseModel):
    nodeRefs: Optional[np.array] = Field() # numpy array 2 dimensional? list of refernce nodes on each line
    '''
    #

class Spline(BaseModel):
    #can either be defined directly here as 3xX array, or can be defined as a list of points (not both)
    pointRefs: Optional[list] = Field() # list of reference integers
    splineType: Optional[int] = Field()  #types of splines based on OCC line types?
    memberName: Optional[str] = Field()
    points: Optional[list] = Field() #list of point objects







d = CompositeDB()
d.fileMetadata.lastModified = "30/05/2024"

d.name = "new"

# Convert dictionary to JSON string
print(d)
json_str = serialize(d)

# Print the JSON string
print(json_str)

#save as file
with open('Test_CI_dump.json', 'w') as out_file:
     json.dump(json_str, out_file, sort_keys = True, indent = 4,
               ensure_ascii = False)
     
#open file

D = deserialize(json_str)

print(D)

print(D.fileMetadata.lastModified)