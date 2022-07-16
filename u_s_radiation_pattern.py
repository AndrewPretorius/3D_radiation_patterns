#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 21:54:42 2022

@author: ee16a2p
"""

import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot

# Script to plot 3D radiation patterns from a horizontal pure DC fault

# SH-wave radiation patterns

n = 90

theta = np.linspace(0,np.pi/2,n)
phi = np.linspace(0,2*np.pi,n)

# define arrays of phi and theta values

theta_full = np.empty((n,n))
phi_full = np.empty((n,n))

for i in range(n):
    theta_full[i,:] = theta
    phi_full[:,i] = phi
    
# calculate S-wave radiation pattern amplitude and vertical component

u_s = np.empty((n,n))
u_s_vert = np.empty((n,n))

for t in range(n): #theta
    for p in range(n): #phi
        u_s[t,p] = np.sqrt(((np.cos(2*theta[t])*np.cos(phi[p]))**2)+((np.cos(theta[t])*np.sin(phi[p]))**2))# u_s vector amplitude
        u_s_vert[t,p] = u_s[t,p]*np.cos(theta[t]) # vertical component only
        
#converting from spherical to cartesian coords
X = []
Y = []
Z = []

R = np.transpose(u_s_vert) # replace with u_s for S amplitude, u_theta_vert for vertical component

# scale plot by amplitude

X = R * np.sin(theta_full) * np.cos(phi_full)
Y = R * np.sin(theta_full) * np.sin(phi_full)
Z = R * np.cos(theta_full) 

# layout and plot 
min_X = np.min(X)
min_Y = np.min(Y)
max_X = np.max(X)
max_Y = np.max(Y)

layout2 = go.Layout(title="3d radiation pattern S-wave", xaxis = dict(range=[min_X,max_X],), yaxis = dict(range=[min_Y,max_Y],))

fig2 = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, surfacecolor=R, colorscale='jet', colorbar = dict(title = "Normalised vertical displacement", thickness = 50, xpad = 500))], layout = layout2)

fig2.update_layout(autosize = True, margin = dict(l = 50, r = 50, t = 250, b = 250))

plot(fig2)
