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

n = 90
#%%
# calculate P-wave radiation pattern amplitude and vertical and horizontal components

theta = np.linspace(0,2*np.pi,n)
phi = np.linspace(0,2*np.pi,n)

# define arrays of phi and theta values

theta_full = np.empty((n,n))
phi_full = np.empty((n,n))

for i in range(n):
    theta_full[i,:] = theta
    phi_full[:,i] = phi

u_radial = np.empty((n,n))
u_radial_vert = np.empty((n,n))
u_radial_hori = np.empty((n,n))

for i in range(n): #theta
    for j in range(n): #phi
        u_radial[i,j] = np.sin(2*theta[i])*np.cos(phi[j]) # displacement mplitude
        u_radial_vert[i,j] = u_radial[i,j]*np.cos(theta[i]) # vertical component
        u_radial_hori[i,j] = u_radial[i,j]*np.sin(theta[i]) # horizontal component

#%%
# calculate S-wave radiation pattern amplitude and vertical and horizontal components

theta = np.linspace(0,np.pi,n)
phi = np.linspace(0,2*np.pi,n)

# define arrays of phi and theta values

theta_full = np.empty((n,n))
phi_full = np.empty((n,n))

for i in range(n):
    theta_full[i,:] = theta
    phi_full[:,i] = phi

u_s = np.empty((n,n))
u_s_vert = np.empty((n,n))
u_s_hori = np.empty((n,n))

for t in range(n): #theta
    for p in range(n): #phi
        u_s[t,p] = np.sqrt(((np.cos(2*theta[t])*np.cos(phi[p]))**2)+((np.cos(theta[t])*np.sin(phi[p]))**2))# displacement amplitude
        u_s_vert[t,p] = u_s[t,p]*np.sin(theta[t]) # vertical component only
        u_s_hori[t,p] = u_s[t,p]*np.cos(theta[t]) # horizontal component only
        
# ratio between vertical component of P and S waves

P_S_vert_ratio = np.empty((n,n))
P_S_hori_ratio = np.empty((n,n))
P_S_ratio = np.empty((n,n))

for t in range(n): #theta
    for p in range(n): #phi
        P_S_vert_ratio[t,p] = u_radial_vert[t,p]/u_s_vert[t,p]
        P_S_hori_ratio[t,p] = u_radial_hori[t,p]/u_s_hori[t,p]
        P_S_ratio[t,p] = u_radial[t,p]/u_s[t,p]
    
#converting from spherical to cartesian coords
X = []
Y = []
Z = []

# scale plot by amplitudes - change here to change between total, horizontal, or vertical components

#R = np.transpose(P_S_vert_ratio) 
#R = np.transpose(P_S_hori_ratio)
R = np.transpose(P_S_ratio)

# scale plot by amplitude

X = R * np.sin(theta_full) * np.cos(phi_full)
Y = R * np.sin(theta_full) * np.sin(phi_full)
Z = R * np.cos(theta_full) 

# layout and plot 
min_X = np.min(X)
min_Y = np.min(Y)
max_X = np.max(X)
max_Y = np.max(Y)

layout2 = go.Layout(title="Ratio of P and S wave amplitudes", xaxis = dict(range=[min_X,max_X],), yaxis = dict(range=[min_Y,max_Y],))

fig2 = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, surfacecolor=R, colorscale='jet', colorbar = dict(title = "Ratio", thickness = 50, xpad = 500))], layout = layout2)

fig2.update_layout(autosize = True, margin = dict(l = 50, r = 50, t = 250, b = 250))

plot(fig2)
