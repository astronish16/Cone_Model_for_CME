#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 21:58:38 2021

@author: astronish

"""

""" 
This code is for determine the CME parameters using Cone Model
describe in Xie et al 2004

"""


#%%

" Import necessary Module Here "

import numpy as np
import math
import matplotlib.pyplot as plt
from sunpy.io import read_file
from datetime import datetime as T
from astropy.coordinates import SkyCoord
from sunpy.sun import constants
from sunpy.coordinates import frames
import sunpy.map
from skimage.measure import EllipseModel
from matplotlib.patches import Ellipse,Circle
import cv2


#%%

" Import all data files here."

### C2 frames

data0,header0=read_file('2011_08_04__04_00_06_088__SOHO_LASCO_C2_white-light.jp2')[0] # frame to make runnig difference image for 1st observation
data1,header1=read_file('2011_08_04__04_12_05_780__SOHO_LASCO_C2_white-light.jp2')[0] # very 1st observation of CME in C2 starts from here
data2,header2=read_file('2011_08_04__04_24_38_472__SOHO_LASCO_C2_white-light.jp2')[0]
data3,header3=read_file('2011_08_04__04_36_05_763__SOHO_LASCO_C2_white-light.jp2')[0]

### C3 frames

data5,header5=read_file('2011_08_04__04_18_05_875__SOHO_LASCO_C3_white-light.jp2')[0]  # frame to make runnig difference image for 1st observation
data6,header6=read_file('2011_08_04__04_42_05_760__SOHO_LASCO_C3_white-light.jp2')[0] # very 1st observation of CME in C3 starts from here
data7,header7=read_file('2011_08_04__05_06_06_843__SOHO_LASCO_C3_white-light.jp2')[0]
data8,header8=read_file('2011_08_04__05_30_06_727__SOHO_LASCO_C3_white-light.jp2')[0]
data9,header9=read_file('2011_08_04__05_54_05_910__SOHO_LASCO_C3_white-light.jp2')[0]
data10,header10=read_file('2011_08_04__06_06_05_801__SOHO_LASCO_C3_white-light.jp2')[0]
data11,header11=read_file('2011_08_04__06_18_06_693__SOHO_LASCO_C3_white-light.jp2')[0]

#%%  

" Produce Running Difference Image to enhance moving feature of CME"

ni=data11.copy()       #current image
ni_1=data10.copy()     #previous image

hi=header11.copy()     #current image metadata
hi_1=header10.copy()   #previous image metadata

DI=ni-ni_1

######################################################################
######### Running Difference Image as per Olmedo et al 2008 ##########
######################################################################

time2=T.strptime(hi['TIME_OBS'], "%H:%M:%S.%f").time()
time1=T.strptime(hi_1['TIME_OBS'], "%H:%M:%S.%f").time()

#time and time difference in minutes
t2= (time2.hour * 60)+ (time2.minute) + (time2.second /60.0)
t1= (time1.hour * 60)+ (time1.minute) + (time1.second /60.0)
deltat=t2-t1

alpha=15.0

DI1=(ni- (ni_1*np.mean(ni)/np.mean(ni_1)))*alpha/deltat

###############################################################
###### Running Difference Image using Sunpy.map module  #######
###############################################################

DI2=sunpy.map.Map(ni * 1.0 -ni_1 * 1.0, hi).data

" Use any of above Running Difference Image further as per convinient "

img = DI.copy()                # chage to DI1.copy() & vice-versa
img=img.astype(np.float32)
img[img<0]=0.0


#%%

delta=np.arange(0,360,1)  # free parameter need be use in parametic equation of ellipse
delta=np.deg2rad(delta)

" Solar center & relation between pixel to solar radius"

Sx=hi['CRPIX1']
Sy=hi['CRPIX2']

#################################################################
######### Solar Radius to Pixel conversion using Sunpy.map ######
##################################################################

date=hi['DATE_OBS']
aa=sunpy.map.Map(ni,hi)
print(aa.coordinate_frame)

coord = SkyCoord(0 * constants.radius, 0 * constants.radius, 0 * constants.radius,
                  frame=frames.Heliocentric,observer=aa.observer_coordinate,
                  obstime=date, representation_type='cartesian' )
coord1 = SkyCoord(1 * constants.radius, 0*constants.radius, 0 * constants.radius,
                  frame=frames.Heliocentric,observer=aa.observer_coordinate,
                  obstime=date, representation_type='cartesian')



r1=aa.world_to_pixel(coord)[0].value
r2=aa.world_to_pixel(coord1)[0].value

R_sun=np.abs(r2-r1)


Detector=hi["DETECTOR"]

if Detector=='C3':
    R_disk=3.7*R_sun
else:
    R_disk=2.0*R_sun

#%%  

"""
 Actual part of code which determine the CME parameters.
 Since we want to fit ellipse on halo projected in POS,
 we need to select atleast 5 points on CME leading edge but we will select
 around 30 to 40 points for better accuracy.
