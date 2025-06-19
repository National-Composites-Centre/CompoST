from pydantic import BaseModel, Field, ConfigDict, ValidationError, SerializeAsAny
import numpy as np
from typing import List, Optional, Tuple, Union, Annotated, Any
from datetime import date, time, timedelta

#specifically for axis calcualtions
from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm
import math
import os

from enum import Enum
from pydantic import BaseModel, Field, TypeAdapter
from pydantic.config import ConfigDict

import json
from jsonic import serialize, deserialize

import CompoST.Utilities

#### VERSION 0.8.4 ####
#https://github.com/National-Composites-Centre/CompoST

#documentation link in the repository Readme


def get_author():
    #This function helps assign author on CompositeDB creation, making sure errors in os.getlogin() will be handled
    try:
        author = os.getlogin()
    except: 
        author = ""
    return(author)

class CompositeDBItem(BaseModel):

    memberName: Optional[str] = Field(default = None)
    additionalParameters: Optional[dict] = Field(default = None) #this is bespoke dictionary created by user, it should not hold copies of ID carrying CompoST objects.
    stageID: Optional[int] = Field(default = None) #stage where this object was generated / re-generated
    deactivate_stageID: Optional[int] = Field(default = None) #this object is not relevant after this stage - either it has been superceeded or it's purpose was fullfilled
    active: Optional[bool] = Field(default = True) #This can be turned to False to indicate this object does not represent the latest iteration of the part
    ID: Optional[int] = Field(default = None)

class SimulationData(CompositeDBItem):

    sourceSystem: Optional['SourceSystem'] = Field(default = None) #software or tool used for simulation 
    cadFile: Optional[str] = Field(default=None) #path and filename of reference CAD 
    toolCadFile: Optional[str] = Field(default=None) # path to tool cad, if different from the above
    axisSystemID: Optional[int] = Field(default=None) #reference to axis system ID

class GeometricElement(CompositeDBItem):
    #child of Geometric elements
    source: Optional[object] = Field(default = None)
    refFile: Optional[str] = Field(default = None)
    
class Point(GeometricElement):
    
    x: float = Field(default = 0)
    y: float = Field(default = 0)
    z: float = Field(default = 0)

