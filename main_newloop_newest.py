# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
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
InputSize = "1000"

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




# %%
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
z=2

# Erstellen der verschiedenen Arrays
bodencountout_array = np.empty((nrows,ncols))
bodencountout_array[:] = np.NaN

bodenhoehen_array = np.empty((nrows,ncols))
bodenhoehen_array[:] = np.NaN

vegcount_array = np.empty((nrows,ncols))
vegcount_array[:] = np.NaN

vegcount_higher2_array = np.empty((nrows,ncols))
vegcount_higher2_array[:] = np.NaN

veghigher2_hoehen_array  = np.empty((nrows,ncols))
veghigher2_hoehen_array[:] = np.NaN

vegpoints_array = np.empty((nrows,ncols))
vegpoints_array[:] = np.NaN

bodenpoints_array = np.empty((nrows,ncols))
bodenpoints_array[:] = np.NaN



# %%
#----------------------------------
#Bodenpunkte zaehlen:
#----------------------------------
#Cellsize = float(raw_input("Bitte geben Sie die gewuenschte Rasterzellengroesse an:")) #Raw Input funktioniert in VisualStudio nicht
Cellsize = 1

print("Bodenpunkte in Rasterzellen aufteilen und Mittelwert pro Zelle berechnen:")
printProgressBar(0, len(bodenarray), prefix = 'Progress:', suffix = 'Complete', length = 50)
j=0
for i in bodenarray:
    printProgressBar(j+1, len(bodenarray), prefix = 'Progress:', suffix = 'Complete', length = 50)
    j+=1
    x=i[0]
    y=i[1]
    height = i[2]
    gx = int((x -xmin)/Cellsize)
    gy = int((y -ymax)/-Cellsize)  
    bodencountout_array[gy][gx] +=1
    if np.isnan(bodenhoehen_array[gy][gx]) == True:
        bodenhoehen_array[gy][gx] = i[2]
    else:
        bodenhoehen_array[gy][gx] = np.mean([bodenhoehen_array[gy][gx],i[2]])


# %%
#----------------------------------
#Mittlere Hoehe der VegPunkte:
#----------------------------------
print("Vegetationspunkte in Rasterzellen aufteilen und erstellen eines Array mit Punkten uber 2 Meter:")
printProgressBar(0, len(vegarray), prefix = 'Progress:', suffix = 'Complete', length = 50)
j=0
for i in vegarray:
    printProgressBar(j+1, len(vegarray), prefix = 'Progress:', suffix = 'Complete', length = 50)
    j+=1
    x=i[0]
    y=i[1]
    height = i[2]
    #print(height-bodenhoehen_array[gy][gx])
    gx = int((x -xmin)/Cellsize)
    gy = int((y -ymax)/-Cellsize)
    vegcount_array[gy,gx]+=1
    if height-bodenhoehen_array[gy][gx] >= 2:
        vegcount_higher2_array[gy,gx]+=1
        if np.isnan(vegcount_higher2_array[gy][gx]) == True:
            veghigher2_hoehen_array[gy][gx] = (i[2]-bodenhoehen_array[gy][gx])
        else:
            veghigher2_hoehen_array[gy][gx] = np.mean([veghigher2_hoehen_array[gy][gx],i[2]])   

#print ("1",veghigher2_hoehen_array)
#         veghigher2_hoehen_array[gy][gx] = (i[2]-bodenhoehen_array[gy][gx])
# veghigher2_hoehen_array[gy][gx] = np.mean([veghigher2_hoehen_array[gy][gx],i[2]])
# # # Zwei obere Zeilen = Vereinfachung der unteren Schleife - bei Boden auch noch zu machen            
  



    # #print("xRichtungEnde") 
    # #vegstdout_array[np.isnan(vegstdout_array)] = 0
    # #veghoeheout_array[np.isnan(veghoeheout_array)] = 0


# %%
#-------------------------------
#Index anzahl veg zu bodenpunkte veg/(veg-boden):
#-------------------------------
indexarray1 = np.empty((nrows,ncols))
indexarray1 = vegcount_array/(vegcount_array+bodencountout_array)


# %%
#-------------------------------
#Index anzahl veg ueber 2 m zu bodenpunkte veg/(veg-boden):
#-------------------------------
indexhoehen2m = np.empty((nrows,ncols))
indexhoehen2m = vegcount_higher2_array/(vegcount_higher2_array+bodencountout_array)


# %%
#-------------------------------
#OutRaster schreiben:
#-------------------------------


#Boden Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/BodenCount_%s.tif"  % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
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
dataset = driver.Create("Export/BodenHoehen_%s.tif" % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

# #Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

# #Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(bodenhoehen_array)
dataset.FlushCache()


# %%

#Vegetation Zaehler Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/VegCount_%s.tif" % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

#Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

#Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(vegcount_array)
dataset.FlushCache()


# %%

# #Vegetation Mittlere Hoehe Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/VegHoehen_%s.tif" % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

# #Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

# #Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(veghigher2_hoehen_array)
dataset.FlushCache()

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
#Index Verhaeltnis VegPunkte zu Bodenpunkte Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/Index1_%s.tif" % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

#Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

#Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(indexarray1)
dataset.FlushCache()


# %%
#Index Verhaeltnis VegPunkte zu Bodenpunkte Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/Index2_higher2_%s.tif" % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

#Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

#Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(indexhoehen2m)
dataset.FlushCache()

# # %%
# #Index Verhaeltnis VegPunkte zu Bodenpunkte Raster Saga
# driver = gdal.GetDriverByName("AAIGrid")
# dataset = driver.Create("Export/Index2_higher2_%s.tif" % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
# #dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

# #Koordinatensystem definieren:
# dstSRS = osr.SpatialReference()
# dstSRS.ImportFromEPSG(32632)
# dest_wkt = dstSRS.ExportToWkt()

# dataset.SetProjection(dest_wkt)

# #Raster ausgeben:
# bandout = dataset.GetRasterBand(1).WriteArray(vegstdout_array)
# dataset.FlushCache()

print ("finalDone")
