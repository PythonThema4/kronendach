# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#-------------------------------
#Funktionen:
#-------------------------------

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '*', printEnd = "\r"):
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

#-------------------------------
#File einlesen:
#-------------------------------
fobj = open('Daten/Waldpunktwolke_5000.txt', "r") #Input File

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

vegetationsarray = np.array(vegetationslist)        
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

bodenout_array = np.empty((nrows,ncols))
bodenout_array.fill(0)


# %%
#----------------------------------
#Bodenpunkte zaehlen:
#----------------------------------
bodencount = 0
countlist =[]
arraycount_x = 0
arraycount_y = 0

print("Bodenpunkte zuordnen:")
printProgressBar(0, len(np.arange(ymax,ymax-nrows,-1)), prefix = 'Progress:', suffix = 'Complete', length = 50)
j=0
for y in np.arange(ymax,ymax-nrows,-1):
    printProgressBar(j+1, len(np.arange(ymax,ymax-nrows,-1)), prefix = 'Progress:', suffix = 'Complete', length = 50)
    j+=1
    # print("yRichtung:",y)
    # print("ArraypositionY:",arraycount_y)
    for x in np.arange(xmin,xmin+ncols,1):
        # print("xRichtung:",x)
        # print("ArraypositionX:",arraycount_x)
        for i in bodenarray:
            if x <= i[0] < x+1 and y >= i[1] > y-1:
                bodencount+=1
        bodenout_array[arraycount_y][arraycount_x]=bodencount
        arraycount_x+=1     
        bodencount=0
    arraycount_x=0
    arraycount_y+=1
    # print("xRichtungEnde")    




# %%
#-------------------------------
#OutRaster schreiben:
#-------------------------------

driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Bodenpunkte_5000.tif", ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

#Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

#Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(bodenout_array)
dataset.FlushCache()


# %%



