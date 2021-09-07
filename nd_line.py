# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:07:13 2021

@author: dpm42
"""

import numpy as np
from scipy.spatial import distance
import sys
from scipy.interpolate import splev, splprep

class nd_line():
    def __init__(self,points,inplace = False):
        self.points = np.array([tuple(x) for x in points])
        self.length = self._length(points)
        self.type = 'linear'
    def _length(self,points):
        'calculate the length (sum of the euclidean distance between points)'
        return  sum([distance.euclidean(points[i],points[i+1]) for i in range(len(points)-1)])
    def interp(self,dist):
        'return a point a specified distance along the line'
        if dist>self._length(self.points): sys.exit('length cannot be greater than line length')
        i=0
        d=0
        while d<dist:
            #can def make this more efficient with np.cumsum
            i+=1
            d+=distance.euclidean(self.points[i-1],self.points[i])
        last_point_dist = distance.euclidean(self.points[i-1],self.points[i])
        d-=last_point_dist
        vector = (self.points[i]-self.points[i-1])/last_point_dist
        remdist = dist-d
        final_point = remdist*vector+self.points[i-1]
        check = self.points.copy()[0:i+1]
        check[i] = final_point
        if abs(self._length(check)/dist-1)>.001: sys.exit('Something is wrong')
        return(final_point)
    def splineify(self,samples = None):
        'Turn line into a spline approximation, currently occurs in place'
        if samples is None: samples = len(self.points)
        tck,u = splprep([self.points[:,0],self.points[:,1]])
        self.points = np.transpose(splev(np.linspace(0,1,num=samples),tck))
        self.length = self._length(self.points)
        self.type = 'spline'