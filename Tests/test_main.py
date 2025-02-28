import unittest
import CompoST.CompositeStandard as cs
import datetime

#Tests don't come with pip installed repository

#create an example file with 


def create_example():
    #create an example file with various different objects, sharing IDs
    #this has to be crated from scratch as this test script should work with any version, hence old files will not do

    #This deals with currently standardised/fixed objects, all non-core objects are to be added as they become fixed

    #MainFile
    D = cs.CompositeDB()
    D.fileMetadata.author = "Marvin"
    D.fileMetadata.cadFile = "no_file.CATPart"
    D.fileMetadata.lastModified = str(datetime.datetime)
    D.fileMetadata.lastModifiedBy = "Hall9000"

    #Instantiate lists
    D.allComposite = []
    D.allGeometry = []
    D.allSimulations = []
    D.allStages = []
    D.allTolerances = []
    D.allMaterials = []
    D.allDefects = []
    
    p0 = cs.Point(x=0,y=0,z=0,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(p0)

    p1 = cs.Point(x=0,y=0,z=10,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(p1)

    p2 = cs.Point(x=0,y=10,z=10,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(p2)

    p3 = cs.Point(x=0,y=10,z=0,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(p3)

    l = cs.Line(points=[p0,p1],length=10,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(l)

    l2 = cs.Line(IDs=[p2.ID,p3.ID],length=10,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(l2)

    me1 = cs.MeshElement(nodes=[p1,p2,p3,p0],ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(me1)

    #this one doesnt have all children stored in AllGeo
    #(1 mesh element with refs, 1 with half refs, 1 with no refs)
    AM = cs.AreaMesh(meshElements=[me1,
                                   cs.MeshElement(nodes=[p0,p1,cs.Point(x=10,y=0,z=10),cs.Point(x=10,y=0,z=0)]),
                                   cs.MeshElement(nodes=[cs.Point(x=10,y=0,z=10),cs.Point(x=10,y=0,z=0),cs.Point(x=20,y=0,z=0),cs.Point(x=20,y=0,z=10)])
                                                            ],ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(AM)

    #the z should be auto calculated, but x,y are perpendicular so should not need re-calcs
    AX = cs.AxisSystem(o_pt=p2,x_pt=p3,y_pt=cs.Point(x=15,y=0,z=5),ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(AX)

    sp = cs.Spline(points=[p1,cs.Point(x=0,y=10,z=0),cs.Point(x=0,y=0,z=-10),cs.Point(x=0,y=-10,z=-2),cs.Point(x=0,y=-10,z=2)],breaks=[3],ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allGeometry.append(sp)

    mat = cs.Material(E1=66,E2=55,v12=0.3,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allMaterials.append(mat)

    mat2 = cs.Material(E1=999,E2=55,v12=0.15,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allMaterials.append(mat2)

    #piece 
    #check the ID of this is adjusted in the sequence==>ply ==> piece depth
    pc = cs.Piece(material=mat,splineRelimitation=sp,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allComposite.append(pc)

    #ply consisting of 3 separate pieces
    pl = cs.Ply(material=mat2,subComponents=[pc,cs.Piece(),cs.Piece()],orientation=60,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allComposite.append(pl)

    #TODO #here add cla, take effective properties to sequence below
    #sequence that uses ply above with ID, and bunch of other plies
    sq = cs.Sequence(material=mat,axisSystemID=AX.ID,subComponents=[pl,cs.Ply(orientation=39,material=mat2,ID=D.fileMetadata.maxID+1),
                                                                       cs.Ply(orientation=33,material=mat2,ID=D.fileMetadata.maxID+2),
                                                                       cs.Ply(orientation=31,material=mat2,ID=D.fileMetadata.maxID+3)],
                                                                       ID=D.fileMetadata.maxID+4)
    D.fileMetadata.maxID += 4
    D.allComposite.append(sq)


    #append different tolerances and differnt number of defects on plies, pieces, sequences

    #TOLERANCES
    #Tolerance on area, defined by spline
    tl = cs.WrinkleTolerance(maxX=10,maxY=20,axisSystemID=AX.ID,maxAmplitude=30,splineRelimitation=sp,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allTolerances.append(tl)

    #Tolerance to object
    tl2= cs.FibreOrientationTolerance(max_avDiffToNominal=10,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allTolerances.append(tl2)
    pc.tolerances = [tl2]

    #Tolerance with bespoke area
    tl3 = cs.DelaminationTolerance(maxX=10,maxY=11,maxArea=100,splineRelimitation=cs.Spline(points=[cs.Point(x=0,y=2,z=3),
                                                                                                    cs.Point(x=0,y=22,z=3),
                                                                                                    cs.Point(x=0,y=2,z=22)]),ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allTolerances.append(tl3)

    #applied on whole part for lack of other definitions
    tl4 = cs.BoundaryTolerance(maxAllowedDev=3,maxAV=1.5,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allTolerances.append(tl4) 

    #TODO here we add various simulatins


    #Observing defects

    #Create a stage for defects
    stg = cs.Stage(memberName="scanning",stageID=len(D.allStages)+1,source=cs.SourceSystem(softwareName="harvest"))
    D.allStages.append(stg)
    ln = stg.stageID

    w = cs.Wrinkle(area=30,ID=D.fileMetadata.maxID+1,stageID=ln)
    D.fileMetadata.maxID += 1
    D.allDefects.append(w)
    pc.defects = [w]

    #second defect for the same piece
    fo = cs.FibreOrientations(averageOrientation=30,avDiffToNominal=30,ID=D.fileMetadata.maxID+1,stageID=ln)
    D.fileMetadata.maxID += 1
    D.allDefects.append(fo)
    pc.defects = [fo]

    #defect with dedicated area
    dl = cs.Delamination(area=35,splineRelimitation=sp,ID=D.fileMetadata.maxID+1,stageID=ln)
    D.fileMetadata.maxID += 1
    D.allDefects.append(dl)
    
    #Defect applied on whole part for lack of definition
    bd = cs.BoundaryDeviation(avDeviation=13,ID=D.fileMetadata.maxID+1,stageID=ln)
    D.fileMetadata.maxID += 1
    D.allDefects.append(bd)




    #To verify 
    #Verify once manually, from then on, verify automatically 
    #^^i.e. edit one of pair, and check both changed after serialization when edited


    #TODO 
    #cs.EngEdgeOfPart
    #cs.SolidComponent
    #cs.CompositeComponent (to nest file)
    #effective properties == with a simulation stage?
    #cs.UnclassifiedDefect

    return(D)

D = create_example()
cs.Save(D,"TEST_Compost","C:\\temp")