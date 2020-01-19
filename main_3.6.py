import numpy as np
from osgeo import gdal

from osgeo import osr

fobj = open('Daten/Waldpunktwolke_100.txt', "r")
#print fobj

pointlist = []


#read in
next(fobj)
for line in fobj:
    line = line.strip()
    line= line.split("\t")   
    pointlist.append(line)
fobj.close

pointarray = np.array(pointlist) 
pointarray = pointarray.astype(float)  


#Neuer Array ohne Gebauede und Boden, Klassen 3, 4, 5
vegetationslist = []

for i in pointarray:
        
        if i[6] == 3 or i[6] ==4 or i[6] ==5:
                vegetationslist.append(i)
                

#print vegetationslist
vegetationsarray = np.array(vegetationslist)
print ("Vegetationsarray", vegetationsarray)
        


#Neuer Array Bodenpunkte
bodenlist = []

for i in pointarray:
        
        if i[6] == 2:
                bodenlist.append(i)
                
bodenarray = np.array(bodenlist)
print ("Bodenarray", bodenarray)
        


#print pointlist
print ("--------")

#max values
maxvals = np.amax(pointarray,axis=0) 
xmax=maxvals[0]
ymax=maxvals[1]
print ("xmax:",xmax)
print ("ymax:",ymax)
#min values
minvals = np.amin(pointarray,axis=0) 
xmin=minvals[0]
ymin=minvals[1]
print ("xmin:",xmin)
print ("ymin:",ymin)
#ratio
nrows= np.ceil(ymax-ymin)
ncols= np.ceil(xmax-xmin)

print (nrows)
print (ncols)
#create Extent Raster
bodenout_array = np.empty((nrows,ncols))
bodenout_array.fill(0.0)


bodencount = 0
countlist =[]
arraycount_x = 0
arraycount_y = 0


for x in np.arange(xmin,xmin+ncols):
    #print x
    
    for y in np.arange(ymin,ymin+nrows):
        #print y
        for i in bodenarray:
                if i[0] >= x and i[0] <= x+1 and i[1] >= y and i[1] <= y+1:
                        bodencount+=1        
        countlist.append(bodencount)                
        bodencount=0
print ("-------")
print ("Kontrolle")
print (countlist)
print ("leng", len(bodenarray))

countarray = np.array(countlist)
print (countarray)


# for x in np.arange(xmin,xmin+ncols):
#     #print x
#     arraycount_x+=1
#     for y in np.arange(ymin,ymin+nrows):
#         #print y
#         arraycount_y+=1
#         for i in bodenarray:
#                 if i[0] >= x and i[0] <= x+1 and i[1] >= y and i[1] <= y+1:
#                         bodencount+=1

#                 bodenout_array[arraycount_x][arraycount_y]=bodencount
#                 bodencount = 0
        

driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Out2.tif", int(ncols), int(nrows), 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

# projection = osr.SpatialReference()
# projection = projection.ImportFromEPSG(32623)
# print projection

#dataset.SetProjection(projection)

bandout = dataset.GetRasterBand(1)
bandout.WriteArray(bodenout_array)
dataset.FlushCache()
