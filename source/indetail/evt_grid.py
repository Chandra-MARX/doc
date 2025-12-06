'''Generate schematic of a pile-up event
'''
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # import required for projection='3d'


event1 = np.array([[0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., .01, .01, .01, 0., 0., 0.],
                   [0., 0., .01, 5., 2., 0., 0., 0.],
                   [0., 0., .01, .01, .01, 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.]])
event2 = np.array([[0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 1., 4., 1., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0.]])


xpos = np.arange(8)
ypos = xpos.copy()
xpos, ypos = np.meshgrid(xpos, ypos)
xpos = xpos.flatten()
ypos = ypos.flatten()


z0 = np.zeros_like(event1).flatten()
dx = np.ones_like(z0)
dy = dx.copy()

ind1 = event1.flatten() > 0
ind2 = event2.flatten() > 0

relevantregion = np.zeros((8, 8))
relevantregion[1:6, 1:6] = 1
indrelevant = relevantregion.flatten() > 0


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.bar3d(xpos[indrelevant], ypos[indrelevant], z0[indrelevant],
         dx[indrelevant], dy[indrelevant], 
         relevantregion.flatten()[indrelevant]*1e-4,
         color='y', zsort='average', alpha=None)

ax.bar3d(xpos[ind1], ypos[ind1], z0[ind1], dx[ind1], dy[ind1], event1.flatten()[ind1], color='b', zsort='average', alpha=.7)

ax.bar3d(xpos[ind2], ypos[ind2], event1.flatten()[ind2], dx[ind2], dy[ind2], event2.flatten()[ind2], zsort='average', color='r', alpha=.7)
ax.set_xlim3d(8, 0)
ax.set_ylim3d(0, 8)
ax.set_zlim3d(0, 5)
ax.view_init(29., -71.)
ax.set_zlabel('PHA [keV]')
ax.set_xlabel('pixel')
ax.set_ylabel('pixel')
fig.subplots_adjust(0,0,1,1)
