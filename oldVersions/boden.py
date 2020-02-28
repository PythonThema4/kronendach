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
from scipy import interpolate


#-------------------------------
#File einlesen:
#-------------------------------
fobj = open('Daten/Waldpunktwolke.txt', "r") #Input File
InputSize = "full"

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
bodencountout_array.fill(0)

bodenhoehencountout_array = np.empty((nrows,ncols))
bodenhoehencountout_array[:] = np.NaN

bodenhoehen_array = np.empty((nrows,ncols))
bodenhoehen_array[:] = np.NaN

vegcount_array = np.empty((nrows,ncols))
vegcount_array.fill(0)

vegcount_higher2_array = np.empty((nrows,ncols))
vegcount_higher2_array.fill(0)

veghohen_arry= np.empty((nrows,ncols))
veghohen_arry[:] = np.NaN

veghigher2_hoehen_array  = np.empty((nrows,ncols))
veghigher2_hoehen_array[:] = np.NaN

vegpoints_array = np.empty((nrows,ncols))
vegpoints_array[:] = np.NaN

bodenpoints_array = np.empty((nrows,ncols))
bodenpoints_array[:] = np.NaN

veghigher2_count_array = np.empty((nrows,ncols))
veghigher2_count_array[:] = np.NaN

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
    bodenhoehencountout_array[gy][gx] +=1
    if np.isnan(bodenhoehencountout_array[gy][gx]) == True:
        bodenhoehen_array[gy][gx] = i[2]
    else:
        bodenhoehen_array[gy][gx] = np.mean([bodenhoehen_array[gy][gx],i[2]])

if bodencountout_array[gy][gx] == 0:
    bodencountout_array[gy][gx] +=1


##### Boden interpolation
##Dokumention : "https://modelhelptokyo.wordpress.com/2017/10/25/how-to-interpolate-missing-values-2d-python/"
a = np.arange(0, ncols)
b = np.arange(0, nrows)
#mask invalid values
array = np.ma.masked_invalid(bodenhoehen_array)
xx, yy = np.meshgrid(a, b)
#get only the valid values
x1 = xx[~array.mask]
y1 = yy[~array.mask]
newarr = array[~array.mask]

GD1 = interpolate.griddata((x1, y1), newarr.ravel(),
                          (xx, yy),
                             method='cubic')

print (GD1)

# %%
#-------------------------------
#OutRaster schreiben:
#-------------------------------


#Boden Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/BodenInterpo_%s.tif"  % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
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
#-------------------------------
#OutRaster schreiben:
#-------------------------------


#Boden Raster
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("Export/Bodenhoehe_%s.tif"  % (InputSize), ncols, nrows, 1, gdal.GDT_Float32)
dataset.SetGeoTransform((xmin,1,0,ymax,0,-1))

#Koordinatensystem definieren:
dstSRS = osr.SpatialReference()
dstSRS.ImportFromEPSG(32632)
dest_wkt = dstSRS.ExportToWkt()

dataset.SetProjection(dest_wkt)

#Raster ausgeben:
bandout = dataset.GetRasterBand(1).WriteArray(GD1)
dataset.FlushCache()