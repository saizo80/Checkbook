# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:36:56 2019

@author: Matthew Thornton

Needs to be able to:
    Print all Transactions
    Add Transactions:
        Purchases
        Deposits
    Print Budget Info
    Change Budget Amounts

"""
import budgetController
import platform
from datetime import date

class __main__:
    def __init__(self):
        self.changed = False
        self.budget_change = False
        if 'Windows' in platform.system():
            self.os_clear = 'cls'
        else:
            self.os_clear = 'clear'
        
        todayBuffer = date.today()
        self.today = todayBuffer.strftime('%b-%y')
        self.transactionDate = todayBuffer.strftime('%m-%d-%y')
        
        self.control = budgetController.budgetController()
        self.control.loadBudgets()
        self.control.loadTransactions()
        
        
        if self.today != self.control.stored_date.replace("\n",""):
            self.control.changeMonth(self.today)
            self.changed = True
            self.budget_change = True
        
        self.control.clearScreen(self.os_clear)

        self.main_menu = ("[0] Exit\n"
                          "[1] Manage Transactions\n"
                          "[2] Manage Budgets")
        
        self.transaction_menu = ("[0] Back\n"
                                 "[1] Print all Transactions\n"
                                 "[2] Add a Transaction\n"
                                 "[3] Remove a Transaction\n"
                                 "[4] Change a Transaction Date\n"
                                 "[5] Change the Current Balance")
        
        self.budget_menu = ("[0] Back\n"
                            "[1] Print Budget Reports\n"
                            "[2] Change a Budget Limit\n"
                            "[3] Add a new Budget\n"
                            "[4] Remove a Budget")
        
        self.menu()
        
        
    def menu(self):
        while True:
            print(self.main_menu)
            print ()
            
            choice = input()
            if '1' in choice:
                while True:
                    print (self.transaction_menu)
                    print ()
                    choice = input()
                    if '1' in choice:
                        print ()
                        self.control.printTransactions()
                    elif '2' in choice:
                        self.changed = True
                        print ("\n[1] Purchase\n"+
                               "[2] Deposit")
                        Type = input()
                        if '1' in Type and '-1' not in Type:
                            Type = 'Purchase'
                            
                            for i in range(len(self.control.budgets)):
                                print ("[{}] {}\n".format(i+1,self.control.budgets[i].name))
                            bC = int(input())
                            budgetChoice = self.control.budgets[bC-1].name
                        elif '2' in Type:
                            Type = 'Deposit'
                            budgetChoice = ''
                        else:
                            continue
                        amount = input("Enter the Amount: ")
                        print ()
                        self.control.addTransaction(Type, amount, budgetChoice, self.transactionDate)
                    elif '3' in choice:
                        self.changed = True
                        print ()
                        self.control.removeTransaction()
                        print ()
                    elif '4' in choice:
                        print ()
                        self.control.changeTranDate()
                        self.changed = True
                        print ()
                    elif '5' in choice:
                        print ("\nEnter the new Balance:")
                        try:
                            newBalance = float(input())
                            self.control.setBalance(newBalance)
                            self.changed = True
                        except Exception as e:
                            print (e)
                        print ()
                    elif 'clear' in choice:
                        self.control.clearScreen(self.os_clear)
                    elif '0' or 'exit' in choice:
                        break
                    else:
                        print ("Invalid Input.\n")
            elif '2' in choice:
                while True:
                    print (self.budget_menu)
                    print ()
                    
                    choice = input()
                    
                    if '1' in choice:
                        print ()
                        self.control.printBudgets()
                    elif '2' in choice:
                        print ()
                        self.control.changeBudget()
                        self.budget_change = True
                        print ()
                    elif '3' in choice:
                        self.control.addNewBudget()
                        self.budget_change = True
                    elif '4' in choice:
                        self.control.removeBudget()
                        self.budget_change = True
                    elif 'clear' in choice:
                        self.control.clearScreen(self.os_clear)
                    else:
                        break
            elif 'clear' in choice:
                self.control.clearScreen(self.os_clear)
            elif '0' or 'exit' in choice:
                if self.changed:
                    print ("Writing new Transaction Data . . .")
                    self.control.exitWrite()
                    
                if self.budget_change:
                    print ("Writing new Budget Data . . .")
                    self.control.exitWriteBudget()
                    
                if self.budget_change or self.changed:
                    self.control.putFiles()
                    
                break 
            else:
                print ("Invalid Input.\n")
                        
        
if __name__ == '__main__':
    __main__()