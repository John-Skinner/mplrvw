import numpy as np
import matplotlib.pyplot as plt
import nrrd
import sys

exam="hi"
std="hello"
scpcroot = "C:/Users/rayon/Documents/GitHub/mplrvw/scpc"


matlabCompare = False


data, header = nrrd.read(scpcroot + '/myMean0.nrrd')
data = np.transpose(np.squeeze(data,2))
width = data.shape[1]
height = data.shape[0];
profileCoord = int(data.shape[0]/2)-20
corData,corHeader = nrrd.read(scpcroot + '/my_finalCorrection.nrrd')
corData = np.transpose(np.squeeze(corData,2))
maskData, maskHeader = nrrd.read(scpcroot + '/myStaticMask.nrrd')
maskData = np.transpose(np.squeeze(maskData,2))
if matlabCompare:
    mlCordata,mlCorHeader = nrrd.read(scpcroot + '/ml_finalCorrection.nrrd')
    mlCordata = np.transpose(np.squeeze(mlCordata,2))
    mlCorProfile = mlCordata[:,profileCoord]


meanProfile = data[profileCoord,:].flatten()
u = meanProfile.flatten()
corProfile = corData[profileCoord,:].flatten()
maskProfile = maskData[profileCoord,:].flatten()
horizontalProfile = list()
widthTrack = list()
for i in np.arange(0, width):
    if maskProfile[i] == 1:
        horizontalProfile.append(meanProfile[i])
        widthTrack.append(i)

testProfile = data[:,profileCoord].flatten()
testMask = maskData[:,profileCoord].flatten()
corTest = corData[:,profileCoord].flatten()
testList = list()
testTrack = list()
for i in np.arange(0,height):
    if testMask[i] == 1:
        testList.append(meanProfile[i])
        testTrack.append(i)
        


t=np.arange(1,width+1)
h=np.arange(1,height+1)
profileplot = np.empty(width)
profileplot[:] = profileCoord

fig1, axes = plt.subplots( nrows=2, ncols=2, constrained_layout=True,figsize=(15,18))
fig1.suptitle(exam)
axes[0, 1].scatter(widthTrack,horizontalProfile,s=15,c=(1,0,0))
axes[0, 1].plot(t,corProfile)
if matlabCompare:
    axes[0, 1].plot(t,mlCorProfile)
axes[0, 1].set_xlim(1,width)
axes[0, 1].set_ylim(-1000,1000)
axes[1, 0].scatter(testTrack,testList, s=15, c=(1,0,0))
axes[1, 0].plot(t, corTest)
axes[1, 0].set_ylim(-1000,1000)
maskData = np.mod(maskData+1,2)
axes[0, 1].set_title('Fitting to Profile Curve')
axes[1, 1].imshow(data,cmap=plt.cm.gray,interpolation="none", aspect = 'equal')
axes[1, 1].imshow(maskData,cmap=plt.cm.Set1,interpolation='none',aspect='equal',alpha=0.2)
axes[1, 1].set_title('Mean of Phase Image (Static Tissue in Red')
axes[1, 1].plot(t,profileplot)
axes[1, 1].plot(profileplot, h)
axes[0, 0].set_visible(False)

plt.show()
