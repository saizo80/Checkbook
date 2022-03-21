from Transaction import Transaction as tran
from Budget import Budget as bug
import os, subprocess
from datetime import datetime, date
from tkinter import messagebox


class Functions():
    def __init__(self, month):
        self.counter = 1
        self.transactions = []
        self.budgets = {}
        self.date = None
        self.balance = 0
        
        self.startup()
        self.sortDates()
        """
        if self.date != month:
            self.changeMonth(month)
        """
            
        
    def startup(self):
        os.chdir(os.path.dirname(__file__))
        try:
            with open("budgets.cfg", "r") as f:
                for line in f:
                    if line != "":
                        temp = line.split(",")
                        self.createBudget(temp[0], float(temp[1].strip()), 0)
        except:
            messagebox.showinfo("Error", "Budgets file not found. File will be created.")
            with open("budgets.cfg", "w+") as f:
                pass

        try:
            with open("transactions.cfg", 'r') as f:
                tempCounter = 0
                for line in f:
                    if tempCounter == 0:
                        self.date = line.split(",")[0]
                        self.balance = float(line.split(",")[1])
                        tempCounter += 1
                    else:
                        temp = line.split(",")
                        self.createTransaction(float(temp[0]), temp[1], temp[2], temp[3])
        except:
            messagebox.showinfo("Error", "Transactions file not found. File will be created.\nPlease enter balance.")
            with open("transactions.cfg", "w+") as f:
                f.write("{}".format(date.today().strftime('%b-%y')))
        
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
        if date != "":
            transaction.date = date
            self.sortDates()
        if budget != "0":
            self.budgets.get(transaction.budget).current -= transaction.amount
            transaction.budget = budget
            self.budgets.get(transaction.budget).current += transaction.amount
        if amount != "":
            self.budgets.get(transaction.budget).current -= transaction.amount
            self.balance -= transaction.amount
            transaction.amount = float(amount)
            self.balance += transaction.amount
            self.budgets.get(transaction.budget).current += transaction.amount
        if descrip != "\n":
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
                
    def writeBudgets(self):
        with open("budgets.cfg", 'w') as f:
            for i in self.budgets:
                f.write("{},{}\n".format(self.budgets.get(i).name, self.budgets.get(i).cap)) 
    
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

    def editBudget(self, budget, name, cap):
        for i in self.budgets:
            if self.budgets.get(i).name == budget:
                temp = self.budgets.get(i)
        if name != "":
            temp.name = name
        if cap != "":
            temp.cap = float(cap)
        self.writeBudgets()
    
    def removeBudget(self, name):
        temp = self.budgets.get(name)
        
        for i in self.transactions:
            if i.budget == temp.name:
                i.budget = "None"
                self.budgets.get("None").current += i.amount
        self.budgets.pop(name)
        self.writeBudgets()
    
    def createNewBudget(self, name, cap):
        self.createBudget(name, float(cap), 0)
        self.writeBudgets()
        
    def changeMonth(self, date):
        # Write all the transactions to a file
        if not os.path.exists("old-transactions"):
            subprocess.call(['mkdir', 'old-transactions'])
        subprocess.call(['mv', 'transactions.cfg', 'old-transactions/transactions{}.cfg'.format(self.date)])
        # Remove all transactions from the list
        self.transactions = []
        
        # Create new transactions file
        with open("transactions.cfg", "w+") as f:
            f.write("{},{:.2f}".format(date, self.balance))
        
        # Rewrite the budgets file
        amount = 0.0
        with open("budgets.cfg",'w') as f:
            for i in range(len(self.budgets)):
                if self.budgets.get(i).name != "Other":
                    f.write("{},{:.2f}\n".format(self.budgets[i].name, 
                        self.budgets[i].cap))
                    if self.budgets[i].cap - self.budgets[i].current != 0:
                        amount += (self.budgets[i].limit - self.budgets[i].current)
                        
            f.write("{},{:.2f}\n".format('Other',
                            self.budgets.get('Other').current + amount))