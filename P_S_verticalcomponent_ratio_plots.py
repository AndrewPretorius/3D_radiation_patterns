#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 21:51:52 2022

@author: ee16a2p
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation
from matplotlib import cm

n = 100
x = 1000
z = np.linspace(300,-700,1000)

phi = np.linspace(0,2*np.pi,37)
phi_deg = np.rad2deg(phi)
theta = np.arctan(x/z)

A_fp = np.empty((len(theta),len(phi)))
A_fp_zhat = np.empty((len(theta),len(phi)))
A_fs = np.empty((len(theta),len(phi)))
A_fs_zhat = np.empty((len(theta),len(phi)))

#%%
# measured P and S ratio

p_amps = np.load('p_amps_smoothed.npy')
s_amps = np.load('s_amps_smoothed.npy')

# add artificial shift to make crossover point of amplitude profiles at (0,0)
x_shift= np.full((50),-0.043204)
y_shift = np.full((50),3.3647)

p_s_ratio_measured = (p_amps)/(s_amps)
p_s_ratio_measured_shift = (p_amps+x_shift)/(s_amps+x_shift)
depth = np.linspace(300,-700,50)
depth_20 = depth+y_shift
"""
plt.plot(p_s_ratio_measured,depth_20)
plt.plot(s_amps,depth_20)
plt.plot(p_amps,depth_20)

plt.plot(p_amps+x_shift,depth_20+y_shift)
#plt.plot(s_amps+x_shift,depth_20+y_shift)
"""


#%%

# p and s wave ratio

for t in range(len(theta)):
    for p in range(len(phi)):
        A_fp[t,p] = np.sin(2*theta[t])*np.cos(2*phi[p])
        A_fp_zhat[t,p] = A_fp[t,p]*np.cos(theta[t])
        A_fs[t,p] = np.sqrt(((np.cos(2*theta[t])*np.cos(phi[p]))**2)+((np.cos(theta[t])*np.sin(phi[p]))**2))
        A_fs_zhat[t,p] = A_fs[t,p]*np.sin(theta[t])
        
f_z_phi_vert = A_fp_zhat/A_fs_zhat # ratio between vertical amplitudes of p and s waves
f_z_phi = A_fp/A_fs # ratio between vertical amplitudes of p and s waves

fig1, ax1 = plt.subplots(1, 1, figsize = (6, 6))

col=cm.get_cmap('jet', len(phi))


#def animate_f(i):    # for animated plot
for i in range(len(phi)):     # for static plot
    #ax1.cla()
    ax1.plot(p_s_ratio_measured_shift,depth_20, c='k')
    ax1.plot(f_z_phi_vert[:,i],z,label="phi = "+str(int(phi_deg[i]))+" degrees",c=col(i/len(phi)))
    ax1.set_ylim([-700, 300]) # fix the x axis
    ax1.set_xlim([-3, 3]) # fix the y axis
    plt.ylabel('z')
    plt.xlabel('f(z,phi)')
    plt.title("P and S vertical component ratio f(z,phi), 0<phi<360 degrees ")
    #plt.colorbar()
    plt.legend()
    
#nim1 = animation.FuncAnimation(fig1, animate_f, frames = len(phi) + 1, interval = 80, blit = False)
plt.show()



