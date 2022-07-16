#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 21:57:26 2022

@author: ee16a2p
"""

import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt


#%%
# P-wave radiation pattern for a horizontal pure DC fault

n = 90 # number of increments of 2*pi

theta = np.linspace(0,np.pi,n)
phi = np.linspace(0,2*np.pi,n)

# define arrays of phi and theta values

theta_full = np.empty((n,n))
phi_full = np.empty((n,n))

for i in range(n):
    theta_full[i,:] = theta
    phi_full[:,i] = phi

#calculate vertical component of P-wave

u_radial = np.empty((n,n))
u_radial_vert = np.empty((n,n))
u_radial_hori = np.empty((n,n))

for i in range(n): #theta
    for j in range(n): #phi
        u_radial[i,j] = np.sin(2*theta[i])*np.cos(phi[j])
        u_radial_vert[i,j] = u_radial[i,j]*np.cos(theta[i])
        u_radial_hori[i,j] = u_radial[i,j]*np.sin(theta[i])


#converting from spherical to cartesian coords
X = []
Y = []
Z = []

R = np.transpose(u_radial_vert) #replace value here with u_radial for P amplitude, or u_radial vert for vertical component only

# scale plot by amplitude

X = R * np.sin(theta_full) * np.cos(phi_full)
Y = R * np.sin(theta_full) * np.sin(phi_full)
Z = R * np.cos(theta_full) 

# layout and plot
min_X = np.min(X)
min_Y = np.min(Y)
max_X = np.max(X)
max_Y = np.max(Y)

layout1 = go.Layout(title="3D Radiation Pattern P-wave", xaxis = dict(range=[min_X,max_X],), yaxis = dict(range=[min_Y,max_Y],))

fig1 = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, surfacecolor=R, colorscale='jet', colorbar = dict(title = "displacement", thickness = 50, xpad = 500))], layout = layout1)

fig1.update_layout(autosize = True, margin = dict(l = 50, r = 50, t = 250, b = 250))

plot(fig1)

