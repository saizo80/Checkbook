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

class budgetController:
    def __init__(self):
        self.__transactions = []
        self.budgets = []
        self.__transactionFile = "/transactions.txt"
        self.budgetsFile = "/budgets.txt"
        self.__current_dir = os.path.dirname(os.path.realpath(__file__))
        self.__balance = 0.0
        self.stored_date = ""
        self.__remoteTransactionPath = "/home/pi/vault/Serious_files/Financial_Documents/Budget_Files/transactions.txt"
        self.__remoteBudgetPath = "/home/pi/vault/Serious_files/Financial_Documents/Budget_Files/budgets.txt"
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
            self.__balance = float(input("Please Enter your"
                                                     " current Balance: "))
        except:
            print ("Incorrect Input.")
            return self.cantFindBalance()
    def loadTransactions(self):
        gotBalance = False
        try:
            with open(self.__current_dir + self.__transactionFile, "r") as f:
                for line in f:
                    if ',' not in line:
                        if '-' in line and '.' not in line:
                            self.stored_date = line
                            if self.stored_date == "":
                                self.cantFindDate()
                        else:
                            self.__balance = float(line)
                            gotBalance = True
                    elif 'Deposit' not in line:
                        tokens = line.split(',')
                        self.__transactions.append(transaction(tokens[0],
                            float(tokens[1]),tokens[2], tokens[3], tokens[4].replace("\n","")))
                        Type = tokens[2].replace("\n","")

                        for i in range(len(self.budgets)):
                            if Type == self.budgets[i].name:
                                self.budgets[i].add(float(tokens[1]))
                    else:
                        tokens = line.split(",")
                        self.__transactions.append(transaction(tokens[0],
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
    
    def printTransactions(self):
        for i in range(len(self.__transactions)):
            print(self.__transactions[i].toString())
        print ("\nCurrent Balance: ${:.2f}".format(self.__balance))
        print ("\n__________________\n")
        
    def printBudgets(self):
        for i in range(len(self.budgets)):
            print (self.budgets[i].report())
            print ("\n_________________\n")
        print ("\n")
    
    def addTransaction(self, Type, amount, budgetChoice, date):
        amount = float(amount)
        print ("Please give a short Description.")
        des = input()
        self.__transactions.append(transaction(Type, amount, budgetChoice, date, des))

        if budgetChoice != "":
            for i in range(len(self.budgets)):
                if budgetChoice == self.budgets[i].name:
                    self.budgets[i].add(amount)
            
            
        if 'Purchase' in Type:
            self.__balance -= amount
        else:
            self.__balance += amount
        
        
    def removeTransaction(self):
        for i in range(len(self.__transactions)):
            print ("[{}] : {}".format(i + 1, self.__transactions[i].toString()))
        choice = int(input("Which one would you like to remove? Enter"+
                           " -1 to cancel: "))
        if choice != -1:
            amount = self.__transactions[choice-1].amount
            if 'Purchase' in self.__transactions[choice-1].Type:
                self.__balance += amount
            else:
                self.__balance -= amount
            
            budgetChoice = self.__transactions[choice-1].budgetType
            if budgetChoice != "":
                for i in range(len(self.budgets)):
                    if budgetChoice == self.budgets[i].name:
                        self.budgets[i].add(amount - (amount * 2))
                    
            self.__transactions.pop(choice - 1)
    
    def changeBudget(self):
        for i in range(len(self.budgets)):
            print ("[{}] {}: ${:.2f}".format(i + 1, self.budgets[i].name,
                   self.budgets[i].limit))
        try:
            choice = int(input())
            if choice != -1:
                choice -= 1
                amount = float(input("\nEnter a new Amount: "))
                self.budgets[choice].limit = amount
            else:
                return
        except Exception as e:
            print (e)
            traceback.print_exc()
            input("Press Enter to Continue.")
            return
    
    def changeTranDate(self):
        for i in range(len(self.__transactions)):
            print ("[{}] : {}".format(i + 1, self.__transactions[i].toString()))
        choice = int(input("Which one would you like to change? Enter"+
                           " -1 to cancel: "))
        if choice != -1:
            newDate = input("Please enter date in this format mm-dd-yy: ")
            self.__transactions[choice - 1].date = newDate
    
    
    def clearScreen(self, clear):
        os.system(clear)
            
    def exitWrite(self):
        with open(self.__current_dir + self.__transactionFile,"w") as f:
            f.write("{:.2f}\n".format(self.__balance))
            f.write("{}".format(self.stored_date))
            for i in range(len(self.__transactions)):
                f.write(self.__transactions[i].write())
    
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
            for i in range(len(self.__transactions)):
                f.write(self.__transactions[i].write())
        
        # Remove all transactions from the list
        self.__transactions = []
        
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
    
    def addNewBudget(self):
        try:
            print("\nEnter the name for the new Budget:")
            name = input()
            print("\nEnter the limit for the Budget:")
            limit = float(input())
        except Exception as e:
            print(e)
            traceback.print_exc()
        else:
            self.budgets.append(budgets.Budget(limit, name))
        print ()
    
    def removeBudget(self):
        try:
            print("\nIt could be bad if you removed a budget that\n"
                  "has transactions for this period. Be Warned.\n"
                  "Enter -1 to Cancel.\n")
            for i in range(len(self.budgets)):
                print ("[{}] {}\n".format(i+1, self.budgets[i].report()))
                
            print ()
            choice = int(input())
            if choice != -1:
                self.budgets.pop(choice-1)
        except Exception as e:
            print (e)
            traceback.print_exc()
        print ()
    
    def getFiles(self):
        print ("Downloading Files From Server . . .")
        try:
            with open(self.__current_dir + "/network.cfg","r") as f:
                for line in f:
                    tokens = line.split(',')
                    
            ip = tokens[0]
            port = int(tokens[1])
            user = tokens[2]
            passwd = tokens[3]
            
            self.ssh.connect(ip, port, user, passwd)
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
            with open(self.__current_dir + "/network.cfg","r") as f:
                for line in f:
                    tokens = line.split(',')
                    
            ip = tokens[0]
            port = int(tokens[1])
            user = tokens[2]
            passwd = tokens[3]
            
            self.ssh.connect(ip, port, user, passwd)
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
        remotePath = "/home/pi/vault/Serious_files/Financial_Documents/Budget_Files/Old_Transactions/"
        try:
            with open(self.__current_dir + "/network.cfg","r") as f:
                for line in f:
                    tokens = line.split(',')
                    
            ip = tokens[0]
            port = int(tokens[1])
            user = tokens[2]
            passwd = tokens[3]
            
            self.ssh.connect(ip, port, user, passwd)
            sftp = self.ssh.open_sftp()
            sftp.put(self.__current_dir + "/old_transactions/" +
                     self.stored_date.replace("\n","") + "-transactions.txt",
                     remotePath + self.stored_date.replace("\n","")
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
            