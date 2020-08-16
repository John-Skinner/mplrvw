import numpy as np
import matplotlib.pyplot as plt
import nrrd
import sys

exam=sys.argv[1]
std=sys.argv[2]


matlabCompare = False


data, header = nrrd.read('/tmp/scpc/myMean0.nrrd')
data = np.transpose(np.squeeze(data,2))
width = data.shape[1]
profileCoord = int(data.shape[0]/2)-20
corData,corHeader = nrrd.read('/tmp/scpc/my_finalCorrection.nrrd')
corData = np.transpose(np.squeeze(corData,2))
maskData, maskHeader = nrrd.read('/tmp/scpc/myStaticMask.nrrd')
maskData = np.transpose(np.squeeze(maskData,2))
if matlabCompare:
    mlCordata,mlCorHeader = nrrd.read('/tmp/scpc/ml_finalCorrection.nrrd')
    mlCordata = np.transpose(np.squeeze(mlCordata,2))
    mlCorProfile = mlCordata[:,profileCoord]


meanProfile = data[profileCoord,:].flatten()
u = meanProfile.flatten()
corProfile = corData[profileCoord,:].flatten()
maskProfile = maskData[profileCoord,:].flatten()
meanProfile = np.multiply(maskProfile,meanProfile)


t=np.arange(1,width+1)
profileplot = np.empty(width)
profileplot[:] = profileCoord

fig1, axes = plt.subplots( nrows=2, ncols=1, constrained_layout=True,figsize=(5,8))
fig1.suptitle(exam)
axes[0].scatter(t,meanProfile,s=0.5,c=(1,0,0))
axes[0].plot(t,corProfile)
if matlabCompare:
    axes[0].plot(t,mlCorProfile)
axes[0].set_xlim(1,width)
maskData = np.mod(maskData+1,2)
axes[0].set_title('Fitting to Profile Curve')
axes[1].imshow(data,cmap=plt.cm.gray,interpolation="none", aspect = 'equal')
axes[1].imshow(maskData,cmap=plt.cm.Set1,interpolation='none',aspect='equal',alpha=0.2)
axes[1].set_title('Mean of Phase Image (Static Tissue in Red')
axes[1].plot(t,profileplot)

plt.show()