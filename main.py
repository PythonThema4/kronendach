import numpy as np



fobj = open('/run/media/csav9726/ANDREAS/Python/Projekt/15.01/kronendach/Daten/Waldpunktwolke_short.txt', "r")
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


#Neuer Array ohne Gebauede und Boden


vegetationslist = []

for i in pointarray:
        
        if i[6] == 3 or i[6] ==4 or i[6] ==5:
                vegetationslist.append(i)
                

#print vegetationslist
vegetationsarray = np.array(vegetationslist)
print vegetationsarray
        



#print pointlist
print "--------"

#max values
maxvals = np.amax(pointarray,axis=0) 
xmax=maxvals[0]
ymax=maxvals[1]
print "xmax:",xmax
print "ymax:",ymax
#min values
minvals = np.amin(pointarray,axis=0) 
xmin=minvals[0]
ymin=minvals[1]
print "xmin:",xmin
print "ymin:",ymin
#ratio
nrows= np.ceil(ymax-ymin)
ncols= np.ceil(xmax-xmin)

print nrows
print ncols
#create Extent Raster
array = np.empty(nrows,ncols)

# for x in np.arange(xmin,xmin+ncols):
#     print x
#     for y in np.arange(ymin,ymin+nrows):
#         print y
        

