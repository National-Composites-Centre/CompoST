from pydantic import BaseModel, Field, ConfigDict, ValidationError, SerializeAsAny
import numpy as np
from typing import Optional, Tuple, Union, Annotated
from datetime import date, time, timedelta


from enum import Enum
from pydantic import BaseModel, Field, TypeAdapter
from pydantic.config import ConfigDict

import json
from jsonic import serialize, deserialize

#### VERSION 0.67 ####
#https://github.com/National-Composites-Centre/CompoST

#potentially replace by JSON parser for Pydantic
#However, for now largely bespoke scripted breakdown for good control of format

#"CompositeElement" type objects include: Piece, Ply, SolidComponent, CompositeComponent

#anything that can be referenced must have an ID, this ID should correspond to the order in which it is stored. 
#Therefore for now ID is not directly specified but is inherent in the list it belongs to)


#IS THIS EVEN NEDED TODO
class CompositeDBItem(BaseModel):

    memberName: Optional[str] = Field(default = None)
    additionalParameters: Optional[dict] = Field(default = None) # dictionary of floats
    additionalProperties: Optional[dict] = Field(default = None) # dictionary of strings
    stageIDs: Optional[list] = Field(default = None) #list of references to stages
    ID: Optional[int] = Field(default = None)

class GeometricElement(CompositeDBItem):
    #child of Geometric elements
    source: Optional[object] = Field(default = None)
    refFile: Optional[str] = Field(default = None)
    
class Point(GeometricElement):
    #value: np.array = Field(np.asarray[0,0,0])
    #memberName: Optional[str] = Field(None) #can point out specific points for reference - group points for unexpected reasons...
    x: float = Field(default = 0)
    y: float = Field(default = 0)
    z: float = Field(default = 0)

class AxisSystem(GeometricElement):
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

class FileMetadata(BaseModel):
    #the below might be housed in specialized class
    lastModified: Optional[str] = Field(default=None) #Automatically refresh on save - string for json parsing
    lastModifiedBy: Optional[str] = Field(default=None) #String name
    author: Optional[str] = Field(default=None) #String Name
    version: Optional[str] = Field(default= "0.67") #eg. - type is stirng now, for lack of better options
    layupDefinitionVersion: Optional[str] = Field(default=None)

    #external file references - separate class?
    cadFile: Optional[str] = Field(default=None)
    cadFilePath: Optional[str] = Field(default=None)

    #v.064
    maxID: int = Field(default =0)

class CompositeDB(BaseModel):

    #model_config = ConfigDict(title='Main')
    name: str = Field(default = "test")

    #All elements and all geometry are all stored here and used elsewhere as refrence
    #Points are stored withing those, as referencing is not efficient

    allComposite: Optional[list['CompositeElement']] = Field(default=None)   #List of "CompositeElement" type objects
    allEvents: Optional[list] = Field(default=None) #List of "events" objects - all = exhaustive list
    allGeometry: Optional[list['GeometricElement']] = Field(default=None) # list of "GeometricElement" objects - all = exhaustive list
    allStages: Optional[list] = Field(default=None) #??? manuf process - all = exhaustive list
    allMaterials: Optional[list['Material']] = Field(default=None) #List of "Material" objects - all = exhaustive list
    allDefects: Optional[list['Material']] = Field(default=None) # list of all defects
    allTolerances: Optional[list['Tolerance']] = Field(default = None) # list of all Tolerances
    fileMetadata: FileMetadata = Field(default = FileMetadata()) #list of all "axisSystems" objects = exhaustive list

class CompositeElement(CompositeDBItem):
    database: Optional[object] = Field(None) #can there be multiple of these dbItems in one file? if so ==> list???
    subComponents: Optional[list['CompositeElement']] = Field(None) # list of subComponents -- all belong to the CompositeElement family
    mappedProperties: Optional[list['CompositeComponent|Sequence|Ply|Piece']] = Field(None) #list of objects - various allowed: Component, Sequence, Ply, Piece
    mappedRequirements: Optional[list] = Field(None) # list of objects - "Requirement"
    defects: Optional[list] = Field(None) #list of objects - "defects"
    axisSystemID: Optional[int] = Field(None) #ID reference to allAxis systems 
    referencedBy: Optional[list[int]] = Field(None) # list of int>
    status: Optional[str] = Field(None) #TODO

class Piece(CompositeElement):
    #CompositeElement type object
    #In practical terms this is section of ply layed-up in one (particulartly relevant for AFP or similar)
    splineRelimitationRef: Optional[int] = Field(None) #reference to spline object
    material: Optional[str] = Field(None) #ref to material in allMaterials

