# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:39:05 2019

@author: Matthew Thornton

This file will contain all of the different budget classes

Maybe I could do the budgets as one template and make them by reading them
from the file -- That was a good idea!
"""
class Budget:
    def __init__(self, limit, name):
        self.limit = float(limit)
        self.current = 0.0
        self.name = name
    def add(self, c):
        self.current += c
    def report(self):
        return ("{}:\nLimit: ${:.2f}\nCurrent: ${:.2f}\nPercentage: "
            "{:.2f}%\nRemaining: ${:.2f}".format(self.name, self.limit, 
             self.current, (self.current/self.limit)*100, 
             self.limit-self.current))