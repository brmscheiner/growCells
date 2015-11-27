''' Notes: don't check intersections and create new spheres if 
distance between the centerpoints of two spheres is greater than 
the sum of the radii. Remove volume and area calculations and 
create a sphere class which holds brep object and information 
about centerpoint, radius, and color 

And obviously change all variable names :P '''

import rhinoscriptsyntax as rs


def GrowthRecursion(points, totalSpheres, prevRad, prevTrans):
    
    newSpheres = []
    newSpheres = IsPointsInsideNewSpheres(points, newSpheres, prevRad)
    
    #search posible centerpoints
    IntersectionPoints = GetIntersections(totalSpheres, newSpheres, prevTrans)
    
    #Update total spheres
    totalSpheres = UpdateTotalSpheres(totalSpheres, newSpheres)
    
    #Get Outside Points
    outSidePoints = GetOutsidePoints(IntersectionPoints, totalSpheres)
    
    newRad = prevRad*GF
    newTrans = prevTrans*TF
    if len(totalSpheres) < 10:
        GrowthRecursion(outSidePoints, totalSpheres, newRad, newTrans)

def isPtInside(p, sph):
    
    inside = True
    
    centroid = rs.SurfaceVolumeCentroid(sph)
    perimeter = rs.BrepClosestPoint(sph, centroid[0])
    rad = rs.Distance(centroid [0], perimeter [0])
    
    dist = rs.Distance(p, centroid[0])
    

    
    if dist > rad:
        inside = False
    
    return inside

def IsPointsInsideNewSpheres(points, spheres, rad):
        
        
    
    if len(spheres) == 0:
        sphere = rs.AddSphere(points [0], rad)
        spheres.append(sphere)
        points.remove(points [0])

    
    if len(points)>0:
        putPt =True
        for s in spheres:
            if isPtInside(points[0], s) == True:
                putPt = False

        if putPt == True:
            sphere = rs.AddSphere(points [0], rad)
            spheres.append(sphere)
            points.remove(points [0])
        else:
            points.remove(points [0])
            
        if len(points)>0:
            IsPointsInsideNewSpheres(points, spheres, rad)

    return spheres

def GetIntersections(totalSph, newSph, translation):
    IntersectionPoints = []
    for t in totalSph:
        for n in newSph: 
            
            intersection = rs.IntersectBreps(t, n)
            if intersection is not None:
                if len(intersection) != 0:
                    for int in intersection:
                        pointOnIntersection = rs.AddPoint(rs.CurveEndPoint(int))
                        
                        rs.ObjectColor(intersection,(255,0,255))
                        centreIntersection = rs.CurveAreaCentroid(int)
                        pointOnCenterIntersection = rs.AddPoint(centreIntersection [0])
                        
                        vectorDirectionOffset = rs.PointAdd(pointOnCenterIntersection, pointOnIntersection)
                        
                        Aux = rs.OffsetCurve(int, vectorDirectionOffset, translation)
                        #rs.ObjectColor(Aux, (0,255,0))
                        
                        centerPointsInfo = rs.CurveBrepIntersect(Aux, plane00)
                        """
                        centerPtA = rs.AddPoint(centerPointsInfo [0][1])
                        centerPtB = rs.AddPoint(centerPointsInfo [1][1])
                        """
                        if centerPointsInfo is not None:
                            IntersectionPoints.append(centerPointsInfo [1][0])
                            if len(centerPointsInfo [1])>1:
                                IntersectionPoints.append(centerPointsInfo [1][1])
    return IntersectionPoints

def UpdateTotalSpheres(totalSpheres, newSpheres):
    for n in newSpheres:
        totalSpheres.append(n)
    return totalSpheres

def GetOutsidePoints(intPts, totalSpheres):
    pointsForElimination = []
    
    if len(intPts)>0:
        for t in totalSpheres:
            for p in intPts: 
                centroid = rs.SurfaceVolumeCentroid(t)
                perimeter = rs.BrepClosestPoint(t, centroid[0])
                rad = rs.Distance(centroid [0], perimeter [0])
                
                dist = rs.Distance(p, centroid[0])
                #print dist
                
                if dist < rad:
                    pointsForElimination.append(p)
                    [pointsForElimination.remove(i) for i in pointsForElimination if pointsForElimination.count(i) >= 2]
        
        #remove points inside previous from list
    if len(pointsForElimination)>0:
        if len(intPts)>0:
            for x in pointsForElimination:
                    intPts.remove(x)
    
    return intPts

#plane00 = rs.WorldXYPlane()
plane00 = rs.GetObject("select Surface")
#plane00AreaCentroid = rs.SurfaceAreaCentroid(plane00)
#plane00Center = rs.BrepClosestPoint(plane00, plane00AreaCentroid [0])


#centerPt00 = plane00Center [0]

centerPt00 = rs.GetPoint("select center")

rad00 = 1

initialAngle = 0
TF = .7
GF = 1.02
rotAngle = 0

firstSpheres = []
#totalRadius = []

sphere00 = rs.AddSphere(centerPt00, rad00)
firstSpheres.append(sphere00)


connection01 = rs.AddPoint(rs.Polar(centerPt00, initialAngle, rad00))

rad01 = (rad00*GF)
translation01 = .2
summOfRotationAngle = initialAngle + rotAngle
centerPt01 = rs.Polar(connection01, summOfRotationAngle, translation01)

sphere01 = rs.AddSphere(centerPt01,rad01)
firstSpheres.append(sphere01)

#find intersections
intersection00 = rs.IntersectBreps(sphere00, sphere01)

plane01 = rs.CurvePlane(intersection00) #???

translation02 = TF
Aux01 = rs.OffsetCurve(intersection00, plane01 [0], translation02) #???
rs.ObjectColor(Aux01, (0,255,0))
print plane01 
#pointsCenter = rs.PlaneCurveIntersection(plane00, Aux01)
pointsCenter = rs.CurveBrepIntersect(Aux01, plane00)
print pointsCenter


centerPt = []
"""
centerPt02A = rs.AddPoint(pointsCenter [0])
centerPt02B = rs.AddPoint(pointsCenter [1])
"""
centerPt.append(pointsCenter [1][0])
centerPt.append(pointsCenter [1][1])

rad02 = rad00*GF




GrowthRecursion(centerPt, firstSpheres, rad02, translation02)