class AxisSystem(GeometricElement):
    #Axis system on default uses root axis system values

    #Axes are defined as points - the vector/axis itself is 
    #the point minus the origin.

    #User should only specify origin point and two of the axes.
    #Third axis is calculated when this object is initialized 
    #and re-calculated when any parameter is changed.

    #The user should not be manually editing z_pt. 

    #point of origin
    o_pt: Point = Field(default=Point(x=0,y=0,z=0))

    #point that defines x axis - origin_pt ==> x_pt is the axis as vector
    x_pt: Point = Field(default=Point(x=1,y=0,z=0))

    #point that defines y axis - origin_pt ==> y_pt is the axic as vector
    y_pt: Point = Field(default=Point(x=0,y=1,z=0))

    #When x_pt and y_pt are not perpendicular y_pt.z is adjusted so that they are.
    #Point that defines z axis - origin_pt ==> z_pt is the axis as vector.
    z_pt: Point = Field(default=Point(x=0,y=0,z=1))


    def __init__(self, **data):
        super().__init__(**data)
        self._calculateZ()

    #pass local data to recalcZ method for new z_pt 
    def _calculateZ(self) -> None:
        self.__dict__['z_pt'], self.__dict__['y_pt'] = self.recalcZ(self)
        return(self)   

    @staticmethod
    def recalcZ(self):
        #calculate the third vector and find the point to store
        u = np.asarray([self.x_pt.x-self.o_pt.x, self.x_pt.y-self.o_pt.y, self.x_pt.z-self.o_pt.z])
        v = np.asarray([self.y_pt.x-self.o_pt.x, self.y_pt.y-self.o_pt.y, self.y_pt.z-self.o_pt.z])
        #cross product
        cp = np.cross(u,v)
        #point rather than vector
        ptZ = cp +  np.asarray([self.o_pt.x, self.o_pt.y, self.o_pt.z])
        z_pt = Point(x=ptZ[0],y=ptZ[1],z=ptZ[2])

        #check whether the secondary (y_pt) vector is perpendicular to primary (x_pt)
        c = dot(u,v)/norm(u)/norm(v)
        angle = arccos(clip(c,-1,1))*180/math.pi
        #check if right angle - giving small margin in case rounding errors on input
        if (angle < 89.9) or (angle >  90.1):
            cp2 = np.cross(u,cp)
            ptY = cp2 +  np.asarray([self.o_pt.x, self.o_pt.y, self.o_pt.z])
            y_pt = Point(x=ptY[0],y=ptY[1],z=ptY[2])

            print("Secondary axix of an AxisSystem is not perpendicular to primary, this is automatically recalculated.")

            #TEMP CHECK 
            #c = dot(u,cp2)/norm(u)/norm(cp2)
            #angle = arccos(clip(c,-1,1))*180/math.pi
            #print("fixed angle is: ",angle)
        else:
            #keep y_pt the same
            y_pt = self.y_pt

        return(z_pt,y_pt)

    def __setattr__(self, name: str, value: Any) -> None:
        # Override setattr - responds to changes in o_pt, x_pt, or y_pt
        super().__setattr__(name, value)
        if name in {"o_pt", "x_pt", "y_pt"}:
            self._calculateZ()
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class FileMetadata(BaseModel):
    #the below might be housed in specialized class
    lastModified: Optional[str] = Field(default=None) #Automatically refresh on save - string for json parsing
    lastModifiedBy: Optional[str] = Field(default=None) #String name
    author: Optional[str] = Field(default=None) #String Name
    version: Optional[str] = Field(default= "0.8.4") #eg. - type is stirng now, for lack of better options
    layupDefinitionVersion: Optional[str] = Field(default=None)

    #external file references - separate class?
    cadFile: Optional[str] = Field(default=None)
    cadFilePath: Optional[str] = Field(default=None)

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
    allDefects: Optional[list['Defect']] = Field(default=None) # list of all defects
    allTolerances: Optional[list['Tolerance']] = Field(default = None) # list of all Tolerances
    fileMetadata: FileMetadata = Field(default = FileMetadata(author=get_author())) #list of all "axisSystems" objects = exhaustive list
    allSimulations: Optional[list['SimulationData']] = Field(default = None) #List of simulation data objects
    allManufMethod: Optional[list['ManufMethod']] = Field(default=None) #List of all manufacturing methods involved

class ManufMethod(CompositeDBItem):

    #parent method for various manufacturing techniques that require bespoke information storage
    axisSystemID: Optional[int] = Field(None) #ID reference to allAxis systems 

class FilamentWinding(ManufMethod):

    #each ply will likely need separate one of these object, but sometimes object can be reused

    windingPath: Optional['Spline'] = Field(default=None) #Spline defined path of material, as wound on the mandrel
    meridian: Optional['Spline'] = Field(default=None) #2D cross section of PV (assumes axisymmetry) - if this shape is revolved it should produce the PV shape.
    steppedMandre: Optional['Spline'] = Field(default=None) # for first ply this is equivalent to meridian, then stepped mandrel defines the outermost shape including built-up material
    xMin: Optional[float] = Field(default=None) #relevant for hoop layers, defines start point for winding (minimum x-direction limit)
    xMax: Optional[float] = Field(default=None) #relevant for hoop layers, defines start point for winding (maximum x-direction limit)
    layerType: Optional[str] = Field(default=None) #hoop/helical-geodesic/helical-nongeodesic  TODO make this into prescribed keywords and force selection of those only

class CompositeElement(CompositeDBItem):

    #TODO below list of all possible compositeComponents, would be neater if instead of listing them it could be of "CompositeComponent children"
    subComponents: Optional[List[Union['CompositeComponent', 'Sequence', 'Ply', 'Piece', 'SolidComponent']]] = Field(None) # list of subComponents -- all belong to the CompositeElement family
    requirements: Optional[list] = Field(None) # list of objects - "Requirement"
    defects: Optional[list['Defect']] = Field(None) #list of objects - "defects"
    tolerances: Optional[list['Tolerance']] = Field(None)
    axisSystemID: Optional[int] = Field(None) #ID reference to allAxis systems 
    referencedBy: Optional[list[int]] = Field(None) # list of int>
    manufMethod: Optional['ManufMethod'] = Field(None) #manufacturing method relevant to this object

