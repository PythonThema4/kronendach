# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#-------------------------------
#Funktionen:
#-------------------------------

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


# %%
import numpy as np
from osgeo import gdal
from osgeo import osr
import time
import statistics 


#-------------------------------
#File einlesen:
#-------------------------------
fobj = open('Daten/Waldpunktwolke_1000.txt', "r") #Input File

pointlist = []

next(fobj)
for line in fobj:
    line = line.strip()
    line= line.split("\t")   
    pointlist.append(line)
fobj.close


# %%
#-------------------------------
#Daten einlesen und nach Typ Filtern:
#-------------------------------

pointarray = np.array(pointlist) 
pointarray = pointarray.astype(float)  
print(len(pointarray))

#Neuer Array ohne Gebauede und Boden, Klassen 3, 4, 5
vegetationslist = []
bodenlist=[]

print("Vegetations-und Bodenliste einlesen:")
printProgressBar(0, len(pointarray), prefix = 'Progress:', suffix = 'Complete', length = 50)
j=0
for i in pointarray:
    printProgressBar(j+1, len(pointarray), prefix = 'Progress:', suffix = 'Complete', length = 50)
    j+=1
    if i[6] == 3 or i[6] ==4 or i[6] ==5:
        vegetationslist.append(i)
    if i[6] == 2:
        bodenlist.append(i)

vegarray = np.array(vegetationslist)        
bodenarray = np.array(bodenlist)


#----------------------------------
#Extend Array with random numbers:
#----------------------------------
#max values
maxvals = np.amax(pointarray,axis=0) 
xmax=maxvals[0]
ymax=maxvals[1]
# print ("xmax:",xmax)
# print ("ymax:",ymax)

#min values
minvals = np.amin(pointarray,axis=0) 
xmin=minvals[0]
ymin=minvals[1]
# print ("xmin:",xmin)
# print ("ymin:",ymin)

#empty array with extent dimensions
nrows= int(np.ceil(ymax-ymin))
ncols= int(np.ceil(xmax-xmin))

bodencountout_array = np.empty((nrows,ncols))
bodencountout_array.fill(0)

bodenhoehenout_array = np.empty((nrows,ncols))
bodenhoehenout_array.fill(0)

vegcountout_array = np.empty((nrows,ncols))
vegcountout_array.fill(0)

# veghoeheout_array = np.empty((nrows,ncols))
# veghoeheout_array.fill(0)

# vegstdout_array = np.empty((nrows,ncols))
# vegstdout_array.fill(0)

# vegslicecountout_array = np.empty((nrows,ncols))
# vegslicecountout_array.fill(0)

# vegsliceverh_array = np.empty((nrows,ncols))
# vegsliceverh_array.fill(0)

# veghoehe_ab2_array = np.empty((nrows,ncols))
# veghoehe_ab2_array.fill(0)

vegpoints_array = np.empty((nrows,ncols))
vegpoints_array.fill(0)

bodenpoints_array = np.empty((nrows,ncols))
bodenpoints_array.fill(0)

# %%
#----------------------------------
#Bodenpunkte zaehlen:
#----------------------------------
#bodencount = 0
#countlist =[]
#arraycount_x = 0
#arraycount_y = 0
bodenhoehenlist = []

Cellsize=1

for i in bodenarray:
 #   print (i)
    x=i[0]
    y=i[1]
    height = i[2]
    gx = int((x -xmin)/Cellsize)
    gy = int((y -ymax)/-Cellsize)  
    bodencountout_array[gy,gx]+=1
    bodenpoints_array[gy,gx] = i[2]
print(bodenpoints_array)    
#for i in bodenpoints_array:
 #   print (i)

#     bodenhoehenout_array[gy,gx] = np.mean(bodenpoints_array,axis=0)

# print (bodenhoehenout_array)   

#bodenhoehenout_array= [nrows,ncols]=np.mean(bodenpoints_array[)

