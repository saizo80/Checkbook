from Transaction import Transaction as tran
from Budget import Budget as bug
import os
from datetime import datetime

class Functions():
    def __init__(self):
        self.counter = 1
        self.transactions = []
        self.budgets = {}
        self.date = None
        self.balance = 0
        
        self.startup()
        self.sortDates()
        
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
                        self.date = line.split(",")[0]
                        self.balance = float(line.split(",")[1])
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
    
    def addTransaction(self, amount, budget, date, descrip):
        self.transactions.append(tran(amount, budget, date, descrip))
        self.budgets.get(budget).current += amount
        self.balance += amount
        self.sortDates()
        self.writeTransactions()
        
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
    
    def getTransactionsCombo(self):
        buffer = []
        for i in range(len(self.transactions)):
            buffer.append(self.transactions[i].getCombo())
        return buffer
    
    def sortDates(self):
        for i in range(len(self.transactions)):
            self.transactions[i].date = datetime.strptime(self.transactions[i].date, "%m-%d-%y")
        
        self.transactions.sort(key=lambda r: r.date)
        
        for i in range(len(self.transactions)):
            self.transactions[i].date = self.transactions[i].date.strftime("%m-%d-%y")
    
    def comboboxReturn(self, data):
        buffer = data.split(" - ")
        date = buffer[0]
        budgetType = buffer[1]
        amount = float(buffer[2])
        description = buffer[3]
        
        for i in range(len(self.transactions)):
            if self.transactions[i].date == date:
                if self.transactions[i].budget == budgetType:
                    if self.transactions[i].amount == amount:
                        if self.transactions[i].descrip == description:
                            return self.transactions[i]
    
    def editTransaction(self, date, budget, amount, descrip, data):
        transaction = self.comboboxReturn(data)
        if date is not "":
            transaction.date = date
            self.sortDates()
        if budget is not "0":
            self.budgets.get(transaction.budget).current -= transaction.amount
            transaction.budget = budget
            self.budgets.get(transaction.budget).current += transaction.amount
        if amount is not "":
            self.budgets.get(transaction.budget).current -= transaction.amount
            self.balance -= transaction.amount
            transaction.amount = float(amount)
            self.balance += transaction.amount
            self.budgets.get(transaction.budget).current += transaction.amount
        if descrip is not "\n":
            transaction.descrip = descrip.strip() 
        self.writeTransactions()   
    
    def removeTransaction(self, data):
        transaction = self.comboboxReturn(data)
        self.budgets.get(transaction.budget).current -= transaction.amount
        self.balance -= transaction.amount
        self.transactions.remove(transaction)
        self.sortDates()
        self.writeTransactions()
        
    def writeTransactions(self):
        with open("transactions.cfg", "w") as f:
            f.write("{},{:.2f}".format(self.date,self.balance))
            for x in self.transactions:
                f.write("\n{:.2f},{},{},{}".format(x.amount, x.budget,
                                            x.date, x.descrip))   
    
    def getBudgets(self):
        display = ""
        divide = "___________________\n"
        for i in self.budgets:
            display += "{}\n{}\n".format(self.budgets.get(i).report(), divide)
        return display 
    
    def budgetsCombo(self):
        buffer = []
        for i in self.budgets:
            buffer.append(i)
        return buffer