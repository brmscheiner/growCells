import rhinoscriptsyntax as rs
from math import sqrt



class Sphere:
    def __init__(self,c,r,color=None):
        ''' center of sphere c takes the form [x,y,z] and r > 0 '''
        self.c=c
        self.r=r
        self.x=c[0]
        self.y=c[1]
        self.z=c[2]
        self.brep=rs.AddSphere(c,r)
        if color:
            self.setColor(color)
            
    def setColor(self,color):
        ''' color takes the form (r,g,b) where 0<=r,g,b<=255 '''
        rs.ObjectColor(self.brep,color)
        
    def isClose(self,isphere):
        d = sqrt((self.x-isphere.x)**2 + (self.y-isphere.y)**2 + (self.z-isphere.z)**2)
        if d < (self.r + isphere.r):
            return True
        else:
            return False
            
    def isPointInside(self,point):
        x = point[0]
        y = point[1]
        z = point[2]
        d = sqrt((self.x-x)**2 + (self.y-y)**2 + (self.z-z)**2)
        if d>self.r:
            return False
        else:
            return True
            
    def getNewCenterPoints(self,surface,isphere):
        t = 0.7 # translation factor 
        intersection = rs.IntersectBreps(self.brep,isphere.brep)
        intersectionPlane = rs.CurvePlane(intersection)
        scaledIntersection = rs.OffsetCurve(intersection,intersectionPlane[0],t)
        # ip[0] = Origin=53.5112860700772,12.7634118321508,102.900274104955 XAxis=-1.09236069576488E-13,1,0, YAxis=-2.18668221722765E-14,-2.38886166598282E-27,-1, ZAxis=-1,-1.09236069576488E-13,2.18668221722765E-14
        # must change offset to be a point outside the curve object
        rhino_pts = rs.CurveBrepIntersect(scaledIntersection,surface)
        intersection_pts = []
        if rhino_pts is not None:
            intersection_pts.append(rhino_pts[1][0])
            if len(rhino_pts[1])>1:
                intersection_pts.append(rhino_pts[1][1])
        return intersection_pts

def createDemoSurface():
    ''' Create a demo surface for fast debugging '''
    points = []
    pt0 = rs.AddPoint(-100,0,-100)
    pt1 = rs.AddPoint(-50,0,+100)
    pt2 = rs.AddPoint(0,0,-100)
    pt3 = rs.AddPoint(50,0,100)
    pt4 = rs.AddPoint(100,0,-100)
    ptRef = rs.AddPoint(-100,500,-100)
    points.append(pt0)
    points.append(pt1)
    points.append(pt2)
    points.append(pt3)
    points.append(pt4)
    
    section = rs.AddInterpCurve(points)
    rail = rs.AddLine(pt0, ptRef)
    
    plane00 = rs.ExtrudeCurve(section, rail)
    pt00 = rs.AddPoint(-50,250,100)
    return plane00

def createSpheres(centerPointList,r,color=None):
    ''' creates a list of spheres from a list of center points '''
    newSpheres = []
    for cp in centerPointList:
#        new = Sphere(cp,r)
        new = Sphere([0,0,0],20)
        print cp
        if color:
            new.setColor(color)
        newSpheres.append(new)
    return newSpheres

def growth(newCells,oldCells,surface,depth):
    r = 20 # radius could depend on depth 
    if depth>5:
        return
    else: 
        # Identify potential growth areas on surface 
        candidateCenterPoints = []
        for new in newCells:
            for old in oldCells:
                if new.isClose(old):
                    pts = new.getNewCenterPoints(surface, old)
                    candidateCenterPoints += pts
        # Prune growth areas 
        newCenterPoints = []
        for cp in candidateCenterPoints:
            insideFlag = False
            newCenterPoints.append(cp)
#            for cell in cells:
#                print cp
#                if cell.isPointInside(cp):
#                    insideFlag = True
#            if insideFlag == False:
#                newCenterPoints.append(cp)
#        # Build new cells 
#        for cp in newCenterPoints:
#            cells.append(Sphere(cp,r))
#        print depth
        oldCells = newCells + oldCells
        newCells = createSpheres(newCenterPoints,r)
        print newCenterPoints
        growth(newCells,oldCells,surface,depth+1)

if __name__=="__main__":
    surface = createDemoSurface()
    initialSphere = Sphere([-50,300,100],20)
    initialSphere.setColor((0,255,0))
    secondSphere = Sphere([-50,315,100],20)
    newCells = [initialSphere]
    oldCells = [secondSphere]
    growth(newCells,oldCells,surface,0)