"""


### obtain data ponts for fit elipse 

X = []
Y = []


 
 
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):                                 
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        X.append(x)
        Y.append(y)
        #color = (0, 0, 155) 
        #cv2.circle(DI, (x, y), 1, color, thickness=-1)            
        #cv2.putText(DI, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, color, thickness=1)
        cv2.imshow("CME", DI)
        
       
 
 
cv2.namedWindow("CME",cv2.WINDOW_NORMAL)
cv2.resizeWindow('CME', 1000,900)
cv2.setMouseCallback("CME", on_EVENT_LBUTTONDOWN)
cv2.imshow("CME",DI)
cv2.waitKey(0)
cv2.destroyWindow('CME')

# Fit ellipse and plot it on Image

B=[]

i=0
while (i<len(X)):       # convert those X & Y array into point pair.
    A=(X[i],Y[i])
    B.append(A)
    i=i+1

    
a_points = np.array(B)    # Those point pair is required to fit ellipse.
x = a_points[:, 0]
y = a_points[:, 1]

ell = EllipseModel()
ell.estimate(a_points)

xc, yc, a, b, alpha = ell.params


print("Ellipse parameter:")
print("center = ",  (xc, yc))
print("axes = ", (a,b))
print("angle of rotation for minor axis (alpha) = ", (alpha*180/np.pi))

if a>b:
    print("Cone fitting is not good according to cone model ")
else:
    pass

print("===========================================================")
    

def CME(h,k,a,b,alpha):            # function to determine geomatrical parameter of CME
    Theta=(math.asin(a/b))         # using formula given in Xie et al 2004.
    Omega=(math.atan((b*math.cos(Theta))/np.abs((h-Sx))))
    p=math.cos(Theta)*math.cos(alpha)
    q=math.cos(Theta)*math.sin(alpha)
    t=math.sin(Theta)
    Lambda=math.atan(q/np.sqrt(p**2.0 + t**2.0))
    Phi=math.atan(p/t)
    r_dis=b/math.sin(Omega)
    return Theta,Omega,Lambda,Phi,r_dis


cme=CME(xc,yc,a,b,alpha)
print("CME Parameters according to Cone Model: (Angles are in degree)")
print("Cone Axis projection in POS (theta) = "+str(math.degrees(cme[0])))
print("Angular half-width of Cone = " + str(math.degrees(cme[1])))
print("Latitude = "+ str(math.degrees(cme[2])))
print("Longitude = "+ str(math.degrees(cme[3])))
print("Radial Distance = "+ str(cme[4]/R_sun)+ " R_sun unit.")

#%%  



Xp=xc-a*np.cos(alpha)*np.sin(delta) -b*np.sin(alpha)*np.cos(delta)
Yp=yc-a*np.sin(alpha)*np.sin(delta) +b*np.cos(alpha)*np.cos(delta)

dist=np.sqrt((Sx-Xp)**2.0+ (Sy-Yp)**2.0)
print("=================================================")
print("Average radial distance in LASCO FOV is " +str(np.mean(dist)/R_sun) + " R_sun unit")
print("Farthest point of CME leading edge in LASCO FOV is " + str(np.max(dist)/R_sun)+ " R_sun unit")

plt.figure(figsize=(10,10))
ax = plt.gca()

ellipse = Ellipse(xy=(xc,yc), width=2*a, height=2*b, angle=alpha*180/np.pi, edgecolor='r', fc='None', lw=2)
ax.add_patch(ellipse)
ax.plot(xc,yc,'ro')


ax.plot(Sx,Sy,"y*")
disk=Circle(xy=(Sx,Sy),radius=R_disk,edgecolor='b',fc='None')
ax.add_patch(disk)

sun=Circle(xy=(Sx,Sy),radius=R_sun,edgecolor='y',fc='None')
ax.add_patch(sun)


ax.imshow(DI,origin="lower",cmap="gray")
plt.title(str(hi['TELESCOP'])+" "+str(hi['INSTRUME'])+" "+str(hi['DETECTOR'])+' '+str(hi['TIME_OBS']))
plt.show()
