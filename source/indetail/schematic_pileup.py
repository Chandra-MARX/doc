'''Generate schematic of a pile-up event
'''
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # import required for projection='3d'

event1 = np.array([[0.0, 0.0, 0.0],
                   [0.0, 1.4, 0.1],
                   [1.0, 0.0, 0.0]])
event2 = np.array([[0.0, 0.0, 0.0],
                   [0.8, 1.3, 0.0],
                   [0.4, 0.0, 0.0]])

xpos = np.arange(3)
ypos = xpos.copy()
xpos, ypos = np.meshgrid(xpos, ypos)
xpos = xpos.flatten()
ypos = ypos.flatten()

z0 = np.zeros_like(event1).flatten()
dx = np.ones_like(z0)
dy = dx.copy()

ind = event1.flatten() > 0

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.bar3d(xpos[ind], ypos[ind], z0[ind], dx[ind], dy[ind], event1.flatten()[ind], color='b', zsort='average', alpha=None)
ind = event2.flatten() > 0
ax.bar3d(xpos[ind], ypos[ind], event1.flatten()[ind], dx[ind], dy[ind], event2.flatten()[ind], color='r', zsort='average', alpha = None)
ax.set_xlim3d(3, 0)
ax.set_ylim3d(0, 3)

ax.set_zlabel('PHA [keV]')
ax.set_xlabel('pixel')
ax.set_ylabel('pixel')
ax.set_title('Piled-up event')
fig.subplots_adjust(0,0,1,1)