class Piece(CompositeElement):
    #CompositeElement type object
    #In practical terms this is section of ply layed-up in one (particulartly relevant for AFP or similar)
    splineRelimitation: Optional['Spline'] = Field(None) #points collected as spline for relimitation
    material: Optional['Material'] = Field(None) #material from allMaterials

class Ply(CompositeElement):
    #CompositeElement type object
    material: Optional['Material'] = Field(None) #material from allMaterials
    orientation: Optional[float] = Field(None)
    splineRelimitation: Optional['Spline'] = Field(None) #points collected as spline for relimitation
    splineRelimitationRef: Optional[int] = Field(None) #same as above but stored as reference to ID

class Sequence(CompositeElement):
    #CompositeElement type object
    orientations: Optional[list[float]] = Field(None) #used for minimalistic definition where ply-objects are avoided
    materials: Optional[list['Material']] = Field(None) #listof materials - must be same lenght as orientations
    material: Optional['Material'] = Field(None) #material from allMaterials
    splineRelimitation: Optional['Spline'] = Field(None) #points collected as spline for relimitation
    splineRelimitationRef: Optional[int] = Field(None) #same as above but stored as reference to ID
    EP: Optional['EffectiveProperties'] = Field(None) #Effective properties : if the component has uniform effective properties

class CompositeComponent(CompositeElement):
    #this object is mostly going to be used for bonding co-curing etc where multiple distinct composite components
    #can be defined
    integratedComponent: Optional[list[CompositeDB]] = Field(None) #allows for nesting another comonent within this file
    EP: Optional['EffectiveProperties'] = Field(None) #Effective properties : if the component has uniform effective properties

class SourceSystem(BaseModel):
    softwareName: Optional[str] = Field(None)
    version: Optional[str] = Field(None)
    link: Optional[str] = Field(None) #link to GitHub, docs... where appropriate 

class SolidComponent(CompositeElement):
    #had shapes - for example when including 3D core
    cadFile: Optional[str] = Field(None)
    sourceSystem: Optional[SourceSystem] = Field(None) #SourceSystem object

class EngEdgeOfPart(CompositeElement):
    #Engineering edge of part
    #This allows for overriding definition of where the part is to be trimmed at the end of manufacture
    
    splineRelimitation: Optional['Spline'] = Field(None) #points collected as spline for relimitation
    source: Optional['SourceSystem'] = Field(None) #defines which CAD system was this created in
    referenceGeometry: Optional[str] = Field(None) #reference to the name (string) of geometry that defines this in source CAD system

class Material(CompositeDBItem):
    #this will be extended over time - it should allow for storing different level materials (i.e. stack vs ply)
    E1: Optional[float] = Field(None)
    E2: Optional[float] = Field(None)
    G12: Optional[float] = Field(None)
    G23: Optional[float] = Field(None)
    v12: Optional[float] = Field(None)
    infoSource: Optional[str] = Field(None)
    density: Optional[float] = Field(None)

    #add other related values
    #might need sublacces for materials as relevant for manuf. processes. 

class GenericMaterial(Material):
    
    K1: Optional[float] = Field(None) #principle direction permeability
    K2: Optional[float] = Field(None) #transverse permeability
    K3: Optional[float] = Field(None) #out-of-plane permeability
    thickness: Optional[float] = Field(None)
    Vf: Optional[float] = Field(None)

class Tape(Material):
    thickness: Optional[float] = Field(None) # out of plane size

class EffectiveProperties(Material):
    #this object is used for objects that need homogenized material properties

    thickness: Optional[float] = Field(None)
    K1: Optional[float] = Field(None) #principle direction permeability
    K2: Optional[float] = Field(None) #transverse permeability
    K3: Optional[float] = Field(None) #out-of-plane permeability
    Vf: Optional[float] = Field(None) #fibre volume fraction

