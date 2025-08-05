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
    D.allManufMethods = []
    D.allSimulations = []
    
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
    sq = cs.Sequence(material=mat,axisSystem=AX,subComponents=[pl,cs.Ply(orientation=39,material=mat2,ID=D.fileMetadata.maxID+1),
                                                                       cs.Ply(orientation=33,material=mat2,ID=D.fileMetadata.maxID+2),
                                                                       cs.Ply(orientation=31,material=mat2,ID=D.fileMetadata.maxID+3)],
                                                                       ID=D.fileMetadata.maxID+4)
    D.fileMetadata.maxID += 4
    D.allComposite.append(sq)


    #append different tolerances and differnt number of defects on plies, pieces, sequences

    #TOLERANCES
    #Tolerance on area, defined by spline
    tl = cs.WrinkleTolerance(maxX=10,maxY=20,axisSystem=AX,maxAmplitude=30,splineRelimitation=sp,ID=D.fileMetadata.maxID+1)
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

    #Drape simulation #TODO more complex example - includes splines, lines, etc... will need to be added to re-link function
    ds1 = cs.DrapingSimulation(initialDrapePoint=p1,ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allSimulations.append(ds1) 

    #manufMethod -- TODO add meridian and windingPath -- these will need to be added to the list in Re-link
    fw1 = cs.FilamentWinding(ID=D.fileMetadata.maxID+1)
    D.fileMetadata.maxID += 1
    D.allManufMethods.append(fw1) 

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

#MANUAL check for file created
# D = create_example()
# print("lenC",len(D.allComposite))
# print("lenG",len(D.allGeometry))
# print("lenD",len(D.allDefects))
# print("lenT",len(D.allTolerances))
# print("lenM",len(D.allMaterials))
# cs.Save(D,"TEST_Compost","C:\\temp")

def NewFileComparison(D):
    #This function is used to verify the test component was created as expected

    print("Running generation test...")
    #countErrors
    noErr = 0

    #check number of objects in main lists
    if len(D.allComposite) !=3:
        print("Error: Wrong number of IDed composites in main list.")
        noErr += 1
    if len(D.allGeometry) !=10:
        print("Error: Wrong number of IDed geometries in main list.")
        noErr += 1
    if len(D.allDefects) !=4:
        print("Error: Wrong number of IDed defects in main list.")
        noErr += 1
    if len(D.allTolerances) !=4:
        print("Error: Wrong number of IDed tolerances in main list.")
        noErr += 1
    if len(D.allMaterials) !=2:
        print("Error: Wrong number of IDed materials in main list.")
        noErr += 1
    
    #check maximum ID
    if D.fileMetadata.maxID != 28:
        print("Error: incorrect maxID")
        noErr += 1

    #TODO add anything else that should be checked as required

    return(noErr)

def testReLink(D):
    
    print("Running re-link test...")

    noErr = 0

    #edit one of the ID linked pair

    #Check point re-used in mesh
    for G in D.allGeometry:
        if G.ID == 4:
            G.x = 567 
    #assume error until verified it does not exist
    tErr = True
    for G in D.allGeometry:
        if type(G) == type(cs.AreaMesh()):
            for E in G.meshElements:
                for N in E.nodes:
                    if N.ID == 4:
                        if N.x == 567:
                            tErr = False
                            break
    if tErr == True:
        noErr += 1
        print("Error: Re-link error, the modificication of ID=4 point was not propagated to the copies of the object.")


    #check axis system re-link --only specific instance is checked, it is assumed others work if this does (TODO make more robust?)
    for G in D.allGeometry:
        if G.ID == 9:
            G.memberName = "TEST_TEST"
    #assume error until verified it does not exist
    tErr = True
    for T in D.allTolerances:
        if type(T) == type(cs.WrinkleTolerance()):
            if T.axisSystem.ID == 9:
                if T.axisSystem.memberName == "TEST_TEST":
                    tErr = False
                    break
    if tErr == True:
        noErr += 1
        print("Error: Re-link error, the modificication of ID=9 axis system was not propagated to the copies of the object.")

    
    for C in D.allComposite:
        if C.ID == 13:
            C.memberName = "EDIT_TESTING"

    #assume error until proven otherwise
    tErr = True
    for C in D.allComposite:
        if C.ID == 18:
            for s1 in C.subComponents:
                if s1.ID == 14:
                    for s2 in s1.subComponents:
                        if s2.ID == 13:
                            if s2.memberName == "EDIT_TESTING":
                                tErr = False
                                break
    if tErr == True:
        noErr += 1
        print("Error: Re-link error, the modificication of ID=13 piece was not propagated to the copies of the object.")
    #assume error until proven otherwise
    tErr = True
    for C in D.allComposite:
        if C.ID == 14:
            for s2 in C.subComponents:
                if s2.ID == 13:
                    if s2.memberName == "EDIT_TESTING":
                        tErr = False
                        break
    if tErr == True:
        noErr += 1
        print("Error: Re-link error, the modificication of ID=13 piece was not propagated to the copies of the object.")


    #check material example - ID=11
    for M in D.allMaterials:
        if M.ID == 11:
            M.memberName = "NEW_NAME_FOR_TESTING"

    #assume error until proven otherwise
    tErr = True
    for C in D.allComposite:
        if C.ID == 14:
            for s1 in C.subComponents:
                if s1.ID == 13:
                    if s1.material.ID == 11:
                        if s1.material.memberName == "NEW_NAME_FOR_TESTING":
                            tErr = False
                            break
    if tErr == True:
        noErr += 1
        print("Error: Re-link error,the material with ID=11 was not propagated correctly to a piece ID=13.")    

    #re-save in the end for manual review (optional)
    cs.Save(D,"test_save_review","C:\\temp",overwrite=True)

    #TODO test re-link from initialDrapePoint point storage

    
    #TODO try more re-links when adding functionality (expanding list in Utilities)
    #copied objects 20,2,24...

    return(noErr)

class TestMainCompoST(unittest.TestCase):

    #create file 
    D = create_example()

    #save file in temp
    cs.Save(D,"test_save","C:\\temp",overwrite=True)
    
    #load file
    D = cs.Open("test_save","C:\\temp")

    #test initial file 
    def test_generation(self):
        self.assertEqual(NewFileComparison(self.D),0)

    #test re-link method
    def test_link(self):
        self.assertEqual(testReLink(self.D),0)


    #any more tests needed?

if __name__ == "__main__":
    unittest.main()