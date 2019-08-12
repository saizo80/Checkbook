# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:51:58 2019

@author: Matthew Thornton

This is the base object for a transaction
"""

class transaction:
    def __init__(self, Type, amount, bt, date, des):
        self.Type = Type
        self.amount = amount
        self.budgetType = bt.replace("\n","")
        self.date = date
        self.description = des
    def toString(self):
        if self.budgetType != "":
            return "{} - {} {} - Amount: ${:.2f}\n{}".format(self.date, self.budgetType, 
                    self.Type, self.amount, self.description)
        else:  
            return "{} - {} - Amount: ${:.2f}\n{}".format(self.date, self.Type, self.amount, self.description)
    def write(self):
        if self.budgetType != "":
            return "{},{:.2f},{},{},{}\n".format(self.Type, self.amount, 
                    self.budgetType, self.date, self.description)
        else:
            return "{},{:.2f},{},{}\n".format(self.Type, self.amount, self.date,self.description)
    
    def getCombo(self):
        return "{} - {} - {} - {:.2f} - {}".format(self.date, self.budgetType, self.Type, self.amount, self.description)
        