class Line(GeometricElement):
    #potentially also give options to keep the points directly here in a matrix?

    #Use either IDs or points, not both. IDs recommended if the points 
    # are to be re-used for other geometries.
    points: Optional[list[Point]] = Field(None) 
    IDs: Optional[list[int]] = Field(None)
    lenght: Optional[float] = Field(None) #can be calculated from above, but then can be stored so calcs are not duplicated

class MeshElement(GeometricElement):
    #3 or 4 points, check?
    nodes: list['Point'] = Field(None) # only accept Point classes
    normal: list = Field(None) #x,y,z in the list

class AreaMesh(GeometricElement):
    meshElements: list['MeshElement'] = Field(None) # requires element classes only
    
class Spline(GeometricElement):
    #can either be defined directly here as 3xX array, or can be defined as a list of points (not both)
    splineType: Optional[int] = Field(None)  #types of splines based on OCC line types?
    points: Optional[list['Point']] = Field(None) #list of point objects
    length: Optional[float] = Field(None)
    breaks: Optional[list[int]] = Field(None) #This allows for identification of points which break continuity of spline (i.e. spline is ended and new started - used for sharp corners)

class Defect(CompositeDBItem):
    
    location: Optional[list[float]] = Field(None) #x,y,z location
    effMaterial: Optional['EffectiveProperties'] = Field(None) #adjusted material class saved in materials
    status: Optional[bool] = Field(None) # None = not evaluated, True = defect outside of tolerance, False = deviation but fits within tolerance
    axisSystemID: Optional[int] = Field(None) #reference to axis system stored in Geo. elements
    file: Optional[str] = Field(None) #reference to dedicated defect file
    splineRelimitation: Optional['Spline'] = Field(None)

class Wrinkle(Defect):

    area: Optional[float] = Field(None)
    aspectRatio: Optional[float] = Field(None) #typically size_x/size_y
    maxRoC: Optional[float] = Field(None)
    size_x: Optional[float] = Field(None) #primary direction size, according to referenced axisSystemID, or global axis if local not available
    size_y: Optional[float] = Field(None)
    meshRef: Optional[int] = Field(None) # area covered by defect expressed in mesh format (area or volume)
    amplitude: Optional[float] = Field(None) #out of plane maxiumum size of the defect

class FibreOrientations(Defect):

    lines: Optional[list['Line']] = Field(None) #list of lines collected to denote orientations map
    orientations: Optional[list[float]] = Field(None) #list of floats corresponding to the "lines" list 
    averageOrientation: Optional[float] = Field(None) #average of "orientations", does not account for varying lenght of lines
    avDeviation: Optional[list[float]] = Field(None) #average deviation to nominal


class Tolerance(CompositeDBItem):
    #inherited by all specific tolerance definition objects
    splineRelimitation: Optional['Spline'] = Field(None) #area for this definition

class WrinkleTolerance(Tolerance):

    maxY: Optional[float] = Field(None)
    maxX: Optional[float] = Field(None)
    axisSystemID: Optional[int] = Field(None)
    maxArea: Optional[float] = Field(None)
    maxRoC: Optional[float] = Field(None) #maximum rate of change, in radians
    maxSkew: Optional[float] = Field(None) #TODO define
    maxAmplitude: Optional[float] = Field(None)

class Delamination(Defect):

    #Delamination occurs between two layers/plies, the convention is to append it to the one that is in the tool direction.

    size_x: Optional[float] = Field(None) #length in x axis direction
    size_y: Optional[float] = Field(None) #length in y axis direction
    area: Optional[float] = Field(None)  

class DelaminationTolerance(Tolerance):

    maxX: Optional[float] = Field(None) #maximum length in x axis direction
    maxY: Optional[float] = Field(None) #maximum length in y axis direction
    maxArea: Optional[float] = Field(None) #maximume allowed area per defect

class BoundaryDeviation(Defect):
    
    maxDeviation: Optional[float] = Field(None) #maximum distance of a measured point from intended boundary
    avDeviation: Optional[float] = Field(None) #average deviation along the boundary