#print (bodenhoehenout_array)
    # for i in bodenarray[-1]:
    # print (i)
    # xnew=i[0]
    # y2=i[1]
    # gx2 = int((x2 -xmin)/Cellsize)
    # gy2 = int((y2 -ymax)/-Cellsize)
    # if x == gx2 and y == gy2:
    #     bodenhoehenlist.append(i[2])
    # else:
    #     bodenhoehenout_array[gy,gx]=np.mean(bodenhoehenlist)
    #     bodenhoehenlist=[]
    #bodenpoints_array[gy,gx]=i
   # bodenpoints_array[gy,gx] = i
    #  bodencountout_array[gy,gx]=1
    # if x <= i[0] < gx+1 and gy >= i[1] > gy-1:
    #    bodenhoehenlist.append(i[2])
    #bodenhoehenout_array[gy,gx]=np.mean(bodenhoehenlist)
    #bodenhoehenlist=[]
    #print(bodencountout_array)
    #bodenpoints_array[gy,gx]=i


# print("Bodenpunkte zuordnen:")
# printProgressBar(0, len(np.arange(ymax,ymax-nrows,-1)), prefix = 'Progress:', suffix = 'Complete', length = 50)
# j=0
# for y in np.arange(ymax,ymax-nrows,-1):
#     printProgressBar(j+1, len(np.arange(ymax,ymax-nrows,-1)), prefix = 'Progress:', suffix = 'Complete', length = 50)
#     j+=1
#     # print("yRichtung:",y)
#     # print("ArraypositionY:",arraycount_y)
#     for x in np.arange(xmin,xmin+ncols,1):
#         # print("xRichtung:",x)
#         # print("ArraypositionX:",arraycount_x)
#         for i in bodenarray:
#             if x <= i[0] < x+1 and y >= i[1] > y-1:
#                 bodencount+=1
#                 bodenhoehenlist.append(i[2])
#         bodencountout_array[arraycount_y][arraycount_x]=bodencount
#         bodenhoehenout_array[arraycount_y][arraycount_x]=np.mean(bodenhoehenlist)
#         arraycount_x+=1     
#         bodencount=0
#         bodenhoehenlist=[]
#     arraycount_x=0
#     arraycount_y+=1
    # print("xRichtungEnde")
    #bodenhoehenout_array[np.isnan(bodenhoehenout_array)] = 0




# %%
#----------------------------------
#Mittlere Hoehe der VegPunkte:
#----------------------------------
#vegcount = 0
#vegslicecount = 0

# countlist =[]
# arraycount_x = 0
# arraycount_y = 0
# veghoehenlist = []

# print("VegPunkte zuordnen:")
# printProgressBar(0, len(np.arange(ymax,ymax-nrows,-1)), prefix = 'Progress:', suffix = 'Complete', length = 50)
# j=0

Cellsize=1

for i in vegarray:
    x=i[0]
    y=i[1]
    height = i[2]
    gx = int((x -xmin)/Cellsize)
    gy = int((y -ymax)/-Cellsize)
    vegcountout_array[gy,gx]+=1
   # vegpoints_array[gy,gx]=i

# for y in np.arange(ymax,ymax-nrows,-1):
#     printProgressBar(j+1, len(np.arange(ymax,ymax-nrows,-1)), prefix = 'Progress:', suffix = 'Complete', length = 50)
#     j+=1
#     # print("yRichtung:",y)
#     # print("ArraypositionY:",arraycount_y)
#     for x in np.arange(xmin,xmin+ncols,1):
#         # print("xRichtung:",x)
#         # print("ArraypositionX:",arraycount_x)
#         for i in vegarray:
#             if x <= i[0] < x+1 and y >= i[1] > y-1: #Hier sind wir in der jeweiligen Zelle
#                 veghoehenlist.append(i[2])
#                 vegcount+=1
#                 if i[2] >= ((max(veghoehenlist))-1):
#                     vegslicecount+=1
        
    #     #vegpoints_array[arraycount_y][arraycount_x]=(veghoehenlist)
    #     veghoeheout_array[arraycount_y][arraycount_x]=np.mean(veghoehenlist) #Mittlere Hoehe der VegPunkte
    #     vegstdout_array[arraycount_y][arraycount_x]=np.std(veghoehenlist) #Standardabweichung der VegPunkte
    #     #vegcountout_array[arraycount_y][arraycount_x]=vegcount #Anzahl der Vegetationspunkte in Zelle
    #     vegslicecountout_array[arraycount_y][arraycount_x]=vegslicecount #Anzahl der Vegetationspunkte in Zelle

    #     #forif veghoehenlist ==
    #      #   print (max(veghoehenlist))
    #     arraycount_x+=1     
    #     vegcount=0
    #     vegslicecount=0
    #     veghoehenlist=[]
    # arraycount_x=0
    # arraycount_y+=1
    # #print("xRichtungEnde") 
    # #vegstdout_array[np.isnan(vegstdout_array)] = 0
    # #veghoeheout_array[np.isnan(veghoeheout_array)] = 0


