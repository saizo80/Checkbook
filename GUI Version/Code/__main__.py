# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 13:49:27 2019

@author: Matthew Thornton

still need to add:
    remove a transaction - DONE
    change transaction date - DONE
    change current balance - DONE
    change budget limit - DONE
    add a new budget - DONE
    remove a budget - DONE
    
"""

import tkinter as tk
from tkinter import ttk
import budgetController as bC
import platform
from datetime import date

if 'Windows' in platform.system():
    LARGE_FONT = ("Arial", 12) # font's family is Arial, font's size is 12
    SMALL_FONT = ("Arial", 9)
else:
    SMALL_FONT = ("Arial", 14)
    LARGE_FONT = ("Arial", 19)

todayBuffer = date.today()
today = todayBuffer.strftime('%b-%y')
transactionDate = todayBuffer.strftime('%m-%d-%y')

CHANGED = False

BUDGET_CHANGED = False


bControl = bC.budgetController()

bControl.loadBudgets()

bControl.loadTransactions()

if today != bControl.stored_date.replace("\n",""):
            bControl.changeMonth(today)
            CHANGED = True
            BUDGET_CHANGED = True


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.test = "test"
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Checkbook") # set the title of the main window
        
        
        
        #self.geometry("400x500") # set size of the main window to 300x300 pixels
        
        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
        self.frames = {} # these are pages we want to navigate to
 
        for F in (landingPage, transactionMenu, budgetReport, 
                  printTransactions, addTransaction, budgetMenu, 
                  removeTransaction, changeTransactionDate, changeBalance,
                  changeBudgetLimit, addBudget, removeBudget): # for each page
            frame = F(container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky="nsew") # grid it to container
 
        self.show_frame(landingPage) # let the first page is StartPage
 
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
 
class landingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Start Page', font=LARGE_FONT)
        label.pack(pady=10, padx=10) # center alignment
 
        button1 = ttk.Button(self, text='Transaction Menu',  # when click on this button, call the show_frame method to make PageOne appear
                            width=25, command=lambda : controller.show_frame(transactionMenu))
        button1.pack() # pack it in
        
        button2 = ttk.Button(self, text="Budget Menu", width=25, command=lambda: controller.show_frame(budgetMenu))
        button2.pack()
        
        quitButton = ttk.Button(self, text="Quit", width=25, command = lambda : self.exitProgram(controller))
        quitButton.pack()
        
    def exitProgram(self, controller):
        global CHANGED
        global BUDGET_CHANGED
        if CHANGED:
            bControl.exitWrite()
        if BUDGET_CHANGED:
            bControl.exitWriteBudget()
        
        if BUDGET_CHANGED or CHANGED:
            bControl.putFiles()
        
        controller.destroy()
 
class transactionMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Transaction Menu', font=LARGE_FONT)
        label.pack(pady=10, padx=10)
 
        homeButton = ttk.Button(self, text='Back', # likewise StartPage
                            width=25, command=lambda : controller.show_frame(landingPage))
        printButton = ttk.Button(self, text="Print all Transactions", width=25, command=lambda:controller.show_frame(printTransactions))
        
        addButton = ttk.Button(self, text="Add Transaction", width=25, command=lambda:controller.show_frame(addTransaction))
        
        removeButton = ttk.Button(self, text="Remove Transaction", width=25, command=lambda:controller.show_frame(removeTransaction))
        
        changeDate = ttk.Button(self, text='Change a Transaction Date', width=25, command = lambda:controller.show_frame(changeTransactionDate))
        
        changeBalanceButton = ttk.Button(self, text='Change Balance', width=25, command = lambda:controller.show_frame(changeBalance))
        
        printButton.pack()
        addButton.pack()
        removeButton.pack()
        changeDate.pack()
        changeBalanceButton.pack()
        homeButton.pack(padx=20,pady=20)

class budgetMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Budget Menu", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        budgetReportButton = ttk.Button(self, text="Budget Report", width=25, command=lambda:controller.show_frame(budgetReport))
        
        homeButton = ttk.Button(self, text="Back", width=25, command = lambda:controller.show_frame(landingPage))
        
        limitButton = ttk.Button(self, text="Change Budget Limit", width=25, command = lambda:controller.show_frame(changeBudgetLimit))
        
        addButton = ttk.Button(self, text="Add a Budget", width=25, command=lambda:controller.show_frame(addBudget))
        
        removeButton = ttk.Button(self, text="Remove a Budget", width=25, command=lambda:controller.show_frame(removeBudget))
        
        budgetReportButton.pack()
        limitButton.pack()
        addButton.pack()
        removeButton.pack()
        homeButton.pack(pady=20,padx=20)

class printTransactions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.txt = tk.Text(self, borderwidth=1, relief="sunken")
        self.txt.config(font=SMALL_FONT, undo=True, wrap='word', width=40, height=20)
        self.txt.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        self.txt.insert(1.0, bControl.getTransactions())

        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set
        
        button2 = ttk.Button(self, text="Update", width=25, command=self.updateTxt)
        button2.grid(row=1, column=0, sticky='nsew')
        button1 = ttk.Button(self, text ="Back", width=25, command = lambda : controller.show_frame(transactionMenu))
        button1.grid(row=2, column=0, sticky='nsew')
        
        
    def updateTxt(self):
        self.txt.delete("1.0", "end")
        
        self.txt = tk.Text(self, borderwidth=1, relief="sunken")
        self.txt.config(font=SMALL_FONT, undo=True, wrap='word', width=40, height=20)
        self.txt.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        self.txt.insert(1.0, bControl.getTransactions())

        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set
        
class budgetReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
      
        self.txt = tk.Text(self, borderwidth=1, relief="sunken")
        self.txt.config(font=SMALL_FONT, undo=True, wrap='word', width=40, height=20)
        self.txt.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        self.txt.insert(1.0, bControl.getBudgets())
        
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

        button2 = ttk.Button(self, text="Update", width=25, command = self.updateReport)
        button2.grid(row=1, column=0, sticky='nsew')
        button1 = ttk.Button(self, text ="Back to Home", width=25, command = lambda : controller.show_frame(budgetMenu))
        button1.grid(row=2, column=0, sticky='nsew')
    
    def updateReport(self):
        self.txt.delete("1.0","end")
      
        self.txt = tk.Text(self, borderwidth=1, relief="sunken")
        self.txt.config(font=SMALL_FONT, undo=True, wrap='word', width=40, height=20)
        self.txt.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        self.txt.insert(1.0, bControl.getBudgets())
        
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set
        
class addTransaction(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Add Transaction:", font = LARGE_FONT)
        label.grid(row=1, column=2)
        
       # - - - - - - - - - - - - -
       # Specify Transaction Type:
        self.tranType = tk.StringVar()
        self.tranType.set("0")
        typeFrame = ttk.LabelFrame(self, text="Type", relief=tk.RIDGE, padding=6)
        typeFrame.grid(row=2, column=1, padx=6, sticky=tk.N + tk.W + tk.S + tk.E)
    
         
        purchase = ttk.Radiobutton(typeFrame, text="Purchase",
                                       variable=self.tranType, value="Purchase")
        deposit = ttk.Radiobutton(typeFrame, text="Deposit",
                                       variable=self.tranType, value="Deposit")
        
        purchase.grid(row=1,column=1, sticky=tk.W + tk.N)
        deposit.grid(row=2, column=1, sticky=tk.W + tk.N)
        
        
        # - - - - - - - - - - - - - - - 
        # Specify Budget Type:
        self.budgetType = tk.StringVar()
        self.budgetType.set("0")
        budgetFrame = ttk.LabelFrame(self, text="Budget Type\n(Not needed if Deposit)", relief=tk.RIDGE, padding=6)
        budgetFrame.grid(row=3, column=1, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        
        budgetrow = 1
        for i in range(len(bControl.budgets)):
            budget = ttk.Radiobutton(budgetFrame,text=bControl.budgets[i].name,
                                     variable=self.budgetType,
                                     value=bControl.budgets[i].name)
            budget.grid(row=budgetrow,column=1, sticky=tk.W + tk.N)
            budgetrow += 1
        
        
        # - - - - - - - - - - - - - - -
        # Specify Amount:
        self.amount = tk.StringVar()
        self.amount = ""
        
        amountFrame = ttk.LabelFrame(self, text="Amount", relief=tk.RIDGE, padding=6)
        amountFrame.grid(row=2, column=2, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        
        self.amountEntry = ttk.Entry(amountFrame)
        self.amountEntry.grid(row=1,column=1, sticky=tk.W+tk.N)
        
        # - - - - - - - - - - - - -
        # Description:
        self.description = tk.StringVar()
        self.description = ""
        
        descriptionFrame = ttk.LabelFrame(self, text="Description", relief=tk.RIDGE, padding=6)
        descriptionFrame.grid(row=3, column=2, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        
        self.description = tk.Text(descriptionFrame, height=10, width=20)
        self.description.grid(row=1,column=1, sticky=tk.W+tk.N)
        
        # - - - - - - - - - - - - - 
        # Update and exit buttons
        enterButton = ttk.Button(self, text="Enter", width=25, command=lambda: self.passInfo(parent, controller))
        enterButton.grid(row=4,column=1)
        
        printTrans = ttk.Button(self, text ="Print Transactions", width=25, command=lambda:controller.show_frame(printTransactions))
        printTrans.grid(row=5,column=1)
        
        
        quitButton = ttk.Button(self, text ="Back to Home", width=25, command = lambda : controller.show_frame(transactionMenu))
        quitButton.grid(row=6, column=1)
        
        
        
    def passInfo(self, parent, controller):
        if (self.tranType.get() == "Deposit"):
            self.budgetType.set("")
    
        amount1 = float(self.amountEntry.get())
        
        bControl.addTransaction(self.tranType.get(), amount1,
                                self.budgetType.get(), transactionDate, 
                                self.description.get("1.0", "end"))
        global CHANGED
        CHANGED = True
        
        
        controller.show_frame(transactionMenu)
        
class removeTransaction(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Remove Transaction:", font = LARGE_FONT)
        #label.grid(row=1, column=2)
        label.pack(padx=10,pady=10)
        
        self.combobox_value = tk.StringVar()
        self.combo = ttk.Combobox(self, height=10,width=50, textvariable=self.combobox_value)
        self.combo.pack()
        
        self.combo['values'] = bControl.getTransactionsCombo()
        self.combo.current(0)
        
        enterButton = ttk.Button(self, text="Enter", width=25, command=lambda:self.passInfo(parent,controller))
        enterButton.pack()
        
        quitButton = ttk.Button(self, text="Back", width=25, command=lambda:controller.show_frame(transactionMenu))
        quitButton.pack()
    
    def passInfo(self, parent, controller):
        bControl.removeTransaction(self.combobox_value.get())
        self.combo['values'] = bControl.getTransactionsCombo()
        self.combo.current(0)
        global CHANGED
        CHANGED = True
        
class changeTransactionDate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Change Transaction Date:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.combobox_value = tk.StringVar()
        self.combo = ttk.Combobox(self, height=10, width=50, textvariable=self.combobox_value)
        self.combo.pack()
        
        self.combo['values'] = bControl.getTransactionsCombo()
        self.combo.current(0)
        
        label2 = ttk.Label(self, text="Enter New Date\n   mm-dd-yy:", font=SMALL_FONT)
        label2.pack(pady=10,padx=10)
        
        self.amountEntry = ttk.Entry(self)
        self.amountEntry.pack(padx=10)
        
        enterButton = ttk.Button(self, text="Enter", width=25, command=lambda:self.passInfo(parent,controller))
        enterButton.pack(pady=10)
        
        quitButton = ttk.Button(self, text="Back", width=25, command=lambda:controller.show_frame(transactionMenu))
        quitButton.pack()
        
    def passInfo(self, parent, controller):
        bControl.changeTranDate(self.combobox_value.get(), self.amountEntry.get())
        self.combo['values'] = bControl.getTransactionsCombo()
        self.combo.current(0)
        global CHANGED
        CHANGED = True

class changeBalance(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = ttk.Label(self, text="Change Balance:", font=LARGE_FONT)
        titleLabel.pack(pady=10,padx=10)
        
        self.balanceLabel = ttk.Label(self, text="${:.2f}".format(bControl.balance), font=SMALL_FONT)
        self.balanceLabel.pack(pady=10, padx=10)
        
        self.amountEntry = ttk.Entry(self)
        self.amountEntry.pack()
        
        enterButton = ttk.Button(self, text="Enter", width=25, command=lambda:self.passInfo(parent,controller))
        enterButton.pack(pady=10)
        
        quitButton = ttk.Button(self, text="Back", width=25, command=lambda:controller.show_frame(transactionMenu))
        quitButton.pack()
        
    def passInfo(self, parent, controller):
        bControl.balance = float(self.amountEntry.get())
        self.balanceLabel['text'] = "${:.2f}".format(bControl.balance)
        global CHANGED
        CHANGED = True

class changeBudgetLimit(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = ttk.Label(self, text="Change Budget Limit:", font=LARGE_FONT)
        #titleLabel.pack(pady=10,padx=10)
        titleLabel.grid(row=1,column=2)
        
        self.budgetFrame = ttk.LabelFrame(self, text="Budgets", relief=tk.RIDGE, padding=6)
        self.budgetFrame.grid(row=2, column=1, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        
        self.budgetIndex = tk.StringVar()
        self.budgetIndex.set('-1')
        
        budgetrow = 1
        for i in range(len(bControl.budgets)):
            self.budget = ttk.Radiobutton(self.budgetFrame,
                                     text="{} - ${:.2f}".format(
                                             bControl.budgets[i].name,
                                             bControl.budgets[i].limit)
                                     , variable=self.budgetIndex, value=str(i))
            self.budget.grid(row=budgetrow,column=1, sticky=tk.W + tk.N)
            budgetrow += 1
        
        amountFrame = ttk.LabelFrame(self, text="New Limit", relief=tk.RIDGE, padding=6)
        amountFrame.grid(row=2, column=2, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        
        self.newLimit = ttk.Entry(amountFrame)
        self.newLimit.grid(row=1,column=1)
        
        enterButton = ttk.Button(self, text="Enter", width=25, command=lambda:self.passInfo(parent,controller))
        enterButton.grid(row=3, column=1)
        
        quitButton = ttk.Button(self, text="Back", width=25, command=lambda:controller.show_frame(budgetMenu))
        quitButton.grid(row=4, column=1)
    
    def passInfo(self, parent, controller):
        bControl.changeBudget(int(self.budgetIndex.get()), float(self.newLimit.get()))
        global BUDGET_CHANGED
        BUDGET_CHANGED = True
        budgetrow = 1
        for i in range(len(bControl.budgets)):
            self.budget = ttk.Radiobutton(self.budgetFrame,
                                     text="{} - ${:.2f}".format(
                                             bControl.budgets[i].name,
                                             bControl.budgets[i].limit)
                                     , variable=self.budgetIndex, value=str(i))
            self.budget.grid(row=budgetrow,column=1, sticky=tk.W + tk.N)
            budgetrow += 1

class addBudget(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = ttk.Label(self, text="Add New Budget:", font=LARGE_FONT)
        titleLabel.grid(row=1, column=2)
        
        self.nameFrame = ttk.LabelFrame(self, text="Budget Name", relief=tk.RIDGE, padding=6)
        self.nameFrame.grid(row=2, column=1, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
            
        self.nameEntry = ttk.Entry(self.nameFrame)
        self.nameEntry.grid(row=1,column=1)
        
        self.limitFrame = ttk.LabelFrame(self, text="Budget Limit", relief=tk.RIDGE, padding=6)
        self.limitFrame.grid(row=3, column=1, padx=6)
        
        self.limitEntry = ttk.Entry(self.limitFrame)
        self.limitEntry.grid(row=1, column=1)
        
        enterButton = ttk.Button(self, text="Enter", width=25,command=self.passInfo)
        enterButton.grid(row=2, column=2)
        
        quitButton = ttk.Button(self, text="Back", width=25,command=lambda:controller.show_frame(budgetMenu))
        quitButton.grid(row=3, column=2)
        
    def passInfo(self):
        bControl.addNewBudget(float(self.limitEntry.get()), self.nameEntry.get())
        global BUDGET_CHANGED
        BUDGET_CHANGED = True

class removeBudget(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = ttk.Label(self, text="Remove a Budget:", font=LARGE_FONT)
        titleLabel.grid(row=1, column=2)
        
        warningLabel = ttk.Label(self, text="This should probably not be used.\nIt will break stuff.", font=SMALL_FONT)
        warningLabel.grid(row=2, column=2)
        
        self.budgetIndex = tk.StringVar()
        self.budgetIndex.set('-1')
        
        self.budgetFrame = ttk.LabelFrame(self, text="Budgets", relief=tk.RIDGE, padding=6)
        self.budgetFrame.grid(row=4, column=1, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        
        budgetrow = 1
        for i in range(len(bControl.budgets)):
            self.budget = ttk.Radiobutton(self.budgetFrame,
                                     text="{} - ${:.2f}".format(
                                             bControl.budgets[i].name,
                                             bControl.budgets[i].limit)
                                     , variable=self.budgetIndex, value=str(i))
            self.budget.grid(row=budgetrow,column=1, sticky=tk.W + tk.N)
            budgetrow += 1
            
        enterButton = ttk.Button(self, text="Enter", width=25,command=self.passInfo)
        enterButton.grid(row=5, column=1)
        
        quitButton = ttk.Button(self, text="Back", width=25,command=lambda:controller.show_frame(budgetMenu))
        quitButton.grid(row=6, column=1)
    
    def passInfo(self):
        bControl.removeBudget(int(self.budgetIndex.get()))
        
        global BUDGET_CHANGED
        BUDGET_CHANGED = True
        budgetrow = 1
        for i in range(len(bControl.budgets)):
            self.budget = ttk.Radiobutton(self.budgetFrame,
                                     text="{} - ${:.2f}".format(
                                             bControl.budgets[i].name,
                                             bControl.budgets[i].limit)
                                     , variable=self.budgetIndex, value=str(i))
            self.budget.grid(row=budgetrow,column=1, sticky=tk.W + tk.N)
            budgetrow += 1
        
        self.budgetIndex.set('-1')
if __name__ == '__main__':
    app = MainWindow()
    app.minsize(400,300)
    app.mainloop()