class BoundaryTolerance(Tolerance):

    maxAllowedDev: Optional[float] = Field(None) #maximum allowed distance of a measured point from intended boundary
    maxAv: Optional[float] = Field(None) #



class UnclassifiedDefect(Defect):
    #this object is to be used when the defect you are storing does not have dedicated definition
    #use the title field to classify it

    title: Optional[str] = Field(None)

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

class DrapingSimulation(SimulationData):
    #TODO this is to be validated by multiple simulaiton tools working with it

    initialDrapePoint: Optional['Point'] = Field(default=None) #location of first intended contact between ply and tool
    plyID: Optional[int] = Field(default = None) #ply ID - one DrapingSimulation object for each ply
    newOrientation: Optional[float] = Field(default = None) #Prescribed orientation of ply at the initial draping location
    maxShearAngle: Optional[float] = Field(default = None) #maximum predicted shear angle in the full ply
    acceptedDarts: Optional[list['Line']] = Field(default = None) #list of lines indicating accepted locations for darts
    drapeDirections: Optional[list['Spline']] = Field(default = None) #list of splines indicating draping directions, only one spline is to be provided in the list if only initial draping direction matters
    drapedMesh: Optional['AreaMesh'] = Field(default = None) #Mesh object - corresponds to mesh after draping
    mappedShearAngles: Optional[list[float]] = Field(default = None) # list ordered accroding to dreapedMesh that it its mapped against

class Stage(BaseModel):

    stageID: Optional[int] = Field(default=None) 
    memberName: Optional[str] = Field(default=None)
    source: Optional[SourceSystem] = Field(None) #SourceSystem
    processRef: Optional[str] = Field(None) #this is reference to process that corresponds to current stage (e.g. instruction sheet pdf location)
    stageParameters: Optional[dict] = Field (None) #dictionary of bespoke Stage related parameters

# class PlyScan(Stage):

#     #the name is a placeholder
#     machine: Optional[str] = Field(default=None) #designation name of the machine underataking scanning 
#     binderActivated: Optional[str] = Field(default=None) # bool

class FibreOrientationTolerance(Tolerance):
    
    max_avDeviation: Optional[float] = Field(default=None) #average difference to intended ply orientation based off all sampling points within relimitation

class Zone(CompositeDBItem):

    #TODO develop based on use-case requirements

    splineRelimitation: Optional['Spline'] = Field(None) #area for this definition
    splineRelimitationRef: Optional[int] = Field(None) # same as above, but referenced using 'ID'


def generate_json_schema(file_name:str):
    with open(file_name, 'w') as f:
        f.write(json.dumps(CompositeDB.model_json_schema(), indent=4))

def Open(file,path=""):
    #Opens a CompoST file, currently the CompoST file should be same version as this script

    with open(path+"\\"+file+".json","r") as in_file:
        json_str= in_file.read()

    #turn file into workable classes
    D = deserialize(json_str,string_input=True)

    #re-link objects
    D = CompoST.Utilities.reLink(D)

    return(D)

def Save(CompositeDB,file,path="",overwrite=False):

    #Edit metadata to record last user/editor
    try:
        CompositeDB.fileMetadata.lastModifiedBy = os.getlogin()
    except:
        print("failed to access username for logging in fileMetadata from the OS")

    #turn data back to JSON
    json_str = serialize(CompositeDB, string_output = True)

    #clean the JSON
    json_str = CompoST.Utilities.clean_json(json_str)

    #save as file
    #TODO interactive option for overwrite?
    if overwrite == True:

        print("saving as:",path+"\\"+file+".json")
        with open(path+"\\"+file+".json", 'w') as out_file:
            out_file.write(json_str)

    else:
        if os.path.exists(path+"\\"+file+".json"):
            print("file: "+path+"\\"+file+".json"+" already exists. To overwrite it, set overwrite parameter to True")

        else:
            print("saving as:",path+"\\"+file+".json")
            with open(path+"\\"+file+".json", 'w') as out_file:
                out_file.write(json_str)

    return()

#generate_json_schema('compostSchema.json')