# %%
#-------------------------------
#Tatsaechliche VegHoehe: nDom
#-------------------------------
#vegtathoehe_array = np.empty((nrows,ncols))
#vegtathoehe_array = veghoeheout_array - bodenhoehenout_array


# %%
#-------------------------------
#Index anzahl veg zu bodenpunkte veg/(veg-boden):
#-------------------------------
indexarray1 = np.empty((nrows,ncols))
indexarray1 = vegcountout_array/(vegcountout_array+bodencountout_array)


# %%
#-------------------------------
#Index anzahl veg ueber 2 m zu bodenpunkte veg/(veg-boden):
#-------------------------------
#veghoehe_ab2_array = vegtathoehe_array >2
#print (veghoehe_ab2_array)
#indexhoehen2m = np.empty((nrows,ncols))
#indexhoehen2m = vegcountout_array/(vegcountout_array+bodencountout_array)

# %%
# for y in np.arange(ymax,ymax-nrows,-1):
#     # print("yRichtung:",y)
#     # print("ArraypositionY:",arraycount_y)
#     for x in np.arange(xmin,xmin+ncols,1):
#         if vegtathoehe_array[x][y]>=
#         vegsliceverh_array = vegslicecountout_array/vegcountout_array #verhaeltnis von veg im obersten meter zu gesamte vegPunkte


# %%
#-------------------------------
#OutRaster schreiben:
#-------------------------------


#Boden Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/BodenCount_1000.tif", ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

#Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

#Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(bodencountout_array)
dataset.FlushCache()


# %%
# #Bodenhoehen Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/BodenHoehen_1000.tif", ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

# #Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

# #Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(bodenhoehenout_array)
dataset.FlushCache()


# %%

#Vegetation Zaehler Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/VegCount_1000.tif", ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

#Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

#Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(vegcountout_array)
dataset.FlushCache()


# %%

# #Vegetation Mittlere Hoehe Raster
# driver = gdal.GetDriverByName("GTiff")
# dataset = driver.Create("Export/VegHoehen_1000.tif", ncols, nrows, 1, gdal.GDT_Float32)
# dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

# #Koordinatensystem definieren:
# dstSRS = osr.SpatialReference()
# dstSRS.ImportFromEPSG(32632)
# dest_wkt = dstSRS.ExportToWkt()

# dataset.SetProjection(dest_wkt)

# #Raster ausgeben:
# bandout = dataset.GetRasterBand(1).WriteArray(vegtathoehe_array)
# dataset.FlushCache()

print ("done1")
# %%

# #Vegetation Standardabweichung Hoehe Raster
# driver = gdal.GetDriverByName("GTiff")
# dataset = driver.Create("Export/VegStd_1000.tif", ncols, nrows, 1, gdal.GDT_Float32)
# dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

# #Koordinatensystem definieren:
# dstSRS = osr.SpatialReference()
# dstSRS.ImportFromEPSG(32632)
# dest_wkt = dstSRS.ExportToWkt()

# dataset.SetProjection(dest_wkt)

# #Raster ausgeben:
# bandout = dataset.GetRasterBand(1).WriteArray(vegstdout_array)
# dataset.FlushCache()


# %%

#Vegetation Standardabweichung Hoehe Raster
# driver = gdal.GetDriverByName("GTiff")
# dataset = driver.Create("Export/VegStd_1000_float64.tif", ncols, nrows, 1, gdal.GDT_Float64)
# dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

# #Koordinatensystem definieren:
# dstSRS = osr.SpatialReference()
# dstSRS.ImportFromEPSG(32632)
# dest_wkt = dstSRS.ExportToWkt()

# dataset.SetProjection(dest_wkt)

# #Raster ausgeben:
# bandout = dataset.GetRasterBand(1).WriteArray(vegstdout_array)
# dataset.FlushCache()


# %%
#Index Verhaeltnis VegPunkte zu Bodenpunkte Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/Index1_1000.tif", ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

#Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

#Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(indexarray1)
dataset.FlushCache()

print ("finalDone")

# %%


