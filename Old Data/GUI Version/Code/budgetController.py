# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:19:10 2019

@author: Matthew Thornton

This will be the budget controller, one level deeper than the driver
"""
from transaction import transaction
import budgets
import os
import traceback
import paramiko
from datetime import datetime

class budgetController:
    def __init__(self):
        self.transactions = []
        self.budgets = []
        self.__transactionFile = "/transactions.txt"
        self.budgetsFile = "/budgets.txt"
        self.__current_dir = os.path.dirname(os.path.realpath(__file__))
        self.balance = 0.0
        self.stored_date = ""
        
        self.__remoteTransactionPath = ""
        self.__remoteBudgetPath = ""
        self.__ip = ""
        self.__port = 0
        self.__user = ""
        self.__passwd = ""
        self.__oldRemotePath = ""
        
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    def setBalance(self, amount):
        self.__balance = amount
    
    def cantFindDate(self):
        print ("The date could not be found.\nPlease enter the date for this"
               " period in the format Aug-19:")
        self.stored_date = input() 
    
    def cantFindBalance(self):
        print ("The Balance could not be found.")
        try:
            self.balance = float(input("Please Enter your"
                                                     " current Balance: "))
        except:
            print ("Incorrect Input.")
            return self.cantFindBalance()
    def loadTransactions(self):
        gotBalance = False
        try:
            with open(self.__current_dir + self.__transactionFile, "r") as f:
                try:
                    self.balance = float(f.readline())
                except Exception as e:
                    print (e)
                    traceback.print_exc()
                else:
                    gotBalance = True
                for line in f:
                    if ',' not in line:
                        if '-' in line and '.' not in line:
                            self.stored_date = line
                            if self.stored_date == "":
                                self.cantFindDate()
                       
                    elif 'Deposit' not in line:
                        tokens = line.split(',')
                        self.transactions.append(transaction(tokens[0],
                            float(tokens[1]),tokens[2], tokens[3], tokens[4].replace("\n","")))
                        Type = tokens[2].replace("\n","")

                        for i in range(len(self.budgets)):
                            if Type == self.budgets[i].name:
                                self.budgets[i].add(float(tokens[1]))
                    else:
                        tokens = line.split(",")
                        self.transactions.append(transaction(tokens[0],
                                float(tokens[1]),"",tokens[2], tokens[3].replace("\n","")))
                if not gotBalance:
                    self.cantFindBalance()
        except Exception as e:
            print (e)
            traceback.print_exc()
            input("Press Enter to Close.")
            exit()
            
    def loadBudgets(self):
        self.getFiles()
        try:
            with open(self.__current_dir + self.budgetsFile,'r') as f:
                for line in f:
                    tokens = line.split(',')
                    self.budgets.append(budgets.Budget(float(tokens[1]), tokens[0]))
        except Exception as e:
            print (e)
            traceback.print_exc()
            input("Press Enter to Close.")
            exit()
        
    def getTransactions(self):
        display = ""
        divide = "__________________\n"
        for i in range(len(self.transactions)):
            display += "{}\n{}\n".format(self.transactions[i].toString(), divide)
        display += "\nCurrent Balance: ${:.2f}".format(self.balance)
        
        return display
    
    def getBudgets(self):
        display = ""
        divide = "___________________\n"
        for i in range(len(self.budgets)):
            display += "{}\n{}\n".format(self.budgets[i].report(), divide)
        return display
    
    def addTransaction(self, Type, amount, budgetChoice, date, des):
        self.transactions.append(transaction(Type, amount, budgetChoice, date, des))
        print ("Transaction added.")
        if budgetChoice != "":
            for i in range(len(self.budgets)):
                if budgetChoice == self.budgets[i].name:
                    self.budgets[i].add(amount)
            
            
        if 'Purchase' in Type:
            self.balance -= amount
        else:
            self.balance += amount
        
        
    def removeTransaction(self, transaction):
        buffer = transaction.split(" - ")
        date = buffer[0]
        budgetType = buffer[1]
        amount = float(buffer[3])
        description = buffer[4]
        
        for i in range(len(self.transactions)):
            if self.transactions[i].date == date:
                #print ("date success")
                if self.transactions[i].budgetType == budgetType:
                    #print ("budget type success")
                    if self.transactions[i].amount == amount:
                        #print ('amount success')
                        if self.transactions[i].description == description:
                            #print ('description success')
                            bufferOb = self.transactions[i]
                            if 'Purchase' in bufferOb.Type:
                                self.balance += bufferOb.amount
                                
                                for j in range(len(self.budgets)):
                                    if self.budgets[j].name == bufferOb.budgetType:
                                        self.budgets[j].current += (bufferOb.amount - (bufferOb.amount *2))
                            else:
                                self.balance -= bufferOb.amount
                            
                            self.transactions.pop(i)
                            break
    
    def changeBudget(self, index, newLimit):
        self.budgets[index].limit = newLimit
    
    def changeTranDate(self, transaction, newDate):
        buffer = transaction.split(" - ")
        date = buffer[0]
        budgetType = buffer[1]
        amount = float(buffer[3])
        description = buffer[4]
        
        for i in range(len(self.transactions)):
            if self.transactions[i].date == date:
                if self.transactions[i].budgetType == budgetType:
                    if self.transactions[i].amount == amount:
                        if self.transactions[i].description == description:
                            self.transactions[i].date = newDate
                            break
        self.sortDates()
    
    
    def clearScreen(self, clear):
        os.system(clear)
            
    def exitWrite(self):
        with open(self.__current_dir + self.__transactionFile,"w") as f:
            f.write("{:.2f}\n".format(self.balance))
            f.write("{}".format(self.stored_date))
            for i in range(len(self.transactions)):
                f.write(self.transactions[i].write())
    
    def exitWriteBudget(self):
        with open(self.__current_dir + self.budgetsFile,'w') as f:
            for i in range(len(self.budgets)):
                f.write("{},{:.2f}\n".format(self.budgets[i].name, 
                        self.budgets[i].limit))
    
    def changeMonth(self, date):
        # Write all the transactions to a file
        with open(self.__current_dir + "/old_transactions/" + 
                  self.stored_date.replace("\n","") + "-transactions.txt","w+") as f:
            f.write("{:.2f}\n".format(self.__balance))
            f.write("{}".format(self.stored_date))
            for i in range(len(self.transactions)):
                f.write(self.transactions[i].write())
        
        # Remove all transactions from the list
        self.transactions = []
        
        # Create new transactions file
        with open(self.__current_dir + self.__transactionFile,"w") as f:
            f.write("{:.2f}\n".format(self.__balance))
            f.write(date + "\n")
        
        # Rewrite the budgets file
        amount = 0.0
        with open(self.__current_dir + self.budgetsFile,'w') as f:
            for i in range(len(self.budgets)):
                if self.budgets[i].name != "Other":
                    f.write("{},{:.2f}\n".format(self.budgets[i].name, 
                        self.budgets[i].limit))
                    if self.budgets[i].limit - self.budgets[i].current != 0:
                        amount += (self.budgets[i].limit - self.budgets[i].current)
                else:
                    f.write("{},{:.2f}\n".format(self.budgets[i].name,
                            self.budgets[i].limit + amount))
        
        self.uploadOld()
        
        # Remove the budgets
        self.budgets = []
        
        # Reload the budgets
        self.loadBudgets()
        
        
        
        self.stored_date = date
        print ("Successfully Changed Month.\n")
    
    def addNewBudget(self, limit, name):
        
        self.budgets.append(budgets.Budget(limit, name))
        
    
    def removeBudget(self, index):
        self.budgets.pop(index)
    
    def getFiles(self):
        self.loadNetwork()
        print ("Downloading Files From Server . . .")
        try:
            
            self.ssh.connect(self.__ip, self.__port, self.__user, self.__passwd)
            sftp = self.ssh.open_sftp()
            sftp.get(self.__remoteTransactionPath, self.__current_dir + self.__transactionFile)
            sftp.get(self.__remoteBudgetPath, self.__current_dir + self.budgetsFile)
            sftp.close()
            self.ssh.close()
        except Exception as e:
            print (e)
            traceback.print_exc()
            input()
            exit()
        else:
            print ("Files Downloaded Successfully.")
    
    def putFiles(self):
        print ("Uploading Files To Server . . .")
        try:
            
            self.ssh.connect(self.__ip, self.__port, self.__user, self.__passwd)
            sftp = self.ssh.open_sftp()
            sftp.put(self.__current_dir + self.__transactionFile, self.__remoteTransactionPath)
            sftp.put(self.__current_dir + self.budgetsFile, self.__remoteBudgetPath)
            sftp.close()
            self.ssh.close()
        except Exception as e:
            print (e)
            traceback.print_exc()
            input()
            exit()
        else:
            print ("Files Uploaded Successfully.")
    
    def uploadOld(self):
        print ("Uploading Old File To Server . . .")
        try:
            self.ssh.connect(self.__ip, self.__port, self.__user, self.__passwd)
            sftp = self.ssh.open_sftp()
            sftp.put(self.__current_dir + "/old_transactions/" +
                     self.stored_date.replace("\n","") + "-transactions.txt",
                     self.__oldRemotePath + self.stored_date.replace("\n","")
                     + "-transactions.txt")
            sftp.put(self.__current_dir + self.budgetsFile, self.__remoteBudgetPath)
            sftp.close()
            self.ssh.close()
        except Exception as e:
            print (e)
            traceback.print_exc()
            input()
            exit()
        else:
            print ("Old Files Uploaded Successfully.")
    
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
            
    def loadNetwork(self):
        with open(self.__current_dir + "/network.cfg","r") as f:
                tokens = f.readline().split(",")
                
                
                self.__ip = tokens[0]
                
                self.__port = int(tokens[1])
                
                self.__user = tokens[2]
                
                self.__passwd = tokens[3].replace("\n","")
                
                
                buffer = f.readline()
                self.__remoteTransactionPath = buffer.replace("\n","")
                
                
                buffer = f.readline()
                self.__remoteBudgetPath = buffer.replace("\n","")
                
                
                buffer = f.readline()
                self.__oldRemotePath = buffer.replace("\n","")
                