class Ply(CompositeElement):
    #CompositeElement type object
    material: Optional[str] = Field(None) #ref to material in allMaterials
    orientation: Optional[float] = Field(None)
    splineRelimitationRef: Optional[int] = Field(None) #reference to spline object

class Sequence(CompositeElement):
    #CompositeElement type object
    orientations: Optional[list[float]] = Field(None) #used for minimalistic definition where ply-objects are avoided
    materials: Optional[list['Material']] = Field(None) #listof materials - must be same lenght as orientations
    material: Optional[str] = Field(None) #ref to material in allMaterials
    splineRelimitationRef: Optional[int] = Field(None) #reference to spline object

class CompositeComponent(CompositeElement):
    #this object is mostly going to be used for bonding co-curing etc where multiple distinct composite components
    #can be defined
    integratedComponent: Optional[list[CompositeDB]] = Field(None) #allows for nesting another comonent within this file

class SourceSystem(BaseModel):
    softwareName: Optional[str] = Field(None)
    version: Optional[str] = Field(None)
    link: Optional[str] = Field(None) #link to GitHub, docs... where appropriate 

class SolidComponent(CompositeElement):
    #had shapes - for example when including 3D core
    cadFile: Optional[str] = Field(None)
    sourceSystem: Optional[SourceSystem] = Field(None) #SourceSystem object

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
    permeability_1: Optional[float] = Field(None) #primary direction 
    permeability_2: Optional[float] = Field(None) #secondary direction (in-plane)
    permeability_3: Optional[float] = Field(None) #out-of-plane

    type: Optional[str] = Field(None) #TODO eventually limit to list! , CFRP/GFRP/kevlar - set keywords...

    #add other related values

    #might need sublacces for materials as relevant for manuf. processes. 

class Line(GeometricElement):
    #potentially also give options to keep the points directly here in a matrix?

    #Use either IDs or points, not both. IDs recommended if the points 
    # are to be re-used for other geometries.
    points: Optional[list[Point]] = Field() 
    IDs: Optional[list[int]] = Field

class MeshElement(BaseModel):
    #3 or 4 points, check?
    nodes: list['Point'] = Field(None) # only accept Point classes
    normal: list = Field(None) #x,y,z in the list

class AreaMesh(GeometricElement):
    meshElements: list[MeshElement] = Field(None) # requires element classes only
    
class Spline(GeometricElement):
    #can either be defined directly here as 3xX array, or can be defined as a list of points (not both)
    splineType: Optional[int] = Field(None)  #types of splines based on OCC line types?
    points: Optional[list['Point']] = Field(None) #list of point objects
    length: Optional[float] = Field(None)
    breaks: Optional[list[int]] = Field(None) #This allows for identification of points which break continuity of spline (i.e. spline is ended and new started - used for sharp corners)

class Defect(CompositeDBItem):
    
    map: Optional[CompositeDBItem] = Field(None) #any composite or geometric object
    location: Optional[list[float]] = Field(None) #x,y,z location
    source: Optional[SourceSystem] = Field(None) #SourceSystem
    effMaterial: Optional[Material] = Field(None) #adjusted material class saved in materials
    status: Optional[object] = Field(None) #TODO
    axisSystemID: Optional[int] = Field(None) #reference to axis system stored in Geo. elements

class Wrinkle(Defect):

    area: Optional[float] = Field(None)
    aspectRatio: Optional[float] = Field(None) #typically size_x/size_y
    maxRoC: Optional[float] = Field(None)
    size_x: Optional[float] = Field(None) #primary direction size, according to referenced axisSystemID, or global axis if local not available
    size_y: Optional[float] = Field(None)
    splineRelimitationRef: Optional[int] = Field(None) #points collected as spline relimiting the defect
    meshRef: Optional[int] = Field(None) # area covered by defect expressed in mesh format (area or volume)


def generate_json_schema(file_name:str):
    with open(file_name, 'w') as f:
        f.write(json.dumps(CompositeDB.model_json_schema(), indent=4))


#
##
###
####
#####
#From here onwards the objects are not fully standardised - their architecture and definitions are likely to chane!
#####
####
###
##
#

def Tolerance(CompositeDBItem):
    #inherited by all specific tolerance definition objects

    appliedToIDs: Optional[list[int]] = Field(None)

def WrinkleTolerance(Tolerance):

    maxZ: Optional[float] = Field(None)
    maxY: Optional[float] = Field(None)
    maxX: Optional[float] = Field(None)
    axisSystemID: Optional[int] = Field(None)
    maxArea: Optional[float] = Field(None)
    maxSlope: Optional[float] = Field(None)
    maxSkew: Optional[float] = Field(None) #TODO define








#generate_json_schema('compostSchema.json')




def test():
    #TODO make dedicated testing module

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