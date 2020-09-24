from Transaction import Transaction as tran
from Budget import Budget as bug
import os

class Functions():
    def __init__(self):
        self.counter = 1
        self.transactions = []
        self.budgets = {}
        self.date = None
        self.balance = 0
        
        self.startup()
        
    def startup(self):
        os.chdir(os.path.dirname(__file__))
        try:
            with open("budgets.cfg", "r") as f:
                for line in f:
                    temp = line.split(",")
                    self.createBudget(temp[0], float(temp[1]), 0)
        except:
            print("Budgets file not found.")

        try:
            with open("transactions.cfg", 'r') as f:
                tempCounter = 0
                for line in f:
                    if tempCounter is 0:
                        self.date = line
                    else:
                        temp = line.split(",")
                        self.createTransaction(float(temp[0]), temp[1], temp[2], temp[3])
                    tempCounter += 1
        except:
            print("Transaction File Missing")
            
        
    def jam(self, label):
        label.config(text="Button clicked {} times".format(self.counter))
        self.counter += 1
        
    def kill(self):
        exit()
        
    def createTransaction(self, amount, budget, date, descrip):
        self.transactions.append(tran(amount, budget, date, descrip))
        self.budgets.get(budget).current += amount
        
    def createBudget(self, name, cap, current):
        self.budgets[name] = bug(name, cap, current)
    
    def transReport(self):
        roll = ""
        for x in self.transactions:
            roll += "{}\n".format(x.toString())
        return roll
    
    def bugReport(self):
        roll = ""
        for x in self.budgets:
            roll += "{}\n".format(self.budgets.get(x).toString())
        return roll
    
    def getTransactions(self):
        display = ""
        divide = "__________________\n"
        for i in range(len(self.transactions)):
            display += "{}\n{}\n".format(self.transactions[i].toString(), divide)
        display += "\nCurrent Balance: ${:.2f}".format(self.balance)
        
        return display